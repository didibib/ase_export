import bpy
import bpy_extras
from bpy.props import StringProperty, EnumProperty, BoolProperty
import os
from .builder import *
from .writer import *

class ASE_OT_ExportOperator(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = 'io_scene_ase.ase_export'
    bl_label = 'Export ASE'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    filename_ext = '.ase'

    filter_glob: StringProperty(
        default="*.ase",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be highlighted.
    )

    units: EnumProperty(
        default='M',
        items=(('M', 'Meters', ''),
               ('U', 'Unreal', '')),
        name='Units'
    )

    use_raw_mesh_data: BoolProperty(
        default=False,
        description='No modifiers will be evaluated as part of the exported mesh',
        name='Raw Mesh Data')
    
    combine_meshes: BoolProperty(
        default=False,
        name='Combine Meshes')

    units_scale = {
        'M': 100.0,
        'U': 1.0
    }

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'units', expand=False)
        layout.prop(self, 'use_raw_mesh_data')
        layout.prop(self, 'combine_meshes')

    def execute(self, context):
        options = ASEBuilderOptions()
        options.scale = self.units_scale[self.units]
        options.use_raw_mesh_data = self.use_raw_mesh_data
        dir_path = os.path.dirname(self.filepath)
        
        ase = ASE()
        for obj in context.selected_objects:            
            ASEBuilder().build(context, options, obj, ase)
            if not self.combine_meshes:
                ASEWriter().write(dir_path + '\\' + obj.name + self.filename_ext, ase)
                ase = ASE()
        if self.combine_meshes:
            ASEWriter().write(self.filepath, ase)
        self.report({'INFO'}, 'ASE exported successfully')
        return {'FINISHED'}
