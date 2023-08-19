import bpy
import os
from bpy.types import Panel


def panel_draw(self, context):
        layout = self.layout
        scene = context.scene
        box = layout.box()
        row = box.row()
        row.label(text="File Importer")
        row = box.row()
        row.operator("xnd.pipeline_importfbx", text="Import FBX")
        row = box.row()
        row.operator("xnd.reimport_file", text="Reimport File")

class ReimportFile(bpy.types.Operator):
    bl_idname = "xnd.reimport_file"
    bl_label = "Reimport File"
    bl_description = (
        "Reimport file append in filepath attribute"
    )

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        refresh_import(selected_objects)
        return {'FINISHED'}





        # Only needed if you want to add into a dynamic menu.
def menu_func_import(self, context):
    self.layout.operator(ImportFBX.bl_idname, text="FBX Import - XndLib")


# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access).
def register():
    bpy.utils.register_class(ImportFBX)
    bpy.utils.register_class(ReimportFile)
    # bpy.utils.register_class(File_IO)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    


def unregister():
    
    # bpy.utils.unregister_class(File_IO)
    bpy.utils.unregister_class(ImportFBX)
    bpy.utils.unregister_class(ReimportFile)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
