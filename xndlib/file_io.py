import bpy
import os
from bpy.types import Panel

# 隶属于pipeline_tools下的模块
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

        # Exporter
        box = layout.box()
        row = box.row()
        row.label(text="File Exporter")
        row = box.row()
        wm = context.window_manager
        row = box.row()
        row.prop(wm, "file_dir")
        row = box.row()
        row.operator("xnd.pipeline_exportfbx", text="Export FBX")
        row = box.row()
        row.operator("xnd.pipeline_exportobj", text="Export OBJ")
        row = box.row()
        row.operator("xnd.pipeline_inst2csv", text="Instance to CSV")

        


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty,FloatProperty
from bpy.types import Operator

    
'''
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄   ▄       ▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░▌ ▐░▌     ▐░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌ ▐░▌   ▐░▌ 
▐░▌          ▐░▌       ▐░▌  ▐░▌ ▐░▌  
▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌   ▐░▐░▌   
▐░░░░░░░░░░░▌▐░░░░░░░░░░▌     ▐░▌    
▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌   ▐░▌░▌   
▐░▌          ▐░▌       ▐░▌  ▐░▌ ▐░▌  
▐░▌          ▐░█▄▄▄▄▄▄▄█░▌ ▐░▌   ▐░▌ 
▐░▌          ▐░░░░░░░░░░▌ ▐░▌     ▐░▌
 ▀            ▀▀▀▀▀▀▀▀▀▀   ▀       ▀ 
                                                                                                                                                                                                                     
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
        path =  export_path = bpy.path.abspath(self.filepath)
        newimport(file_path=path,use_custom_normals=self.use_custom_normals,global_scale=self.global_scale,colors_type=self.colors_type)
        
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
            



  
class ExportFBX(bpy.types.Operator):
    bl_idname = "xnd.pipeline_exportfbx"
    bl_label = "Export FBX"

    def execute(self, context):
        # 获取当前场景和选中的物体列表
        scene = bpy.context.scene
        selected_objects = bpy.context.selected_objects

        wm = context.window_manager
        directory = wm.file_dir

        # 指定导出路径
        # export_path = "D:/XndLib/tools/blender_plugin/xndlib"
        export_path = bpy.path.abspath(directory)

        # 创建导出路径目录（如果不存在）
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        # 遍历选中的物体列表
        for obj in selected_objects:
            # 选择当前物体并导出为 FBX 文件
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            export_file = export_path + obj.name + ".fbx"
            bpy.ops.export_scene.fbx(filepath=export_file, use_selection=True)
            

        # 重新选择所有物体
        bpy.ops.object.select_all(action='DESELECT')
        for obj in selected_objects:
            obj.select_set(True)

        # 输出导出成功信息
        print("Exported selected objects to:", export_path)
        return {'FINISHED'}

'''
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀▀█░█▀▀▀ 
▐░▌       ▐░▌▐░▌       ▐░▌      ▐░▌    
▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌      ▐░▌    
▐░▌       ▐░▌▐░░░░░░░░░░▌       ▐░▌    
▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌      ▐░▌    
▐░▌       ▐░▌▐░▌       ▐░▌      ▐░▌    
▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄█░▌    
▐░░░░░░░░░░░▌▐░░░░░░░░░░▌ ▐░░░░░░░▌    
 ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀     
                                       
'''    
 
class ExportOBJ(bpy.types.Operator):
    bl_idname = "xnd.pipeline_exportobj"
    bl_label = "Export OBJ"

    def execute(self, context):
        # 获取当前场景和选中的物体列表
        scene = bpy.context.scene
        selected_objects = bpy.context.selected_objects

        wm = context.window_manager
        directory = wm.file_dir

        # 指定导出路径
        # export_path = "D:/XndLib/tools/blender_plugin/xndlib"
        export_path = bpy.path.abspath(directory)

        # 创建导出路径目录（如果不存在）
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        # 遍历选中的物体列表
        for obj in selected_objects:
            # 选择当前物体并导出为 OBJ 文件
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            export_file = export_path + obj.name + ".obj"
            bpy.ops.export_scene.obj(filepath=export_file, use_selection=True)
            

        # 重新选择所有物体
        bpy.ops.object.select_all(action='DESELECT')
        for obj in selected_objects:
            obj.select_set(True)

        # 输出导出成功信息
        print("Exported selected objects to:", export_path)
        return {'FINISHED'}









































'''
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄               ▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌             ▐░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀  ▐░▌           ▐░▌ 
▐░▌          ▐░▌            ▐░▌         ▐░▌  
▐░▌          ▐░█▄▄▄▄▄▄▄▄▄    ▐░▌       ▐░▌   
▐░▌          ▐░░░░░░░░░░░▌    ▐░▌     ▐░▌    
▐░▌           ▀▀▀▀▀▀▀▀▀█░▌     ▐░▌   ▐░▌     
▐░▌                    ▐░▌      ▐░▌ ▐░▌      
▐░█▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄█░▌       ▐░▐░▌       
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌        ▐░▌        
 ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀          ▀         
'''                          

import csv
from mathutils import Matrix

class InstanceToCSV(bpy.types.Operator):
    bl_idname = "xnd.pipeline_inst2csv"
    bl_label = "Instance to CSV"

    def execute(self, context):

        # 获取当前选中的物体
        obj = context.object
        

        # 指定 CSV 文件路径
        wm = context.window_manager
        directory = wm.file_dir

        # 指定导出路径
        # export_path = "D:/XndLib/tools/blender_plugin/xndlib"
        export_path = bpy.path.abspath(directory)

        # 创建导出路径目录（如果不存在）
        if not os.path.exists(export_path):
            os.makedirs(export_path)
        csv_file_path = export_path + obj.name + ".csv"

        # 打开 CSV 文件，并创建 CSV 写入器
        with open(csv_file_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            header = ["---", "SMesh","Transform"]  # 表头
            rows = []    # 数据行

            depsgraph = bpy.context.evaluated_depsgraph_get()
            # 获取选中的物体
            selected_objects = bpy.context.selected_objects

            # 遍历选中的物体
            for obj in selected_objects:
                eval = obj.evaluated_get(depsgraph)
                
                for inst in depsgraph.object_instances:
                    if inst.parent == eval:
                        if not inst.is_instance:
                            pass
                        # from .preset.datatable import unreal_physmesh
                        
                        # # print(inst.object.name)
                        # # print(inst.matrix_world.to_translation(), inst.matrix_world.to_euler())
                        
                        name = inst.object.name
                        sourceobj = bpy.data.objects.get(name)
                        
                        if "Path" in sourceobj.keys():
                            # 获取自定义属性 "Path" 的值
                            path = sourceobj["Path"]
                            
                        else:
                            print("对象 '{}' 没有自定义属性 'Path'。".format(name))
                            path = "--"
                    
                        
                        
                        #获取矩阵变换数据
                        matrix = inst.matrix_world
                        translation, rotation, scale = matrix.decompose()
                        transform = f"Rotation=(X={rotation.x}, Y={rotation.y}, Z={rotation.z}, W={rotation.w}),Translation=(X={translation.x},Y={translation.y},Z={translation.z}),Scale3D=(X={scale.x},Y={scale.y},Z={scale.z})"
                        
                        

                        # rows.append([name,translation, rotation, scale])
                        rows.append([name,path,transform])



           
    
            # write csv -----------------------------------------------
            # 写入 CSV 文件的表头
            writer.writerow(header)
            
            # 写入 CSV 文件
            for row in rows:
                writer.writerow(row)


        # 输出提示信息
        print(f"CSV 文件已保存到：{csv_file_path}")
        return {'FINISHED'}



'''
 ▄▄▄▄▄▄▄▄▄▄▄       ▄▄        ▄       ▄▄▄▄▄▄▄▄▄▄  
▐░░░░░░░░░░░▌     ▐░░▌      ▐░▌     ▐░░░░░░░░░░▌ 
▐░█▀▀▀▀▀▀▀▀▀      ▐░▌░▌     ▐░▌     ▐░█▀▀▀▀▀▀▀█░▌
▐░▌               ▐░▌▐░▌    ▐░▌     ▐░▌       ▐░▌
▐░█▄▄▄▄▄▄▄▄▄      ▐░▌ ▐░▌   ▐░▌     ▐░▌       ▐░▌
▐░░░░░░░░░░░▌     ▐░▌  ▐░▌  ▐░▌     ▐░▌       ▐░▌
▐░█▀▀▀▀▀▀▀▀▀      ▐░▌   ▐░▌ ▐░▌     ▐░▌       ▐░▌
▐░▌               ▐░▌    ▐░▌▐░▌     ▐░▌       ▐░▌
▐░█▄▄▄▄▄▄▄▄▄      ▐░▌     ▐░▐░▌     ▐░█▄▄▄▄▄▄▄█░▌
▐░░░░░░░░░░░▌     ▐░▌      ▐░░▌     ▐░░░░░░░░░░▌ 
 ▀▀▀▀▀▀▀▀▀▀▀       ▀        ▀▀       ▀▀▀▀▀▀▀▀▀▀  
                                                 

'''  




# Only needed if you want to add into a dynamic menu.
def menu_func_import(self, context):
    self.layout.operator(ImportFBX.bl_idname, text="FBX Import - XndLib")

def menu_func_export(self, context):
    self.layout.operator(InstanceToCSV.bl_idname, text="Instance to CSV - XndLib")



# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access).
def register():
    

    from bpy.types import WindowManager
    from bpy.props import (
        StringProperty
    )

    WindowManager.file_dir = StringProperty(
        name="Folder Path",
        subtype='DIR_PATH',
        default="//"
    )

    bpy.types.Scene.cache_enum = bpy.props.EnumProperty(
        name="cache_enum",
        items=[('enum_FBX', "fbx", ""),
            ('enum_OBJ', "obj", ""),
            ('enum_CSV', "csv", "")],
        default='enum_FBX'
    )

    
    bpy.utils.register_class(ExportFBX)
    bpy.utils.register_class(ExportOBJ)
    bpy.utils.register_class(InstanceToCSV)
    bpy.utils.register_class(ImportFBX)
    bpy.utils.register_class(ReimportFile)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    
    

def unregister():

    del bpy.types.Scene.cache_enum
    bpy.utils.unregister_class(ExportFBX)
    bpy.utils.unregister_class(ExportOBJ)
    bpy.utils.unregister_class(InstanceToCSV)
    bpy.utils.unregister_class(ImportFBX)
    bpy.utils.unregister_class(ReimportFile)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)








# if __name__ == "__main__":
#     register()

#     # test call
#     bpy.ops.xnd.pipeline_importfbx('INVOKE_DEFAULT')
