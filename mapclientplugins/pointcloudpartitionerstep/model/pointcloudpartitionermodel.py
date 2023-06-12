"""
Created: April, 2023

@author: tsalemink
"""
from cmlibs.zinc.context import Context


class PointCloudPartitionerModel(object):

    def __init__(self):
        self._point_cloud_coordinates_field = None
        self._mesh_coordinates_field = None
        self._point_cloud_nodes = None
        self._selection_group = None
        self._mesh = None

        self._context = Context("PointCloudPartitioner")
        root_region = self._context.getDefaultRegion()
        self._points_region = root_region.createChild("points")
        self._label_region = root_region.createChild("label")
        self._surfaces_region = root_region.createChild("surfaces")

        self.define_standard_materials()
        self.define_standard_glyphs()

        self._selection_filter = self._create_selection_filter()

    def get_selection_filter(self):
        return self._selection_filter

    def load(self, points_file_location, surface_segmentation_file_location):
        self._points_region.readFile(points_file_location)

        if surface_segmentation_file_location is not None:
            self._surfaces_region.readFile(surface_segmentation_file_location)

        points_field_module = self._points_region.getFieldmodule()
        nodes = points_field_module.findNodesetByName("nodes")
        point_cloud_group_field = points_field_module.createFieldNodeGroup(nodes)
        self._point_cloud_nodes = point_cloud_group_field.getNodesetGroup()

        surface_segmentation_field_module = self._surfaces_region.getFieldmodule()
        self._mesh = surface_segmentation_field_module.findMeshByDimension(2)

    def get_context(self):
        return self._context

    def get_point_cloud_coordinates(self):
        return self._point_cloud_coordinates_field

    def update_point_cloud_coordinates(self, field_name):
        points_field_module = self._points_region.getFieldmodule()
        self._point_cloud_coordinates_field = points_field_module.findFieldByName(field_name)
        self._point_cloud_nodes.removeAllNodes()
        self._point_cloud_nodes.addNodesConditional(self._point_cloud_coordinates_field)

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

    def get_nodes(self):
        return self._point_cloud_nodes

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
