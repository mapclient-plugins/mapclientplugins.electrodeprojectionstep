import os
from opencmiss.zinc.context import Context
from opencmiss.zinc.field import Field
from opencmiss.zinc.glyph import Glyph
from opencmiss.zinc.streamregion import StreaminformationRegion

from opencmiss.utils.zinc.general import define_standard_graphics_objects
from opencmiss.utils.zinc.field import create_field_finite_element

from sparc.electrodeprojection.meshprojection import MeshProjection


def _read_region_description(region, region_description):
    stream_information = region.createStreaminformationRegion()
    memory_resource = stream_information.createStreamresourceMemoryBuffer(region_description['elements'])
    stream_information.setResourceDomainTypes(memory_resource, Field.DOMAIN_TYPE_MESH3D)

    for key in region_description:
        if key != 'elements':
            if isinstance(key, float):
                time = key
            else:
                time = float(key)

            memory_resource = stream_information.createStreamresourceMemoryBuffer(region_description[key])
            stream_information.setResourceDomainTypes(memory_resource, Field.DOMAIN_TYPE_NODES)
            stream_information.setResourceAttributeReal(memory_resource, StreaminformationRegion.ATTRIBUTE_TIME, time)

    region.read(stream_information)


def _read_scene_description(scene, scene_description):
    stream_information = scene.createStreaminformationScene()
    stream_information.setIOFormat(stream_information.IO_FORMAT_DESCRIPTION)
    stream_information.createStreamresourceMemoryBuffer(scene_description)
    scene.read(stream_information)


def _add_electrode_data_points(region, time_based_locations):
    times = time_based_locations['time_array']
    field_module = region.getFieldmodule()
    cache = field_module.createFieldcache()
    coordinates_field = field_module.findFieldByName('coordinates')
    time_sequence = field_module.getMatchingTimesequence(times)
    node_set = field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)

    template = node_set.createNodetemplate()
    template.defineField(coordinates_field)
    template.setTimesequence(coordinates_field, time_sequence)
    field_module.beginChange()

    for key in time_based_locations:
        if key != 'time_array':
            node = node_set.createNode(-1, template)
            cache.setNode(node)
            for index, time in enumerate(times):
                cache.setTime(time)
                location = time_based_locations[key][index]
                coordinates_field.assignReal(cache, location)

    field_module.endChange()


class ElectrodeProjectionModel(object):

    def __init__(self, mesh_description, electrode_positions_on_plane, image_dimensions):

        self._projected_electrode_positions = None
        self._electrode_region = None
        self._coordinate_field = None
        self._scale_field = None
        self._scaled_coordinate_field = None

        self._electrode_positions_on_plane = electrode_positions_on_plane
        self._image_dimensions = image_dimensions
        self._context = Context('projection')
        #define_standard_visualisation_tools(self._context)
        define_standard_graphics_objects(self._context)

        region_description = mesh_description.get_region_description()
        # scene_description = mesh_description.get_scene_description()

        self._region = self._context.createRegion()
        # scene = region.getScene()

        _read_region_description(self._region, region_description)
        # _read_scene_description(scene, scene_description)

        times = electrode_positions_on_plane['time_array']
        time = times[1]
        print('fixing time at:', time)

        self._mesh_projection = MeshProjection(self._region)
        self._mesh_projection.set_time(time)
        self._mesh_projection.set_width_and_height(self._image_dimensions[0], self._image_dimensions[1])
        self._mesh_projection.render()

        self._initialise()
        self._set_electrode_data_points()
        self._render()

        self._electrode_region.writeFile(os.path.join(r'C:\Users\hsor001\Desktop\tmp', 'electrodes.ex'))

    def _initialise(self):
        self._electrode_region = self._region.createChild('electrodes')
        field_module = self._electrode_region.getFieldmodule()
        self._coordinate_field = create_field_finite_element(self._electrode_region)
        self._scale_field = field_module.createFieldConstant([1.0, 1.0, self._mesh_projection.get_z_scale_factor()])
        self._offset_field = field_module.createFieldConstant([0.0, 0.0, self._mesh_projection.get_depth()])
        offset_coordinate_field = field_module.createFieldAdd(self._coordinate_field, self._offset_field)
        self._adjusted_coordinate_field = field_module.createFieldMultiply(offset_coordinate_field, self._scale_field)

    def _set_electrode_data_points(self):
        for electrode_key in self._electrode_positions_on_plane:
            if electrode_key != 'time_array':
                point_locations = self._electrode_positions_on_plane[electrode_key]
                location = [point_locations[1][0], point_locations[1][1], 0]
                _create_data_point(self._coordinate_field, location)

    def _render(self):
        scene = self._electrode_region.getScene()
        scene.beginChange()

        material_module = scene.getMaterialmodule()
        electrode_material = material_module.findMaterialByName('orange')

        node_points = scene.createGraphicsPoints()
        node_points.setFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
        node_points.setCoordinateField(self._adjusted_coordinate_field)
        node_points.setMaterial(electrode_material)
        node_point_attr = node_points.getGraphicspointattributes()
        node_point_attr.setGlyphShapeType(Glyph.SHAPE_TYPE_SPHERE)
        node_point_attr.setBaseSize([8, 8, 8])

        scene.endChange()

    def project(self):
        index = 1
        field_module = self._region.getFieldmodule()
        field_module.beginChange()
        self._projected_electrode_positions = {}
        for electrode_key in self._electrode_positions_on_plane:
            if electrode_key != 'time_array':
                point_locations = self._electrode_positions_on_plane[electrode_key]
                projected_point = self._mesh_projection.project_point(point_locations[index])
                self._projected_electrode_positions[electrode_key] = projected_point

        field_module.endChange()

    def _get_coordinates(self, element, xi_location, time):
        field_module = self._region.getFieldmodule()
        field_cache = field_module.createFieldcache()
        field_cache.setMeshLocation(element, xi_location)
        field_cache.setTime(time)
        coordinates_field = field_module.findFieldByName('coordinates')
        _, location = coordinates_field.evaluateReal(field_cache, 3)

        return location

    def get_context(self):
        return self._context

    def load_settings(self):
        pass

    def get_scene(self):
        return self._mesh_projection.get_scene()

    def get_depth(self):
        return self._mesh_projection.get_depth()

    def set_depth(self, depth):
        field_module = self._offset_field.getFieldmodule()
        field_cache = field_module.createFieldcache()
        self._offset_field.assignReal(field_cache, [0.0, 0.0, depth])
        self._mesh_projection.set_depth(depth)

    def get_z_scale_factor(self):
        return self._mesh_projection.get_z_scale_factor()

    def set_z_scale_factor(self, scale_factor):
        field_module = self._scale_field.getFieldmodule()
        field_cache = field_module.createFieldcache()
        self._scale_field.assignReal(field_cache, [1.0, 1.0, scale_factor])
        self._mesh_projection.set_z_scale_factor(scale_factor)

    def get_electrode_positions_description(self):
        time_array = self._electrode_positions_on_plane['time_array']
        electrode_positions = {'time_array': time_array}
        for electrode_key in self._projected_electrode_positions:
            element, xi_coordinates = self._projected_electrode_positions[electrode_key]
            locations = []
            for time in time_array:
                location = self._get_coordinates(element, xi_coordinates, time)
                locations.append(location)

            electrode_positions[electrode_key] = locations

        return electrode_positions

    def clear_projected_points(self):
        self._mesh_projection.clear_projected_points()

    def done(self):
        pass


def _create_data_point(coordinate_field, location):
    field_module = coordinate_field.getFieldmodule()
    node_set = field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
    node_template = node_set.createNodetemplate()
    node_template.defineField(coordinate_field)
    node = node_set.createNode(-1, node_template)
    field_cache = field_module.createFieldcache()
    field_cache.setNode(node)
    coordinate_field.assignReal(field_cache, location)
