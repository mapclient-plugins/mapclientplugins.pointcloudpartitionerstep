"""
Created: April, 2023

@author: tsalemink
"""
import colorsys
import os
import json

from PySide6 import QtWidgets, QtCore

from cmlibs.zinc.field import Field, FieldFindMeshLocation
from cmlibs.zinc.result import RESULT_OK
from cmlibs.zinc.material import Material
from cmlibs.utils.zinc.general import ChangeManager
from cmlibs.widgets.definitions import SELECTION_GROUP_NAME
from cmlibs.widgets.handlers.scenemanipulation import SceneManipulation

from mapclientplugins.pointcloudpartitionerstep.view.ui_pointcloudpartitionerwidget import Ui_PointCloudPartitionerWidget
from mapclientplugins.pointcloudpartitionerstep.scene.pointcloudpartitionerscene import PointCloudPartitionerScene
from mapclientplugins.pointcloudpartitionerstep.view.customsceneselection import CustomSceneSelection, MODE_MAP, TYPE_MAP

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''


def _get_or_create_selection_field(field_module):
    selection_field = field_module.findFieldByName(SELECTION_GROUP_NAME)
    if selection_field.isValid():
        selection_field = selection_field.castGroup()
    if not selection_field.isValid():
        selection_field = field_module.createFieldGroup()
        selection_field.setName(SELECTION_GROUP_NAME)

    region = field_module.getRegion()
    region.getScene().setSelectionField(selection_field)

    return selection_field


class PointCloudPartitionerWidget(QtWidgets.QWidget):

    def __init__(self, model, parent=None):
        super(PointCloudPartitionerWidget, self).__init__(parent)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self._ui = Ui_PointCloudPartitionerWidget()
        self._ui.setupUi(self)

        self._callback = None
        self._location = None

        self._model = model
        self._scene = PointCloudPartitionerScene(model)
        self._selection_handler = CustomSceneSelection(QtCore.Qt.Key.Key_S)
        self._field_module = None
        self._stored_mesh_location_field = None
        self._points_field_list = ["---"]
        self._surfaces_field_list = ["---"]
        self._connected_sets = []

        self._check_box_dict = {}  # Key is LineEdit, value is CheckBox.
        self._horizontal_layout_dict = {}  # Key is CheckBox, value is Layout
        self._point_group_dict = {}  # Key is CheckBox, value is Group.
        self._rgb_dict = {}  # Key is CheckBox, value is RGB-Value.
        self._button_group = QtWidgets.QButtonGroup()

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
        self._ui.pushButtonContinue.clicked.connect(self._continue_execution)
        self._ui.pushButtonViewAll.clicked.connect(self._view_all_button_clicked)
        self._ui.widgetZinc.graphics_initialized.connect(self._zinc_widget_ready)
        self._ui.widgetZinc.pixel_scale_changed.connect(self._pixel_scale_changed)
        self._ui.pushButtonCreateGroup.clicked.connect(self._create_point_group)
        self._ui.pushButtonRemoveGroup.clicked.connect(self._remove_current_point_group)
        self._ui.pushButtonAddToGroup.clicked.connect(self._add_points_to_group)
        self._ui.pushButtonRemoveFromGroup.clicked.connect(self._remove_selected_points_from_group)
        self._ui.pointsFieldComboBox.textActivated.connect(self._update_point_cloud_field)
        self._ui.meshFieldComboBox.textActivated.connect(self._update_mesh_field)
        self._ui.comboBoxSelectionMode.currentIndexChanged.connect(self._update_selection_mode)
        self._ui.comboBoxSelectionType.currentIndexChanged.connect(self._update_selection_type)
        self._ui.pushButtonSelectPointsOnSurface.clicked.connect(self._select_points_on_surface)
        self._ui.checkBoxSurfacesVisibility.stateChanged.connect(self._scene.set_surfaces_visibility)
        self._ui.checkBoxPointsVisibility.stateChanged.connect(self._scene.set_points_visibility)
        self._ui.pointSizeSpinBox.valueChanged.connect(self._scene.set_point_size)
        self._ui.widgetZinc.handler_updated.connect(self._update_label_text)
        self._ui.widgetZinc.selection_updated.connect(self._update_surface_selection)

    def _setup_field_combo_boxes(self):
        self._ui.pointsFieldComboBox.addItems(self._points_field_list)
        if self._ui.pointsFieldComboBox.count() == 2:
            self._ui.pointsFieldComboBox.setCurrentIndex(1)
            self._update_point_cloud_field()

        self._ui.meshFieldComboBox.addItems(self._surfaces_field_list)
        if self._ui.meshFieldComboBox.count() == 2:
            self._ui.meshFieldComboBox.setCurrentIndex(1)
            self._update_mesh_field()

    def _update_point_cloud_field(self):
        self._model.update_point_cloud_coordinates(self._ui.pointsFieldComboBox.currentText())
        self._scene.update_point_cloud_coordinates()
        # self._ui.widgetZinc.view_all()

    def _update_mesh_field(self):
        self._model.update_mesh_coordinates(self._ui.meshFieldComboBox.currentText())
        self._scene.update_mesh_coordinates()
        # self._ui.widgetZinc.view_all()

    def _setup_selection_mode_combo_box(self):
        self._ui.comboBoxSelectionMode.addItems(MODE_MAP.keys())
        self._update_selection_mode()

    def _setup_selection_type_combo_box(self):
        self._ui.comboBoxSelectionType.addItems(TYPE_MAP.keys())
        self._update_selection_type()

    def _setup_point_size_spin_box(self):
        self._ui.pointSizeSpinBox.setValue(self._scene.get_point_size())

    def load(self, points_file_location, surfaces_file_location):
        self._model.load(points_file_location, surfaces_file_location)
        self._scene.setup_visualisation()

        self._get_points_fields(self._model.get_points_region(), self._points_field_list)
        self._get_surfaces_fields(self._model.get_surfaces_region(), self._surfaces_field_list)
        self._update_node_graphics_subgroup()
        self._setup_field_combo_boxes()

    def _get_points_fields(self, region, field_list):
        self._field_module = region.getFieldmodule()
        self._get_fields(self._field_module, field_list, True)

    def _get_surfaces_fields(self, region, field_list):
        field_module = region.getFieldmodule()
        self._get_fields(field_module, field_list, False)

    def _get_fields(self, field_module, field_list, include_nodes):
        field_iter = field_module.createFielditerator()
        field = field_iter.next()
        node_points = field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        while field.isValid():
            if field.isTypeCoordinate() and (field.getNumberOfComponents() == 3) and (field.castFiniteElement().isValid()):
                field_list.append(field.getName())
            node_group = field.castGroup()
            if include_nodes and node_group.isValid():
                field_node_group = node_group.getFieldNodeGroup(node_points)
                nodeset_group = field_node_group.getNodesetGroup()
                if nodeset_group.isValid():
                    self._add_point_group(node_group)
            field = field_iter.next()

    def clear(self):
        buttons = self._button_group.buttons()
        for button in buttons:
            self._remove_point_group(button)

        self._update_node_graphics_subgroup()

    def set_location(self, location):
        self._location = location

    def get_output_file(self):
        return os.path.join(self._location, "nodes-with-groups.exf")

    def _settings_file(self):
        return os.path.join(self._location, 'settings.json')

    def _write(self):
        if not os.path.exists(self._location):
            os.makedirs(self._location)

        self._model.get_points_region().writeFile(self.get_output_file())

    def _create_group_line_edit(self, name=None):
        next_name = self._next_available_name(name)
        line_edit = QtWidgets.QLineEdit(next_name)
        line_edit.editingFinished.connect(self._validate_line_edit)
        line_edit.editingFinished.connect(self._group_name_changed)
        return line_edit

    def _next_available_name(self, name):
        i = 1
        names = [e.text() for e in self._check_box_dict.keys()]
        stem_name = "Group"
        unique_name = f"{stem_name}_1" if name is None else name
        name = stem_name if name is None else name

        while unique_name in names:
            unique_name = f"{name}_{i}"
            i += 1

        return unique_name

    def _line_edit_is_unique(self, line_edit):
        for value in self._check_box_dict.keys():
            if value.text() == line_edit.text() and value is not line_edit:
                return False
        return True

    def _validate_line_edit(self):
        line_edit = self.sender()
        if self._line_edit_is_unique(line_edit):
            line_edit.setStyleSheet(DEFAULT_STYLE_SHEET)
            line_edit.setToolTip("")
        else:
            line_edit.setStyleSheet(INVALID_STYLE_SHEET)
            line_edit.setToolTip("Warning: group identifier is a duplicate.")

    def _group_name_changed(self):
        line_edit = self.sender()
        check_box = self._check_box_dict[line_edit]
        group = self._point_group_dict[check_box]
        old_name = group.getName()
        new_name = line_edit.text()
        group.setName(new_name)
        self._scene.update_graphics_name(old_name, new_name)

    def check_box_pressed(self):
        if self.sender().isChecked():
            self.sender().group().setExclusive(False)

    def check_box_released(self):
        if self.sender().isChecked():
            self.sender().setChecked(False)
        self.sender().group().setExclusive(True)

    def _create_check_box(self):
        check_box = QtWidgets.QCheckBox()
        check_box.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        check_box.setChecked(True)
        check_box.pressed.connect(self.check_box_pressed)
        check_box.released.connect(self.check_box_released)
        self._button_group.addButton(check_box)
        return check_box

    def _group_button_clicked(self):
        print(self.sender())
        print(self.sender().parent())
        print(self.sender().text())
        print(self.sender().parent().name())
        # print(self._horizontal_layout_dict[self.sender().layout()])

    def _create_button(self, label):
        button = QtWidgets.QPushButton(label)
        button.clicked.connect(self._group_button_clicked)
        return button

    def _layout_point_group(self, widgets):
        horizontal_layout = QtWidgets.QHBoxLayout()
        for widget in widgets:
            horizontal_layout.addWidget(widget)
        self._ui.verticalLayout_5.addLayout(horizontal_layout)
        return horizontal_layout

    def _add_point_group(self, group=None):
        line_edit = self._create_group_line_edit(group.getName() if group is not None else None)
        check_box = self._create_check_box()
        sel_button = self._create_button("sel.")
        del_button = self._create_button("del.")
        horizontal_layout = self._layout_point_group([check_box, line_edit, sel_button, del_button])

        if group is None:
            group = self._field_module.createFieldGroup()
            group.setName(line_edit.text())

        self._register_point_group(group, line_edit, check_box, horizontal_layout)

    def _create_point_group(self):
        self._add_point_group()
        self._update_node_graphics_subgroup()

    def _register_point_group(self, group, line_edit, check_box, horizontal_layout):
        self._check_box_dict[line_edit] = check_box
        self._horizontal_layout_dict[check_box] = horizontal_layout
        self._point_group_dict[check_box] = group
        self._rgb_dict[check_box] = None
        self._update_color_map()
        self._scene.update_graphics_materials(self._rgb_dict)
        material = self._rgb_dict[check_box]
        self._scene.create_point_graphics(self._model.get_points_region().getScene(), self._model.get_point_cloud_coordinates(), group, material)

    def _update_node_graphics_subgroup(self):
        only_one_group = None
        multiple_groups = None
        for group in self._point_group_dict.values():
            if only_one_group is None and multiple_groups is None:
                only_one_group = self._field_module.createFieldNot(group)
                multiple_groups = group
            else:
                only_one_group = None
                multiple_groups = self._field_module.createFieldOr(group, multiple_groups)

        if only_one_group is None and multiple_groups is None:
            self._scene.set_node_graphics_subgroup_field(None)
        elif only_one_group is None:
            self._scene.set_node_graphics_subgroup_field(self._field_module.createFieldNot(multiple_groups))
        else:
            self._scene.set_node_graphics_subgroup_field(only_one_group)

    def _remove_current_point_group(self):
        checked_button = self._get_checked_button()
        self._remove_points_from_group(checked_button)
        self._remove_point_group(checked_button)
        self._update_node_graphics_subgroup()

    def _remove_point_group(self, checked_button):
        group_name = self._point_group_dict[checked_button].getName()
        # Schedule the group for deletion.
        self._point_group_dict[checked_button].setManaged(False)
        # Remove UI elements.
        horizontal_layout = self._horizontal_layout_dict[checked_button]
        for i in reversed(range(horizontal_layout.count())):
            horizontal_layout.itemAt(i).widget().deleteLater()
        horizontal_layout.deleteLater()

        # Remove dictionary entries.
        del self._rgb_dict[checked_button]
        del self._point_group_dict[checked_button]
        del self._horizontal_layout_dict[checked_button]
        for key in self._check_box_dict.keys():
            if self._check_box_dict[key] is checked_button:
                del self._check_box_dict[key]
                break

        # Update the scene.
        self._update_color_map()
        self._scene.update_graphics_materials(self._rgb_dict)
        self._scene.delete_point_graphics(group_name)

    def _update_color_map(self):
        def get_distinct_colors(n):
            hue_partition = 1.0 / (n + 1)
            return [list(colorsys.hsv_to_rgb(hue_partition * value, 1.0, 1.0)) for value in range(0, n)]

        material_module = self._model.get_points_region().getScene().getMaterialmodule()
        colors = get_distinct_colors(len(self._rgb_dict) + 1)
        colors.pop(0)
        for i in range(len(colors)):
            material = material_module.createMaterial()
            material.setManaged(True)
            material.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, colors[i])
            material.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, colors[i])
            material.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [0.1, 0.1, 0.1])
            self._rgb_dict[list(self._rgb_dict.keys())[i]] = material

    def _add_points_to_group(self):
        selection_field = self._field_module.findFieldByName(SELECTION_GROUP_NAME).castGroup()
        selected_nodeset_group = self._get_node_selection_group()
        checked_group = self._get_checked_group()
        nodeset_group = self._get_checked_nodeset_group(checked_group)
        if not nodeset_group.isValid():
            return

        # Add the selected Nodes to the chosen Group.
        scene = self._field_module.getRegion().getScene()
        with ChangeManager(scene):
            node_iter = selected_nodeset_group.createNodeiterator()
            node = node_iter.next()
            while node.isValid():
                nodeset_group.addNode(node)
                node = node_iter.next()

            selection_field.clear()

    def _remove_selected_points_from_group(self):
        selection_field = self._field_module.findFieldByName(SELECTION_GROUP_NAME).castGroup()
        selected_nodeset_group = self._get_node_selection_group()
        checked_button = self._get_checked_button()
        self._remove_points_from_group(checked_button, selection_field, selected_nodeset_group)

    def _remove_points_from_group(self, checked_button, field_group=None, selected_nodeset_group=None):
        checked_group = self._point_group_dict.get(checked_button, None)
        nodeset_group = self._get_checked_nodeset_group(checked_group)
        if not nodeset_group:
            return

        # If the method was called without a selection group, remove all nodes.
        if field_group is None or selected_nodeset_group is None:
            field_group = checked_group
            selected_nodeset_group = nodeset_group

        # Remove the selected Nodes from the chosen group.
        node_iter = selected_nodeset_group.createNodeiterator()
        node = node_iter.next()
        while node.isValid():
            nodeset_group.removeNode(node)
            node = node_iter.next()
        field_group.clear()

    def _update_selection_mode(self):
        mode = MODE_MAP[self._ui.comboBoxSelectionMode.currentText()]
        self._selection_handler.set_primary_selection_mode(mode)

    def _update_selection_type(self):
        scene_filter_module = self._model.get_context().getScenefiltermodule()
        selection_type = TYPE_MAP[self._ui.comboBoxSelectionType.currentText()]
        scene_filter = scene_filter_module.createScenefilterFieldDomainType(selection_type)
        self._selection_handler.set_scene_filter(scene_filter)

    def _select_points_on_surface(self):
        point_coordinate_field = self._model.get_point_cloud_coordinates()
        mesh_coordinate_field = self._model.get_mesh_coordinates()
        selection_mesh_group = self._get_mesh_selection_group()

        client_field_module = point_coordinate_field.getFieldmodule()
        host_field_module = mesh_coordinate_field.getFieldmodule()
        # root_region = self._model.get_context().getDefaultRegion()
        with ChangeManager(host_field_module):
            with ChangeManager(client_field_module):
                coordinate_arg = host_field_module.createFieldArgumentReal(3)
                find_host_coordinates = host_field_module.createFieldFindMeshLocation(coordinate_arg, mesh_coordinate_field, selection_mesh_group)
                find_host_coordinates.setSearchMode(FieldFindMeshLocation.SEARCH_MODE_NEAREST)
                host_coordinates = host_field_module.createFieldEmbedded(mesh_coordinate_field, find_host_coordinates)

                apply_host_coordinates = client_field_module.createFieldApply(host_coordinates)
                apply_host_coordinates.setBindArgumentSourceField(coordinate_arg, point_coordinate_field)

                self._data_projection_delta_coordinate_field = client_field_module.createFieldSubtract(
                    point_coordinate_field,
                    apply_host_coordinates)

                self._data_projection_error_field = client_field_module.createFieldMagnitude(
                    self._data_projection_delta_coordinate_field)
                tolerance_field = client_field_module.createFieldConstant(0.00001)

                conditional_field = client_field_module.createFieldLessThan(self._data_projection_error_field, tolerance_field)

                selection_group = self._get_node_selection_group()
                selection_group.addNodesConditional(conditional_field)

        selection_mesh_group.removeAllElements()
        self._ui.pushButtonSelectPointsOnSurface.setEnabled(False)

    def _update_surface_selection(self):
        mesh_selection_group = self._get_mesh_selection_group()
        mesh_selected = True if mesh_selection_group.getSize() else False
        self._ui.pushButtonSelectPointsOnSurface.setEnabled(mesh_selected)

        if mesh_selection_group:
            self._select_connected_mesh_elements(mesh_selection_group)

    def _select_elements(self, field_module, mesh_selection_group, element_identifiers):
        region = field_module.getRegion()
        mesh = mesh_selection_group.getMasterMesh()

        scene = region.getScene()
        with ChangeManager(scene):
            for element_identifier in element_identifiers:
                mesh_selection_group.addElement(mesh.findElementByIdentifier(element_identifier))

    def _select_connected_mesh_elements(self, mesh_selection_group):
        coordinate_field = self._model.get_mesh_coordinates()
        field_module = coordinate_field.getFieldmodule()
        initial_element = mesh_selection_group.createElementiterator().next()
        initial_element_identifier = initial_element.getIdentifier()
        if len(self._connected_sets):
            selected_elements = [_set for _set in self._connected_sets if initial_element_identifier in _set]
            if selected_elements:
                self._select_elements(field_module, mesh_selection_group, selected_elements[0])
            return

        mesh = mesh_selection_group.getMasterMesh()
        element_iterator = mesh.createElementiterator()
        element = element_iterator.next()
        element_nodes = []
        element_identifiers = []
        while element.isValid():
            element_identifiers.append(element.getIdentifier())
            eft = element.getElementfieldtemplate(coordinate_field, -1)
            local_node_count = eft.getNumberOfLocalNodes()
            node_identifiers = []
            for index in range(local_node_count):
                node = element.getNode(eft, index + 1)
                node_identifiers.append(node.getIdentifier())

            element_nodes.append(node_identifiers)
            element = element_iterator.next()

        initial_element_index = element_identifiers.index(initial_element_identifier)
        connected_sets = _find_connected(initial_element_index, element_nodes)

        el_ids = []
        for connected_set in connected_sets:
            ids = []
            for index in connected_set:
                ids.append(element_identifiers[index])

            el_ids.append(ids)

        self._connected_sets = el_ids
        self._select_elements(field_module, mesh_selection_group, el_ids[0])

    def _get_node_selection_group(self):
        region = self._model.get_points_region()
        selection_field = _get_or_create_selection_field(region.getFieldmodule())

        selection_node_group = selection_field.getFieldNodeGroup(self._model.get_nodes())
        if not selection_node_group.isValid():
            selection_node_group = selection_field.createFieldNodeGroup(self._model.get_nodes())

        return selection_node_group.getNodesetGroup()

    def _get_mesh_selection_group(self):
        mesh = self._model.get_mesh()
        region = self._model.get_surfaces_region()
        selection_field = _get_or_create_selection_field(region.getFieldmodule())
        selection_element_group = selection_field.getFieldElementGroup(mesh)

        return selection_element_group.getMeshGroup()

    def _get_checked_group(self):
        checked_button = self._get_checked_button()
        return self._point_group_dict.get(checked_button, None)

    def _get_checked_nodeset_group(self, checked_group):
        if checked_group is None:
            return None

        field_node_group = checked_group.getFieldNodeGroup(self._model.get_nodes())
        if not field_node_group.isValid():
            field_node_group = checked_group.createFieldNodeGroup(self._model.get_nodes())

        return field_node_group.getNodesetGroup()

    def _get_checked_button(self):
        checked_button = self._button_group.checkedButton()

        if len(self._point_group_dict) == 0:
            QtWidgets.QMessageBox.information(self, 'No Point Group Created', 'No point group created. Please create a point group first '
                                                                              'before attempting to add points.', QtWidgets.QMessageBox.StandardButton.Ok)
            return None
        elif not checked_button:
            dlg = GroupSelectionDialog(self, self._check_box_dict.keys())
            if dlg.exec_():
                checked_button = self._check_box_dict[dlg.get_line_edit()]
            else:
                return None

        return checked_button

    def _update_label_text(self):
        handler_label_map = {SceneManipulation: "Mode: View", CustomSceneSelection: "Mode: Selection"}
        handler_label = handler_label_map[type(self._ui.widgetZinc.get_active_handler())]
        self._scene.update_label_text(handler_label)

    def register_done_execution(self, done_execution):
        self._callback = done_execution

    def _zinc_widget_ready(self):
        self._ui.widgetZinc.set_selectionfilter(self._model.get_selection_filter())

    def _pixel_scale_changed(self, scale):
        self._scene.set_pixel_scale(scale)

    def _view_all_button_clicked(self):
        self._ui.widgetZinc.view_all()

    def _continue_execution(self):
        self._save_settings()
        self._remove_ui_region()
        self._update_group_names()
        self._clear_selection_group()
        self._write()
        self._callback()

    def _remove_ui_region(self):
        self._model.remove_label_region()

    def _update_group_names(self):
        for line_edit in self._check_box_dict.keys():
            check_box = self._check_box_dict[line_edit]
            group = self._point_group_dict[check_box]
            group.setName(line_edit.text())

    def _clear_selection_group(self):
        selection_field = self._field_module.findFieldByName(SELECTION_GROUP_NAME).castGroup()
        selection_field.clear()

    def load_settings(self):
        if os.path.isfile(self._settings_file()):
            with open(self._settings_file()) as f:
                settings = json.load(f)

            if "point_size" in settings:
                self._ui.pointSizeSpinBox.setValue(settings["point_size"])

    def _save_settings(self):
        if not os.path.exists(self._location):
            os.makedirs(self._location)

        settings = {
            "point_size": self._ui.pointSizeSpinBox.value()
        }

        with open(self._settings_file(), "w") as f:
            json.dump(settings, f)


class GroupSelectionDialog(QtWidgets.QDialog):
    def __init__(self, parent, line_edits):
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

        self.line_edit_dict = {}
        for line_edit in line_edits:
            text = line_edit.text()
            check_box = QtWidgets.QCheckBox(text)
            self.button_group.addButton(check_box)
            self.layout.addWidget(check_box)
            self.line_edit_dict[text] = line_edit

        self.layout.addStretch()
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def _enable_button(self):
        self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setEnabled(True)

    def get_line_edit(self):
        return self.line_edit_dict[self.button_group.checkedButton().text()]


def _find_connected(initial_triangle_index, triangles):
    connected_triangles = [[initial_triangle_index]]
    connected_nodes = [set(triangles[initial_triangle_index])]
    for triangle_index, triangle in enumerate(triangles):
        if triangle_index == initial_triangle_index:
            continue

        connected_triangles.append([triangle_index])
        connected_nodes.append(set(triangles[triangle_index]))

        index = 0
        while index < len(connected_triangles):
            connection_found = False
            next_index = index + 1
            base_connected_node_set = connected_nodes[index]
            while next_index < len(connected_triangles):
                current_connected_node_set = connected_nodes[next_index]
                intersection = base_connected_node_set.intersection(current_connected_node_set)
                if len(intersection):
                    connection_found = True
                    connected_triangles[index].extend(connected_triangles[next_index])
                    connected_nodes[index].update(connected_nodes[next_index])
                    del connected_triangles[next_index]
                    del connected_nodes[next_index]
                    index = 0
                    # next_index = 0
                else:
                    next_index += 1

            if not connection_found:
                index += 1

    return connected_triangles
