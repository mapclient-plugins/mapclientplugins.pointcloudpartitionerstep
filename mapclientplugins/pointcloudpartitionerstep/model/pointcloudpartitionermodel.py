"""
Created: April, 2023

@author: tsalemink
"""
import math

from cmlibs.maths.octree import VolumeOctree
from cmlibs.maths.vectorops import sub, dot, cross
from cmlibs.utils.zinc.general import ChangeManager
from cmlibs.utils.zinc.region import convert_nodes_to_datapoints
from cmlibs.utils.zinc.scene import scene_create_selection_group
from cmlibs.zinc.context import Context
from cmlibs.zinc.field import Field
from cmlibs.zinc.result import RESULT_OK
from scaffoldmaker.utils.vector import normalise


class PointCloudPartitionerModel(object):

    def __init__(self):
        self._point_cloud_coordinates_field = None
        self._mesh_coordinates_field = None
        self._point_cloud_data_points = None
        self._point_selection_group = None
        self._connected_set_index_field = None
        self._mesh = None

        self._context = Context("PointCloudPartitioner")
        self._root_region = self._context.getDefaultRegion()
        self._points_region = self._root_region.createChild("points")
        self._label_region = self._root_region.createChild("label")
        self._surfaces_region = self._root_region.createChild("surfaces")

        self.define_standard_materials()
        self.define_standard_glyphs()

        self._selection_filter = self._create_selection_filter()

    def get_root_region(self):
        return self._root_region

    def get_selection_filter(self):
        return self._selection_filter

    def get_connected_set_index_field(self):
        return self._connected_set_index_field

    def reset_connected_set_index_field(self):
        self._connected_set_index_field = None

    def load(self, points_file_location, surface_segmentation_file_location):
        self._points_region.readFile(points_file_location)

        surface_segmentation_field_module = self._surfaces_region.getFieldmodule()
        if surface_segmentation_file_location is not None:
            self._surfaces_region.readFile(surface_segmentation_file_location)
            datapoints = surface_segmentation_field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
            datapoints.destroyAllNodes()

        points_field_module = self._points_region.getFieldmodule()
        self._point_selection_group = scene_create_selection_group(self._points_region.getScene())
        node_datapoints = points_field_module.findNodesetByName("nodes")
        self._point_cloud_data_points = points_field_module.findNodesetByName("datapoints")

        if node_datapoints.getSize() > 0:
            convert_nodes_to_datapoints(self._points_region, self._points_region)

        self._mesh = surface_segmentation_field_module.findMeshByDimension(2)

    def get_context(self):
        return self._context

    def get_point_cloud_coordinates(self):
        return self._point_cloud_coordinates_field

    def update_point_cloud_coordinates(self, field_name):
        points_field_module = self._points_region.getFieldmodule()
        self._point_cloud_coordinates_field = points_field_module.findFieldByName(field_name)
        # self._point_cloud_nodes.removeAllNodes()
        # self._point_cloud_nodes.addNodesConditional(self._point_cloud_coordinates_field)

    def get_mesh_coordinates(self):
        return self._mesh_coordinates_field

    def update_mesh_coordinates(self, field_name):
        surface_segmentation_field_module = self._surfaces_region.getFieldmodule()
        self._mesh_coordinates_field = surface_segmentation_field_module.findFieldByName(field_name)

    def get_points_region(self):
        return self._points_region

    def get_label_region(self):
        return self._label_region

    def get_surfaces_region(self):
        return self._surfaces_region

    def remove_label_region(self):
        root_region = self._context.getDefaultRegion()
        root_region.removeChild(self._label_region)

    def get_point_selection_group(self):
        return self._point_selection_group

    def get_data_points(self):
        return self._point_cloud_data_points

    def get_mesh(self):
        return self._mesh

    def _create_selection_filter(self):
        m = self._context.getScenefiltermodule()
        # r1 = m.createScenefilterRegion(self._detection_model.get_region())
        # r2 = m.createScenefilterRegion(self._marker_model.get_region())
        o = m.createScenefilterOperatorOr()
        # o.appendOperand(r1)
        # o.appendOperand(r2)
        return o

    def define_standard_glyphs(self):
        """
        Helper method to define the standard glyphs
        """
        glyph_module = self._context.getGlyphmodule()
        glyph_module.defineStandardGlyphs()

    def define_standard_materials(self):
        """
        Helper method to define the standard materials.
        """
        material_module = self._context.getMaterialmodule()
        material_module.defineStandardMaterials()

    def determine_point_connected_surface(self, connected_sets, ignore_identifiers, tolerance, progress_bar=None):
        data_points = self.get_data_points()
        point_coordinate_field = self.get_point_cloud_coordinates()
        data_points_identifiers, data_points_location = _get_data_points(data_points, point_coordinate_field)
        num_data_points = len(data_points_location)
        field_module = point_coordinate_field.getFieldmodule()
        with ChangeManager(field_module):
            field_cache = field_module.createFieldcache()
            # nodeset_mean = field_module.createFieldNodesetMean(point_coordinate_field, data_points)
            nodeset_minimum = field_module.createFieldNodesetMinimum(point_coordinate_field, data_points)
            nodeset_maximum = field_module.createFieldNodesetMaximum(point_coordinate_field, data_points)
            # result, mean_point = nodeset_mean.evaluateReal(field_cache, 3)
            result, min_bounding_point = nodeset_minimum.evaluateReal(field_cache, 3)
            result, max_bounding_point = nodeset_maximum.evaluateReal(field_cache, 3)
        element_identifiers, element_points, element_data = _transform_mesh_to_list_form(self._mesh, self.get_mesh_coordinates(), ignore_identifiers, progress_bar)
        if element_identifiers is None:
            return
        num_elements = len(element_identifiers)

        update_indexes = {}
        if progress_bar is not None:
            update_interval = max(1, num_elements // 200)
            update_indexes = set([i for i in range(update_interval)] + [i for i in range(update_interval, num_elements, update_interval)])
            progress_bar.setValue(0)
            progress_bar.setLabelText("Rendering in Octree ...")
            progress_bar.setMaximum(num_elements)

        connected_surface_map = {c: i for i, k in enumerate(connected_sets) for c in k}

        # Populate Octtree.
        bb = [min_bounding_point, max_bounding_point]
        o = VolumeOctree(bb, tolerance)
        for i, t in enumerate(element_points):
            obj = DataObject({
                "identifier": element_identifiers[i],
                "surface": connected_surface_map[element_identifiers[i]],
                "points": t,
            })
            o.insert_object(obj)
            if i in update_indexes:
                progress_bar.setValue(i)
                if progress_bar.wasCanceled():
                    return

        if progress_bar is not None:
            progress_bar.setValue(num_elements)

        if progress_bar is not None:
            update_interval = max(1, num_data_points // 200)
            update_indexes = set([i for i in range(update_interval)] + [i for i in range(update_interval, num_data_points, update_interval)])
            progress_bar.setValue(0)
            progress_bar.setLabelText("Finding data point surface ...")
            progress_bar.setMaximum(num_data_points)

        data_point_surface_map = {}
        count = 0
        for i, p in enumerate(data_points_location):
            found = o.find_object(p)
            count += 1
            if found:
                data_point_surface_map[data_points_identifiers[i]] = found.surface()

            if i in update_indexes:
                progress_bar.setValue(i)
                if progress_bar.wasCanceled():
                    return

        field_module = point_coordinate_field.getFieldmodule()
        with ChangeManager(field_module):
            self._connected_set_index_field = field_module.createFieldFiniteElement(1)

            datapoint_template = data_points.createNodetemplate()
            datapoint_template.defineField(self._connected_set_index_field)

            point_cache = field_module.createFieldcache()
            for identifier in data_points_identifiers:
                if identifier in data_point_surface_map:
                    point_datapoint = data_points.findNodeByIdentifier(identifier)
                    point_datapoint.merge(datapoint_template)
                    point_cache.setNode(point_datapoint)
                    self._connected_set_index_field.assignReal(point_cache, data_point_surface_map[identifier])

        if progress_bar is not None:
            progress_bar.setValue(num_data_points)


def _get_data_points(data_points_group, coordinate_field):
    field_module = coordinate_field.getFieldmodule()
    field_cache = field_module.createFieldcache()
    num_components = coordinate_field.getNumberOfComponents()
    points = []
    identifiers = []
    with ChangeManager(field_module):
        node_iterator = data_points_group.createNodeiterator()
        node = node_iterator.next()
        while node.isValid():
            field_cache.setNode(node)
            result, value = coordinate_field.evaluateReal(field_cache, num_components)
            if result == RESULT_OK:
                identifiers.append(node.getIdentifier())
                points.append(value)
            node = node_iterator.next()

    return identifiers, points


def _transform_mesh_to_list_form(mesh, mesh_field, ignore_identifiers, progress_bar=None):
    element_iterator = mesh.createElementiterator()
    element = element_iterator.next()
    element_data = []
    element_nodes = []
    element_identifiers = []
    identifier_index_map = {}

    field_module = mesh_field.getFieldmodule()

    update_indexes = {}
    if progress_bar is not None:
        field_group = field_module.createFieldGroup()
        mesh_group = field_group.getOrCreateMeshGroup(mesh)
        mesh_group.addElementsConditional(mesh_field)
        num_elements = mesh_group.getSize()
        update_interval = max(1, num_elements // 200)
        update_indexes = set([i for i in range(update_interval)] + [i for i in range(update_interval, num_elements, update_interval)])
        progress_bar.setLabelText("Analysing elements ...")
        progress_bar.setMaximum(num_elements)
        progress_bar.setValue(0)

    field_cache = field_module.createFieldcache()
    num_components = mesh_field.getNumberOfComponents()
    count = 0
    with ChangeManager(field_module):
        while element.isValid():
            element_identifier = element.getIdentifier()
            eft = element.getElementfieldtemplate(mesh_field, -1)
            local_node_count = eft.getNumberOfLocalNodes()
            node_identifiers = []
            for index in range(local_node_count):
                node = element.getNode(eft, index + 1)
                field_cache.setNode(node)
                result, value = mesh_field.evaluateReal(field_cache, num_components)
                if result == RESULT_OK:
                    node_identifiers.append(value)

            identifier_index_map[element_identifier] = len(element_identifiers)
            element_identifiers.append(element_identifier)
            element_nodes.append(node_identifiers)

            if count in update_indexes:
                progress_bar.setValue(count)
                if progress_bar.wasCanceled():
                    return None, None, None
            count += 1
            element = element_iterator.next()

    for ignore_identifier in sorted(ignore_identifiers, reverse=True):
        index = identifier_index_map[ignore_identifier]
        del element_identifiers[index]
        del element_nodes[index]

    return element_identifiers, element_nodes, element_data


class DataObject:

    def __init__(self, data):
        self._data = data

    def identifier(self):
        return self._data["identifier"]

    def points(self):
        return self._data["points"]

    def surface(self):
        return self._data["surface"]

    def distance(self, pt, tol):
        pts = self._data["points"]
        v0 = sub(pts[1], pts[0])
        v1 = sub(pts[2], pts[0])
        n = normalise(cross(v1, v0))
        v2 = sub(pt, pts[0])
        if math.fabs(dot(v2, n)) < tol:
            dot00 = dot(v0, v0)
            dot01 = dot(v0, v1)
            dot02 = dot(v0, v2)
            dot11 = dot(v1, v1)
            dot12 = dot(v1, v2)
            inv_den = 1 / (dot00 * dot11 - dot01 * dot01)
            u = (dot11 * dot02 - dot00 * dot12) * inv_den
            v = (dot00 * dot12 - dot01 * dot02) * inv_den

            if (u >= -tol) and (v >= -tol) and (u + v < (1 + tol)):
                return 0.0

        return math.inf
