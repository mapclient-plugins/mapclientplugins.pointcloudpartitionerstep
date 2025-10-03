"""
Created: April, 2023

@author: tsalemink
"""
import colorsys
import os
import json
import hashlib
import webbrowser

from PySide6 import QtWidgets, QtCore

from cmlibs.utils.zinc.general import ChangeManager, rotate_to_next_standard_view
from cmlibs.utils.zinc.mesh import find_connected_mesh_elements_0d
from cmlibs.utils.zinc.scene import scene_get_or_create_selection_group
from cmlibs.widgets.collapsibleboxwidget import CollapsibleBox
from cmlibs.widgets.handlers.scenemanipulation import SceneManipulation
from cmlibs.widgets.ui.ui_buttonswidget import Ui_Buttons
from cmlibs.zinc.material import Material

from mapclientplugins.pointcloudpartitionerstep.scene.pointcloudpartitionerscene import PointCloudPartitionerScene
from mapclientplugins.pointcloudpartitionerstep.view.customsceneselection import CustomSceneSelection, MODE_MAP, \
    TYPE_MAP
from mapclientplugins.pointcloudpartitionerstep.view.grouptableview import GroupModel

from mapclientplugins.pointcloudpartitionerstep.view.ui_coordinateswidget import Ui_Coordinates
from mapclientplugins.pointcloudpartitionerstep.view.ui_displaysettingswidget import Ui_DisplaySettings
from mapclientplugins.pointcloudpartitionerstep.view.ui_grouppointswidget import Ui_GroupPoints
from mapclientplugins.pointcloudpartitionerstep.view.ui_pointcloudpartitionerwidget import \
    Ui_PointCloudPartitionerWidget
from mapclientplugins.pointcloudpartitionerstep.view.ui_selectionwidget import Ui_Selection


def _select_elements(field_module, mesh_selection_group, element_identifiers):
    region = field_module.getRegion()
    mesh = mesh_selection_group.getMasterMesh()

    scene = region.getScene()
    with ChangeManager(scene):
        for element_identifier in element_identifiers:
            mesh_selection_group.addElement(mesh.findElementByIdentifier(element_identifier))


def _generate_hash(filename, block_size=2 ** 20):
    md5 = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def _element_ids(mesh_group):
    element_iterator = mesh_group.createElementiterator()

    identifiers = []
    element = element_iterator.next()
    while element.isValid():
        identifiers.append(element.getIdentifier())
        element = element_iterator.next()

    return identifiers


def _documentation_button_clicked():
    webbrowser.open(
        "https://abi-mapping-tools.readthedocs.io/en/latest/mapclientplugins.pointcloudpartitionerstep/docs/index.html")


class PointCloudPartitionerWidget(QtWidgets.QMainWindow):

    def __init__(self, model, parent=None):
        super(PointCloudPartitionerWidget, self).__init__(parent)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self._ui = Ui_PointCloudPartitionerWidget()
        self._ui.setupUi(self)
        self._setup_dock_widget()

        self._group_points_ui.pushButtonDeleteGroup.setEnabled(False)

        self._callback = None
        self._location = None
        self._input_hash = None

        self._model = model
        self._scene = PointCloudPartitionerScene(model)
        self._selection_handler = CustomSceneSelection(QtCore.Qt.Key.Key_S)
        self._field_module = None
        self._points_field_list = ["---"]
        self._surfaces_field_list = ["---"]
        self._connected_sets = []
        self._progress_dialog = None

        self._groups = []
        self._group_materials = []

        self._setup_table_view()
        self._setup_selection_mode_combo_box()
        self._setup_selection_type_combo_box()
        self._setup_point_size_spin_box()
        self._make_connections()

        self._ui.widgetZinc.set_context(model.get_context())
        self._ui.widgetZinc.register_handler(SceneManipulation())
        self._ui.widgetZinc.register_handler(self._selection_handler)
        self._ui.widgetZinc.set_model(model)

        # self._ui.widgetZinc.setSelectionfilter(model.get_selection_filter())

    def _make_connections(self):
        self._buttons_ui.done_pushButton.clicked.connect(self._continue_execution)
        self._buttons_ui.viewAll_pushButton.clicked.connect(self._view_all_button_clicked)
        self._buttons_ui.stdViews_pushButton.clicked.connect(self._standard_views_button_clicked)
        self._buttons_ui.pushButtonDocumentation.clicked.connect(_documentation_button_clicked)
        self._ui.widgetZinc.graphics_initialized.connect(self._zinc_widget_ready)
        self._ui.widgetZinc.pixel_scale_changed.connect(self._pixel_scale_changed)
        self._group_points_ui.pushButtonCreateGroup.clicked.connect(self._create_point_group)
        self._group_points_ui.pushButtonDeleteGroup.clicked.connect(self._remove_associated_point_group)
        self._group_points_ui.pushButtonAddToGroup.clicked.connect(self._add_selected_points_to_group)
        self._group_points_ui.pushButtonRemoveFromGroup.clicked.connect(self._remove_selected_points_from_group)
        self._coordinates_ui.pointsFieldComboBox.textActivated.connect(self._update_point_cloud_field)
        self._coordinates_ui.meshFieldComboBox.textActivated.connect(self._update_mesh_field)
        self._selection_ui.comboBoxSelectionMode.currentIndexChanged.connect(self._update_selection_mode)
        self._selection_ui.comboBoxSelectionType.currentIndexChanged.connect(self._update_selection_type)
        self._selection_ui.pushButtonSelectPointsOnSurface.clicked.connect(self._select_points_on_surface)
        self._display_settings_ui.checkBoxSurfacesVisibility.stateChanged.connect(self._scene.set_surfaces_visibility)
        self._display_settings_ui.checkBoxPointsVisibility.stateChanged.connect(self._scene.set_points_visibility)
        self._display_settings_ui.pointSizeSpinBox.valueChanged.connect(self._scene.set_point_size)
        self._ui.widgetZinc.handler_activated.connect(self._update_label_text)
        self._ui.widgetZinc.selection_updated.connect(self._selection_updated)
        self._group_points_ui.groupTableView.itemDelegateForColumn(1).button_clicked.connect(
            self._add_group_points_to_selection)
        self._selection_ui.pushButtonDeleteSelectedSurfaceSection.clicked.connect(self._delete_selected_surfaces)
        self._selection_ui.comboBoxDeleteSurfaceHistory.currentIndexChanged.connect(
            self._delete_surface_history_index_changed)
        self._selection_ui.doubleSpinBoxTolerance.valueChanged.connect(self._tolerance_value_changed)
        self._selection_ui.pushButtonInvertSelection.clicked.connect(self._invert_selection_clicked)

    def _setup_dock_widget(self):
        parent_widget = QtWidgets.QWidget(self)

        layout = QtWidgets.QVBoxLayout(parent_widget)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)

        self._identifier_label = QtWidgets.QLabel("Identifier: XXXX")
        layout.addWidget(self._identifier_label)

        self._group_points_ui = Ui_GroupPoints()
        self._selection_ui = Ui_Selection()
        self._display_settings_ui = Ui_DisplaySettings()
        self._coordinates_ui = Ui_Coordinates()
        self._buttons_ui = Ui_Buttons()

        for ui in [self._group_points_ui, self._coordinates_ui, self._selection_ui, self._display_settings_ui]:
            form_container = QtWidgets.QWidget()
            ui.setupUi(form_container)
            tools_box = CollapsibleBox(form_container.windowTitle(),
                                       checked=True if ui is self._group_points_ui else False)
            tools_box.add_widget(form_container)
            layout.addWidget(tools_box, stretch=1)

        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum,
                                       QtWidgets.QSizePolicy.Policy.Expanding)
        layout.addSpacerItem(spacer)

        form_container = QtWidgets.QWidget()
        self._buttons_ui.setupUi(form_container)
        layout.addWidget(form_container)

        self._dock_widget = QtWidgets.QDockWidget("Controls", self)
        self._dock_widget.setObjectName("ControlsDock")
        self._dock_widget.setWidget(parent_widget)

        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self._dock_widget)

    def _setup_field_combo_boxes(self):
        self._coordinates_ui.pointsFieldComboBox.addItems(self._points_field_list)
        if self._coordinates_ui.pointsFieldComboBox.count() > 1:
            self._coordinates_ui.pointsFieldComboBox.setCurrentIndex(1)
            self._update_point_cloud_field()

        self._coordinates_ui.meshFieldComboBox.addItems(self._surfaces_field_list)
        if self._coordinates_ui.meshFieldComboBox.count() > 1:
            self._coordinates_ui.meshFieldComboBox.setCurrentIndex(1)
            self._update_mesh_field()

    def _update_point_cloud_field(self):
        self._model.update_point_cloud_coordinates(self._coordinates_ui.pointsFieldComboBox.currentText())
        self._scene.update_point_cloud_coordinates()
        # self._ui.widgetZinc.view_all()

    def _update_mesh_field(self):
        self._model.update_mesh_coordinates(self._coordinates_ui.meshFieldComboBox.currentText())
        self._scene.update_mesh_coordinates()
        # self._ui.widgetZinc.view_all()

    def _setup_table_view(self):
        self._group_points_ui.groupTableView.setModel(GroupModel(self, self._group_points_ui.groupTableView))
        # self._ui.groupTableView.setItemDelegate(TableDelegate(self._ui.groupTableView))
        # self._ui.groupTableView.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self._group_points_ui.groupTableView.horizontalHeader().setSectionResizeMode(0,
                                                                                     QtWidgets.QHeaderView.ResizeMode.Stretch)
        self._group_points_ui.groupTableView.horizontalHeader().setSectionResizeMode(1,
                                                                                     QtWidgets.QHeaderView.ResizeMode.Fixed)
        selection_model = self._group_points_ui.groupTableView.selectionModel()
        selection_model.selectionChanged.connect(self._group_selection_changed)

    def _setup_selection_mode_combo_box(self):
        self._selection_ui.comboBoxSelectionMode.addItems(MODE_MAP.keys())
        self._update_selection_mode()

    def _setup_selection_type_combo_box(self):
        self._selection_ui.comboBoxSelectionType.addItems(TYPE_MAP.keys())
        self._update_selection_type()

    def _setup_point_size_spin_box(self):
        self._display_settings_ui.pointSizeSpinBox.setValue(self._scene.get_point_size())

    def _tolerance_value_changed(self, value):
        self._model.reset_connected_set_index_field()

    def load(self, points_file_location, surfaces_file_location):
        self._field_module = self._model.get_points_region().getFieldmodule()
        self._scene.setup_visualisation()

        previous_hash = self._load_settings()
        self._input_hash = _generate_hash(points_file_location)
        if self._input_hash == previous_hash:
            points_file_location = self.get_output_file()
        self._model.load(points_file_location, surfaces_file_location)

        self._get_regions_fields(self._model.get_points_region(), self._points_field_list, True)
        self._get_regions_fields(self._model.get_surfaces_region(), self._surfaces_field_list, False)
        self._update_node_graphics_subgroup()
        self._setup_field_combo_boxes()
        self._load_deleted_surfaces()

    def _get_regions_fields(self, region, field_list, include_nodes):
        field_module = region.getFieldmodule()
        self._get_fields(field_module, field_list, include_nodes)

    def _get_fields(self, field_module, field_list, include_nodes):
        field_iter = field_module.createFielditerator()
        field = field_iter.next()
        # node_points = field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        while field.isValid():
            if field.isTypeCoordinate() and (field.getNumberOfComponents() == 3) and (
            field.castFiniteElement().isValid()):
                field_list.append(field.getName())
            node_group = field.castGroup()
            if include_nodes and node_group.isValid():
                nodeset_group = node_group.getNodesetGroup(self._model.get_data_points())
                if nodeset_group.isValid():
                    self._add_point_group(node_group)
            field = field_iter.next()

    def clear(self):
        while len(self._groups):
            self._remove_point_group(0)

        self._update_node_graphics_subgroup()

    def set_location(self, location):
        self._location = location
        self._identifier_label.setText(f"Identifier: {os.path.basename(location)}")

    def get_output_file(self):
        return os.path.join(self._location, "nodes-with-groups.exf")

    def _group_selection_changed(self, new_selection):
        print("Group selection changed", len(new_selection.indexes()))
        selection = len(new_selection.indexes()) > 0
        self._ui_update_selection_dependent_buttons(selection)

    def _settings_file(self):
        return os.path.join(self._location, 'settings.json')

    def _write(self):
        if not os.path.exists(self._location):
            os.makedirs(self._location)

        self._model.get_points_region().writeFile(self.get_output_file())

    def group_count(self):
        return len(self._groups)

    def group_data(self, row, column):
        if column == 0:
            return self._groups[row].getName()

    def set_group_data(self, row, column, value):
        if column == 0:
            self._groups[row].setName(value)

    def move_group_data(self, source_row, target_row):
        group_target_row = len(self._groups) - 1 if target_row == -1 else target_row
        model = self._group_points_ui.groupTableView.model()
        model.layoutAboutToBeChanged.emit()
        self._groups.insert(group_target_row, self._groups.pop(source_row))
        self._scene.update_graphics_materials(self._group_materials)
        self._scene.change_graphics_order(source_row, target_row)
        model.layoutChanged.emit()

    def _next_available_name(self, name=None):
        i = 1
        names = [g.getName() for g in self._groups]
        stem_name = "Group"
        unique_name = f"{stem_name}_1" if name is None else name
        name = stem_name if name is None else name

        while unique_name in names:
            unique_name = f"{name}_{i}"
            i += 1

        return unique_name

    def _add_point_group(self, group=None):
        model = self._group_points_ui.groupTableView.model()

        if group is None:
            name = self._next_available_name()
            group = self._field_module.createFieldGroup()
            group.setName(name)

        model.begin_add_group()
        self._register_point_group(group)
        model.end_add_group()

    def _create_point_group(self):
        self._add_point_group()
        self._update_node_graphics_subgroup()

    def _register_point_group(self, group):
        self._groups.append(group)
        self._group_materials.append(None)
        self._update_color_map()
        self._scene.update_graphics_materials(self._group_materials)
        scene = self._model.get_points_region().getScene()
        coordinates = self._model.get_point_cloud_coordinates()
        material = self._group_materials[-1]
        graphic = self._scene.create_point_graphics(scene, coordinates, group, material)
        self._scene.add_group_graphic(graphic)

    def _update_node_graphics_subgroup(self):
        or_group = None
        group_count = 0
        for group in self._groups:
            group_count += 1
            if group_count == 1:
                or_group = group
            else:
                or_group = self._field_module.createFieldOr(or_group, group)

        if group_count == 0:
            self._scene.set_node_graphics_subgroup_field(or_group)
        else:
            tmp = self._field_module.createFieldNot(or_group)
            self._scene.set_node_graphics_subgroup_field(tmp)

    def _selected_row(self):
        selection_model = self._group_points_ui.groupTableView.selectionModel()
        index = selection_model.currentIndex()
        return index.row()

    def _remove_associated_point_group(self):
        model = self._group_points_ui.groupTableView.model()
        row = self._selected_row()
        model.begin_remove_group(row)
        self._remove_points_from_group(row)
        self._remove_point_group(row)
        self._update_node_graphics_subgroup()
        model.end_remove_group()
        self._group_points_ui.groupTableView.selectionModel().clear()

    def _remove_point_group(self, row):
        # Schedule the group for deletion.
        self._groups[row].setManaged(False)

        # Remove related entries.
        del self._groups[row]
        del self._group_materials[row]

        # Update the scene.
        self._update_color_map()
        self._scene.update_graphics_materials(self._group_materials)
        self._scene.delete_point_graphics(row)

    def _update_color_map(self):
        def get_distinct_colors(n):
            hue_partition = 1.0 / (n + 1)
            return [list(colorsys.hsv_to_rgb(hue_partition * value, 1.0, 1.0)) for value in range(0, n)]

        material_module = self._model.get_points_region().getScene().getMaterialmodule()
        colors = get_distinct_colors(len(self._group_materials) + 1)
        colors.pop(0)
        self._group_materials = []
        for i in range(len(colors)):
            material = material_module.createMaterial()
            material.setManaged(True)
            material.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, colors[i])
            material.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, colors[i])
            material.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
            self._group_materials.append(material)

    def _add_group_points_to_selection(self, row):
        selected_group = self._groups[row]
        nodeset_group = selected_group.getOrCreateNodesetGroup(self._model.get_data_points())

        selected_nodeset_group = self._get_node_selection_group()
        scene = self._field_module.getRegion().getScene()
        with ChangeManager(scene):
            node_iter = nodeset_group.createNodeiterator()
            node = node_iter.next()
            while node.isValid():
                selected_nodeset_group.addNode(node)
                node = node_iter.next()

        self._selection_updated()

    def _add_selected_points_to_group(self):
        selected_group = self._groups[self._selected_row()]
        nodeset_group = selected_group.getOrCreateNodesetGroup(self._model.get_data_points())
        self._add_points_to_group(nodeset_group)
        self._selection_updated()

    def _add_points_to_group(self, nodeset_group):
        # Add the selected Nodes to the chosen Group.
        scene = self._field_module.getRegion().getScene()
        selection_group = scene.getSelectionField().castGroup()
        selected_nodeset_group = self._get_node_selection_group()
        with ChangeManager(scene):
            node_iter = selected_nodeset_group.createNodeiterator()
            node = node_iter.next()
            while node.isValid():
                nodeset_group.addNode(node)
                node = node_iter.next()
            selection_group.clear()

    def _remove_selected_points_from_group(self):
        selection_group = self._model.get_point_selection_group()
        selected_nodeset_group = self._get_node_selection_group()
        row = self._selected_row()
        self._remove_points_from_group(row, selection_group, selected_nodeset_group)
        self._selection_updated()

    def _remove_points_from_group(self, row, field_group=None, selected_nodeset_group=None):
        group = self._groups[row]
        nodeset_group = group.getOrCreateNodesetGroup(self._model.get_data_points())

        # If the method was called without a selection group, remove all nodes.
        if field_group is None or selected_nodeset_group is None:
            field_group = group
            selected_nodeset_group = nodeset_group

        # Remove the selected Nodes from the chosen group.
        node_iter = selected_nodeset_group.createNodeiterator()
        node = node_iter.next()
        while node.isValid():
            nodeset_group.removeNode(node)
            node = node_iter.next()
        field_group.clear()

    def _update_selection_mode(self):
        mode = MODE_MAP[self._selection_ui.comboBoxSelectionMode.currentText()]
        self._selection_handler.set_primary_selection_mode(mode)

    def _update_selection_type(self):
        scene_filter_module = self._model.get_context().getScenefiltermodule()
        current_selection_type = self._selection_ui.comboBoxSelectionType.currentText()
        selection_type = TYPE_MAP[current_selection_type]
        scene_filter = scene_filter_module.createScenefilterFieldDomainType(selection_type)
        self._selection_handler.set_scene_filter(scene_filter)
        self._selection_ui.comboBoxDeleteSurfaceHistory.setEnabled(current_selection_type == "Surface Sections")

    def _connected_set_index(self, element_id):
        for index, connected_set in enumerate(self._connected_sets):
            if element_id in connected_set:
                return index

        return -1

    def _prepare_progress_dialog(self, label_text, button_text, total):
        progress = QtWidgets.QProgressDialog(label_text, button_text, 0, total, self)
        progress.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        return progress

    def _select_points_on_surface(self):
        selection_mesh_group = self._get_mesh_selection_group()
        point_coordinate_field = self._model.get_point_cloud_coordinates()
        point_field_module = point_coordinate_field.getFieldmodule()

        self._progress_dialog = self._prepare_progress_dialog("Calculating locations ...", "Cancel", 1000)

        if self._model.get_connected_set_index_field() is None:
            ignore_identifiers = self._list_ignore_element_identifiers()
            tolerance_value = self._selection_ui.doubleSpinBoxTolerance.value()
            self._model.determine_point_connected_surface(self._connected_sets, ignore_identifiers, tolerance_value,
                                                          self._progress_dialog)
            # mesh_coordinate_field = self._model.get_mesh_coordinates()
            #
            # mesh_region = self._model.get_surfaces_region()
            #
            # mesh_field_module = mesh_coordinate_field.getFieldmodule()
            #
            # mesh2d = mesh_field_module.findMeshByDimension(2)
            #
            # # Transfer datapoints over to mesh region.
            # data_points = self._model.get_data_points()
            # copy_nodeset(mesh_region, data_points)
            # copied_data_points = mesh_field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
            #
            # self._progress_dialog = self._prepare_progress_dialog("Calculating locations ...", "Cancel", copied_data_points.getSize())
            #
            # with ChangeManager(mesh_field_module), ChangeManager(point_field_module):
            #     self._connected_set_index_field = point_field_module.createFieldFiniteElement(1)
            #     find_host_coordinates = mesh_field_module.createFieldFindMeshLocation(mesh_coordinate_field, mesh_coordinate_field, mesh2d)
            #     find_host_coordinates.setSearchMode(FieldFindMeshLocation.SEARCH_MODE_NEAREST)
            #     host_coordinates = mesh_field_module.createFieldEmbedded(mesh_coordinate_field, find_host_coordinates)
            #
            #     data_projection_delta_coordinate_field = mesh_field_module.createFieldSubtract(
            #                 mesh_coordinate_field,
            #                 host_coordinates)
            #     data_projection_error_field = mesh_field_module.createFieldMagnitude(
            #                 data_projection_delta_coordinate_field)
            #     tolerance_value = self._selection_ui.doubleSpinBoxTolerance.value()
            #     tolerance_field = mesh_field_module.createFieldConstant(tolerance_value)
            #
            #     conditional_field = mesh_field_module.createFieldLessThan(data_projection_error_field, tolerance_field)
            #
            #     datapoint_template = data_points.createNodetemplate()
            #     datapoint_template.defineField(self._connected_set_index_field)
            #
            #     identifiers = get_identifiers(copied_data_points)
            #     divisions = 1
            #     chunk_size = len(identifiers) // divisions
            #     split_identifiers = [identifiers[i * chunk_size: (i + 1) * chunk_size] for i in range(divisions)]
            #     remainder = identifiers[divisions*chunk_size:]
            #     if remainder:
            #         split_identifiers.append(remainder)
            #
            #     cancelled = False
            #     count = 0
            #
            #     num_datapoints = len(identifiers)
            #     update_interval = max(1, int(num_datapoints * 0.01))
            #     progress_report_points = set([i for i in range(update_interval)] + [i for i in range(update_interval, num_datapoints, update_interval)])
            #     identifier_surface_index_map = {}
            #     mesh_cache = mesh_field_module.createFieldcache()
            #     st_time = int_time = time.time()
            #     for identifier in identifiers:
            #         datapoint = copied_data_points.findNodeByIdentifier(identifier)
            #         element_identifier, value = _find_datapoint_location(mesh_cache, conditional_field, find_host_coordinates, datapoint)
            #
            #         # if value > 0.5:
            #         #     index = self._connected_set_index(element_identifier)
            #         #     if index != -1:
            #         #         identifier_surface_index_map[identifier] = index
            #
            #         if count in progress_report_points:
            #             now = time.time()
            #             print(f"Elapsed time [{count}/{num_datapoints}]: {now - st_time:.2f} {now - int_time:.2f}")
            #             int_time = now
            #             self._progress_dialog.setValue(count)
            #         count += 1
            #         if self._progress_dialog.wasCanceled():
            #             cancelled = True
            #             break
            #
            #     self._progress_dialog.setValue(num_datapoints)
            #     copied_data_points.destroyAllNodes()
            #     if cancelled:
            #         self._connected_set_index_field = None
            #
            #     print(len(identifier_surface_index_map))
            #     point_cache = point_field_module.createFieldcache()
            #     # point_datapoint = data_points.findNodeByIdentifier(identifier)
            #     # point_datapoint.merge(datapoint_template)
            #     # point_cache.setNode(point_datapoint)
            #     # self._connected_set_index_field.assignReal(point_cache, index)

        if self._model.get_connected_set_index_field() is not None:
            element = selection_mesh_group.createElementiterator().next()
            index = self._connected_set_index(element.getIdentifier())
            with ChangeManager(point_field_module):
                constant_field = point_field_module.createFieldConstant(index)
                conditional_field = point_field_module.createFieldEqualTo(self._model.get_connected_set_index_field(),
                                                                          constant_field)

            selection_group = self._get_node_selection_group()
            points_region = self._model.get_points_region()
            scene = points_region.getScene()
            with ChangeManager(scene):
                selection_group.addNodesConditional(conditional_field)

            selection_mesh_group.removeAllElements()
            self._selection_updated()

    def _selection_updated(self):
        self._ui_update_selection_dependent_buttons()
        self._surface_selection_updated()

    def _ui_update_selection_dependent_buttons(self, group_selection=None):
        group_selection = self._group_points_ui.pushButtonDeleteGroup.isEnabled() if group_selection is None else group_selection
        node_selection_group = self._get_node_selection_group()
        nodes_selected = node_selection_group is not None and node_selection_group.getSize()
        self._group_points_ui.pushButtonAddToGroup.setEnabled(nodes_selected and group_selection)
        self._group_points_ui.pushButtonRemoveFromGroup.setEnabled(nodes_selected and group_selection)
        self._group_points_ui.pushButtonDeleteGroup.setEnabled(group_selection)
        self._selection_ui.pushButtonInvertSelection.setEnabled(nodes_selected)

    def _surface_selection_updated(self):
        mesh_selection_group = self._get_mesh_selection_group()
        mesh_selected = mesh_selection_group is not None and mesh_selection_group.getSize()
        whole_surfaces = self._selection_ui.comboBoxSelectionType.currentText() == "Whole Surfaces"
        surface_sections = self._selection_ui.comboBoxSelectionType.currentText() == "Surface Sections"
        self._selection_ui.pushButtonSelectPointsOnSurface.setEnabled(mesh_selected and whole_surfaces)
        self._selection_ui.labelTolerance.setEnabled(mesh_selected and whole_surfaces)
        self._selection_ui.doubleSpinBoxTolerance.setEnabled(mesh_selected and whole_surfaces)
        self._selection_ui.pushButtonDeleteSelectedSurfaceSection.setEnabled(mesh_selected and surface_sections)

        if mesh_selected and whole_surfaces:
            self._select_connected_mesh_elements(mesh_selection_group)

    def _update_progress(self, value):
        self._progress_dialog.setValue(value)
        return self._progress_dialog.wasCanceled()

    def _list_ignore_element_identifiers(self):
        identifiers = []
        for i in range(self._selection_ui.comboBoxDeleteSurfaceHistory.currentIndex() + 1):
            item = self._selection_ui.comboBoxDeleteSurfaceHistory.itemData(i)
            identifiers.extend(_element_ids(item))

        return sorted(identifiers)

    def _select_connected_mesh_elements(self, mesh_selection_group):
        coordinate_field = self._model.get_mesh_coordinates()
        field_module = coordinate_field.getFieldmodule()

        if len(self._connected_sets) == 0:
            mesh = self._model.get_mesh()
            element_count = mesh.getSize()
            identifiers = self._list_ignore_element_identifiers()

            self._progress_dialog = self._prepare_progress_dialog("Finding connected surfaces", "Cancel", element_count)
            connected_sets = find_connected_mesh_elements_0d(coordinate_field, mesh.getDimension(),
                                                             ignore_elements=set(identifiers),
                                                             progress_callback=self._update_progress)
            self._progress_dialog.setValue(element_count)
            if connected_sets is None:
                return

            self._connected_sets = connected_sets

        initial_element = mesh_selection_group.createElementiterator().next()
        initial_element_identifier = initial_element.getIdentifier()
        selected_elements = [_set for _set in self._connected_sets if initial_element_identifier in _set]
        if selected_elements:
            _select_elements(field_module, mesh_selection_group, selected_elements[0])

    def _delete_selected_surfaces(self):
        for i in range(self._selection_ui.comboBoxDeleteSurfaceHistory.count() - 1,
                       self._selection_ui.comboBoxDeleteSurfaceHistory.currentIndex(), -1):
            self._selection_ui.comboBoxDeleteSurfaceHistory.removeItem(i)

        scene = self._ui.widgetZinc.get_zinc_sceneviewer().getScene()
        selection_field = scene_get_or_create_selection_group(scene)
        self._update_delete_field_function(selection_field)
        scene.getSelectionField().castGroup().clear()
        self._surface_selection_updated()
        self._update_delete_field_function_2()
        self._connected_sets = []
        self._model.reset_connected_set_index_field()

    def _create_element_group_from_identifiers(self, identifiers):
        surface_mesh = self._model.get_mesh()
        field_module = surface_mesh.getFieldmodule()
        with ChangeManager(field_module):
            field_group = field_module.createFieldGroup()
            mesh_group = field_group.createMeshGroup(surface_mesh)
            for identifier in identifiers:
                mesh_group.addElement(surface_mesh.findElementByIdentifier(identifier))

        return mesh_group

    def _update_delete_field_function(self, element_field_group):
        surface_mesh = self._model.get_mesh()
        field_module = surface_mesh.getFieldmodule()
        surface_region = field_module.getRegion()
        with ChangeManager(surface_region):
            surface_mesh_group = element_field_group.getSubregionFieldGroup(surface_region)
            delete_group = field_module.createFieldGroup()
            delete_mesh_group = delete_group.createMeshGroup(surface_mesh)
            delete_mesh_group.addElementsConditional(surface_mesh_group)
            self._selection_ui.comboBoxDeleteSurfaceHistory.blockSignals(True)
            self._selection_ui.comboBoxDeleteSurfaceHistory.addItem(f"Size: {delete_mesh_group.getSize()}",
                                                                    delete_mesh_group)
            self._selection_ui.comboBoxDeleteSurfaceHistory.setCurrentIndex(
                self._selection_ui.comboBoxDeleteSurfaceHistory.count() - 1)
            self._selection_ui.comboBoxDeleteSurfaceHistory.blockSignals(False)

    def _update_delete_field_function_2(self):
        surface_mesh = self._model.get_mesh()
        field_module = surface_mesh.getFieldmodule()
        with ChangeManager(field_module):
            all_delete_groups = field_module.createFieldGroup()
            for i in range(self._selection_ui.comboBoxDeleteSurfaceHistory.currentIndex() + 1):
                item_data = self._selection_ui.comboBoxDeleteSurfaceHistory.itemData(i)
                element_field_group = item_data.getFieldGroup()
                all_delete_groups = field_module.createFieldOr(all_delete_groups, element_field_group)

            not_field = field_module.createFieldNot(all_delete_groups)

            self._scene.set_surface_graphics_subgroup_field(not_field)

    def _delete_surface_history_index_changed(self, index):
        self._update_delete_field_function_2()
        self._model.reset_connected_set_index_field()

    def _invert_selection_clicked(self):
        points_region = self._model.get_points_region()
        scene = points_region.getScene()
        selection_field = scene.getSelectionField().castGroup()
        field_module = points_region.getFieldmodule()
        with ChangeManager(field_module):
            with ChangeManager(scene):
                new_selection_field = field_module.createFieldGroup()
                not_field = field_module.createFieldNot(new_selection_field)
                new_selection_group = new_selection_field.createNodesetGroup(self._model.get_data_points())
                new_selection_group.addNodesConditional(selection_field)

                selection_field.clear()
                selection_field_group = selection_field.getOrCreateNodesetGroup(self._model.get_data_points())
                selection_field_group.addNodesConditional(not_field)

    def _add_elements_to_group(self, element_group):
        # Add the selected Elements to a Group.
        scene = self._field_module.getRegion().getScene()
        selection_group = scene.getSelectionField().castGroup()
        selected_nodeset_group = self._get_node_selection_group()
        with ChangeManager(scene):
            node_iter = selected_nodeset_group.createNodeiterator()
            node = node_iter.next()
            while node.isValid():
                element_group.addNode(node)
                node = node_iter.next()
            selection_group.clear()

        # print(identifiers)

    def _get_node_selection_group(self):
        scene = self._ui.widgetZinc.get_zinc_sceneviewer().getScene()
        selection_field = scene_get_or_create_selection_group(scene)
        return selection_field.getOrCreateNodesetGroup(self._model.get_data_points())

    def _get_mesh_selection_group(self):
        scene = self._ui.widgetZinc.get_zinc_sceneviewer().getScene()
        selection_field = scene_get_or_create_selection_group(scene)
        return selection_field.getMeshGroup(self._model.get_mesh())

    def _update_label_text(self):
        handler_label_map = {SceneManipulation: "Mode: View", CustomSceneSelection: "Mode: Selection"}
        handler_label = handler_label_map[type(self._ui.widgetZinc.active_handler())]
        self._scene.update_label_text(handler_label)

    def register_done_execution(self, done_execution):
        self._callback = done_execution

    def _zinc_widget_ready(self):
        self._ui.widgetZinc.set_selection_filter(self._model.get_selection_filter())
        self._ui_update_selection_dependent_buttons()

    def _pixel_scale_changed(self, scale):
        self._scene.set_pixel_scale(scale)

    def _view_all_button_clicked(self):
        self._ui.widgetZinc.view_all()

    def _standard_views_button_clicked(self):
        rotate_to_next_standard_view(self._ui.widgetZinc.get_zinc_sceneviewer())

    def _continue_execution(self):
        self._save_settings()
        self._remove_ui_region()
        self._clear_selection_group()
        self._write()
        self._callback()

    def _remove_ui_region(self):
        self._model.remove_label_region()

    def _clear_selection_group(self):
        scene = self._model.get_points_region().getScene()
        selection_field = scene.getSelectionField().castGroup()
        selection_field.clear()

    def _load_settings(self):
        if os.path.isfile(self._settings_file()):
            with open(self._settings_file()) as f:
                settings = json.load(f)

            if "point_size" in settings:
                self._display_settings_ui.pointSizeSpinBox.setValue(settings["point_size"])
            if "tolerance" in settings:
                self._selection_ui.doubleSpinBoxTolerance.setValue(settings["tolerance"])

            return settings["input_hash"] if "input_hash" in settings else None

    def _load_deleted_surfaces(self):
        if os.path.isfile(self._settings_file()):
            with open(self._settings_file()) as f:
                settings = json.load(f)

            mesh_group = self._create_element_group_from_identifiers([])

            self._selection_ui.comboBoxDeleteSurfaceHistory.blockSignals(True)
            self._selection_ui.comboBoxDeleteSurfaceHistory.clear()
            self._selection_ui.comboBoxDeleteSurfaceHistory.addItem(f"--", mesh_group)

            if "deleted_surfaces" in settings:
                deleted_surfaces = settings["deleted_surfaces"]
                for deleted_surface in deleted_surfaces:
                    mesh_group = self._create_element_group_from_identifiers(deleted_surface)
                    self._selection_ui.comboBoxDeleteSurfaceHistory.addItem(f"Size: {mesh_group.getSize()}", mesh_group)

            self._selection_ui.comboBoxDeleteSurfaceHistory.setCurrentIndex(
                self._selection_ui.comboBoxDeleteSurfaceHistory.count() - 1)
            self._update_delete_field_function_2()
            self._selection_ui.comboBoxDeleteSurfaceHistory.blockSignals(False)

    def _save_settings(self):
        if not os.path.exists(self._location):
            os.makedirs(self._location)

        deleted_surfaces = []
        for i in range(1, self._selection_ui.comboBoxDeleteSurfaceHistory.currentIndex() + 1):
            item = self._selection_ui.comboBoxDeleteSurfaceHistory.itemData(i)
            deleted_surfaces.append(_element_ids(item))

        settings = {
            "input_hash": self._input_hash,
            "point_size": self._display_settings_ui.pointSizeSpinBox.value(),
            "tolerance": self._selection_ui.doubleSpinBoxTolerance.value(),
            "deleted_surfaces": deleted_surfaces,
        }

        with open(self._settings_file(), "w") as f:
            json.dump(settings, f)


class GroupSelectionDialog(QtWidgets.QDialog):
    def __init__(self, parent, group_names):
        super().__init__(parent)

        self.setMinimumSize(300, 200)
        self.setWindowTitle("Select Point Group")

        buttons = QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        self.button_box = QtWidgets.QDialogButtonBox(buttons)
        self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.buttonClicked.connect(self._enable_button)

        message = QtWidgets.QLabel("Please select a group:")
        self.layout.addWidget(message)

        for group_name in group_names:
            check_box = QtWidgets.QCheckBox(group_name)
            self.button_group.addButton(check_box)
            self.layout.addWidget(check_box)

        self.layout.addStretch()
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def _enable_button(self):
        self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setEnabled(True)

    def get_group_name(self):
        return self.button_group.checkedButton().text()


def _find_datapoint_location(mesh_cache, conditional_field, find_host_coordinates, datapoint):
    mesh_cache.setNode(datapoint)
    element, xi = find_host_coordinates.evaluateMeshLocation(mesh_cache, 2)
    _, value = conditional_field.evaluateReal(mesh_cache, 1)
    return element.getIdentifier(), value
