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
        


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty,FloatProperty
from bpy.types import Operator

'''
 ▄▄▄▄▄▄▄▄▄▄▄       ▄         ▄       ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌     ▐░▌       ▐░▌     ▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀▀      ▐░▌       ▐░▌      ▀▀▀▀█░█▀▀▀▀ 
▐░▌               ▐░▌       ▐░▌          ▐░▌     
▐░▌ ▄▄▄▄▄▄▄▄      ▐░▌       ▐░▌          ▐░▌     
▐░▌▐░░░░░░░░▌     ▐░▌       ▐░▌          ▐░▌     
▐░▌ ▀▀▀▀▀▀█░▌     ▐░▌       ▐░▌          ▐░▌     
▐░▌       ▐░▌     ▐░▌       ▐░▌          ▐░▌     
▐░█▄▄▄▄▄▄▄█░▌     ▐░█▄▄▄▄▄▄▄█░▌      ▄▄▄▄█░█▄▄▄▄ 
▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀▀▀       ▀▀▀▀▀▀▀▀▀▀▀       ▀▀▀▀▀▀▀▀▀▀▀ 
                                                 

'''

class ImportFBX(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "xnd.pipeline_importfbx"  # important since its how bpy.ops.xnd.pipeline_importfbx is constructed
    bl_label = "Import FBX"

    # ImportHelper mixin class uses this
    filename_ext = ".fbx"

    filter_glob: StringProperty(
        default="*.fbx",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_custom_normals: BoolProperty(
        name="use custom normals ",
        description="Example Tooltip",
        default=True,
    )

    global_scale: FloatProperty(
        name="Global Scale",
        description="",
        default=1,
    )

    colors_type: EnumProperty(
        name="Colors type",
        description="",
        items=(
            ('NONE', "None", "Description one"),
            ('SRGB', "sRGB", "Description two"),
            ('LINEAR', "Linear", "Description three")
        ),
        default='LINEAR',
    )

    def execute(self, context):
        # 导入fbx文件
        path = export_path = bpy.path.abspath(self.filepath)
        newimport(filepath=path,use_custom_normals=self.use_custom_normals,global_scale=self.global_scale,colors_type=self.colors_type)
        # bpy.ops.import_scene.fbx(filepath=path,use_custom_normals=self.use_custom_normals,global_scale=self.global_scale,colors_type=self.colors_type)

        # # Add attribute
        # objects = bpy.context.selected_objects
        # for obj in objects:
        #     # 获取导入文件的路径
        #     file_path = os.path.abspath(path)
        #     # 添加自定义属性 "filepath"
        #     obj["filepath"] = file_path
        return {'FINISHED'}
        
class ReimportFile(bpy.types.Operator):
    bl_idname = "xnd.reimport_file"
    bl_label = "Reimport File"
    bl_description = (
        "Reimport file append in filepath attribute"
    )

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        reimport(selected_objects)
        return {'FINISHED'}
    

    
'''
 ▄▄▄▄▄▄▄▄▄▄▄       ▄▄       ▄▄       ▄▄▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌     ▐░░▌     ▐░░▌     ▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌
 ▀▀▀▀█░█▀▀▀▀      ▐░▌░▌   ▐░▐░▌     ▐░█▀▀▀▀▀▀▀█░▌     ▐░█▀▀▀▀▀▀▀█░▌     ▐░█▀▀▀▀▀▀▀█░▌      ▀▀▀▀█░█▀▀▀▀ 
     ▐░▌          ▐░▌▐░▌ ▐░▌▐░▌     ▐░▌       ▐░▌     ▐░▌       ▐░▌     ▐░▌       ▐░▌          ▐░▌     
     ▐░▌          ▐░▌ ▐░▐░▌ ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌     ▐░▌       ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌          ▐░▌     
     ▐░▌          ▐░▌  ▐░▌  ▐░▌     ▐░░░░░░░░░░░▌     ▐░▌       ▐░▌     ▐░░░░░░░░░░░▌          ▐░▌     
     ▐░▌          ▐░▌   ▀   ▐░▌     ▐░█▀▀▀▀▀▀▀▀▀      ▐░▌       ▐░▌     ▐░█▀▀▀▀█░█▀▀           ▐░▌     
     ▐░▌          ▐░▌       ▐░▌     ▐░▌               ▐░▌       ▐░▌     ▐░▌     ▐░▌            ▐░▌     
 ▄▄▄▄█░█▄▄▄▄      ▐░▌       ▐░▌     ▐░▌               ▐░█▄▄▄▄▄▄▄█░▌     ▐░▌      ▐░▌           ▐░▌     
▐░░░░░░░░░░░▌     ▐░▌       ▐░▌     ▐░▌               ▐░░░░░░░░░░░▌     ▐░▌       ▐░▌          ▐░▌     
 ▀▀▀▀▀▀▀▀▀▀▀       ▀         ▀       ▀                 ▀▀▀▀▀▀▀▀▀▀▀       ▀         ▀            ▀      
                                                                                                                                                                                  
'''



def newimport(file_path,use_custom_normals = True,global_scale = 1,colors_type = "LINEAR"):
   

    bpy.ops.import_scene.fbx(filepath=file_path,use_custom_normals=use_custom_normals,global_scale=global_scale,colors_type=colors_type)
    # Add attribute
    objects = [ o for o in bpy.context.scene.objects if o.select_get()]
    for newobj in objects:
        newobj["filepath"] = file_path
        newobj["fileSettings"] = str(use_custom_normals)+','+str(global_scale)+','+str(colors_type)
        

def reimport(objects):
     for obj in objects:
        # 检查物体是否具有 "filepath" 属性
        if "filepath" in obj:
            # 检查 "filepath" 属性是否为空
            file_path = obj["filepath"]
            if file_path == "":
                print(f"物体 {obj.name} 的 'filepath' 属性为空")
                
            else:
                # 导入物体之前清除旧物体并记录网格数据
                dataname = obj.name
                for slot in obj.material_slots:
                    # obj.material_slots.clear(0)
                    bpy.data.materials.remove(slot.material, do_unlink=True)
               
                bpy.data.meshes.remove(obj.data, do_unlink=True)
                
                # 使用 "filepath" 属性的值作为文件路径导入文件
                
                bpy.ops.import_scene.fbx(filepath=file_path)

                # Add attribute
                objects = [ o for o in bpy.context.scene.objects if o.select_get()]
                for newobj in objects:
                    if(newobj.name != dataname):
                        for slot in newobj.material_slots:
                            # newobj.material_slots.clear(0)
                            bpy.data.materials.remove(slot.material, do_unlink=True)
                        bpy.data.meshes.remove(newobj.data, do_unlink=True)
                        
                        
                    else:
                        # 添加自定义属性 "filepath"
                        newobj["filepath"] = file_path

def refresh_ref(filepath):
    all_objects = bpy.data.objects
    objs = []
    for obj in all_objects:
        # 检查物体是否具有 "filepath" 属性
        if "filepath" in obj:
            # 比较 "filepath" 属性的值与传入参数
            if obj["filepath"] == filepath:
                
                objs.append(obj)
    if len(objs) ==0:
        newimport(filepath)
    else:
        reimport(objs)
            









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


# if __name__ == "__main__":
#     register()

#     # test call
#     bpy.ops.xnd.pipeline_importfbx('INVOKE_DEFAULT')
