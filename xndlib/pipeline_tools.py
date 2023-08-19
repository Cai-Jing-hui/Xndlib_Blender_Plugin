import bpy
import os
import json
from bpy.types import Panel
import threading
import socket

from . import file_io


class Pipeline_Panel(bpy.types.Panel):
    bl_idname = "XND_PT_pipeline_panel"
    bl_label = "Pipeline Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "XndLib"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        

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
        row.operator("xnd.pipeline_inst2csv", text="Instance to CSV")
        file_io.panel_draw(self,context)

      
        # Houdini
        box = layout.box()
        row = box.row()
        row.label(text="Houdini")
        row = box.row()
        # 添加一个下拉选择列表
        row.label(text="cache format:")
        row = box.row()
        row.prop(context.scene, "cache_enum", text="")
        row = box.row()
        row.operator("xnd.pipeline_sendtohou", text="Send to Houdini")
        row = box.row()
        row.operator("xnd.pipeline_getfromhou", text="Get from Houdini")
        row.prop(context.scene, "realtime_swt")

        



# class MyAddNumbersOperator(bpy.types.Operator):
#     bl_idname = "xnd.pipeline"
#     bl_label = "Add Numbers"

#     def execute(self, context):
#         bpy.ops.mesh.primitive_cube_add()
#         return {'FINISHED'}
    
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
            header = ["Name", "Position", "Rotation", "Scale"]  # 表头
            rows = []    # 数据行



            depsgraph = bpy.context.evaluated_depsgraph_get()
            for object_instance in depsgraph.object_instances:
                obj = object_instance.object
                if object_instance.is_instance:
                    
                    #
                    name = id(object_instance.instance_object)
                    
                    #获取矩阵变换数据
                    matrix = object_instance.matrix_world
                    translation, rotation, scale = matrix.decompose()
                    

                    rows.append([name,translation, rotation, scale])

            for object_instance in depsgraph.object_instances:
                if not object_instance.is_instance:
                    obj = object_instance.object
                    for row in rows:
                        if id(object_instance.object) == row[0]:
                            row[0]=obj.name
    
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
 ▄         ▄       ▄▄▄▄▄▄▄▄▄▄▄       ▄         ▄       ▄▄▄▄▄▄▄▄▄▄        ▄▄▄▄▄▄▄▄▄▄▄       ▄▄        ▄       ▄▄▄▄▄▄▄▄▄▄▄ 
▐░▌       ▐░▌     ▐░░░░░░░░░░░▌     ▐░▌       ▐░▌     ▐░░░░░░░░░░▌      ▐░░░░░░░░░░░▌     ▐░░▌      ▐░▌     ▐░░░░░░░░░░░▌
▐░▌       ▐░▌     ▐░█▀▀▀▀▀▀▀█░▌     ▐░▌       ▐░▌     ▐░█▀▀▀▀▀▀▀█░▌      ▀▀▀▀█░█▀▀▀▀      ▐░▌░▌     ▐░▌      ▀▀▀▀█░█▀▀▀▀ 
▐░▌       ▐░▌     ▐░▌       ▐░▌     ▐░▌       ▐░▌     ▐░▌       ▐░▌          ▐░▌          ▐░▌▐░▌    ▐░▌          ▐░▌     
▐░█▄▄▄▄▄▄▄█░▌     ▐░▌       ▐░▌     ▐░▌       ▐░▌     ▐░▌       ▐░▌          ▐░▌          ▐░▌ ▐░▌   ▐░▌          ▐░▌     
▐░░░░░░░░░░░▌     ▐░▌       ▐░▌     ▐░▌       ▐░▌     ▐░▌       ▐░▌          ▐░▌          ▐░▌  ▐░▌  ▐░▌          ▐░▌     
▐░█▀▀▀▀▀▀▀█░▌     ▐░▌       ▐░▌     ▐░▌       ▐░▌     ▐░▌       ▐░▌          ▐░▌          ▐░▌   ▐░▌ ▐░▌          ▐░▌     
▐░▌       ▐░▌     ▐░▌       ▐░▌     ▐░▌       ▐░▌     ▐░▌       ▐░▌          ▐░▌          ▐░▌    ▐░▌▐░▌          ▐░▌     
▐░▌       ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌     ▐░█▄▄▄▄▄▄▄█░▌     ▐░█▄▄▄▄▄▄▄█░▌      ▄▄▄▄█░█▄▄▄▄      ▐░▌     ▐░▐░▌      ▄▄▄▄█░█▄▄▄▄ 
▐░▌       ▐░▌     ▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌     ▐░░░░░░░░░░▌      ▐░░░░░░░░░░░▌     ▐░▌      ▐░░▌     ▐░░░░░░░░░░░▌
 ▀         ▀       ▀▀▀▀▀▀▀▀▀▀▀       ▀▀▀▀▀▀▀▀▀▀▀       ▀▀▀▀▀▀▀▀▀▀        ▀▀▀▀▀▀▀▀▀▀▀       ▀        ▀▀       ▀▀▀▀▀▀▀▀▀▀▀ 
                                                                                                                         
                              
'''                                  






socket_host = 'localhost'
socket_port=9999


    
class SendToHoudini(bpy.types.Operator):
    bl_idname = "xnd.pipeline_sendtohou"
    bl_label = "Send to Houdini"

    def execute(self, context):
         # 获取所选物体
        selected_objects = bpy.context.selected_objects
        data = []

        export_path = bpy.path.abspath("//cache/")
        export_path = export_path.replace("\\","/")

        # 创建导出路径目录（如果不存在）
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        selected_option = bpy.context.scene.cache_enum


        # for object in selected_objects:
        object = selected_objects
        if(selected_option == "enum_FBX"):
            export_file = export_path + object[0].name + ".fbx"
            bpy.ops.export_scene.fbx(filepath=export_file, use_selection=True)
        if (selected_option == "enum_OBJ"):
            export_file = export_path + object[0].name + ".obj"
            bpy.ops.export_scene.obj(filepath=export_file, use_selection=True)
            '''
            https://docs.blender.org/api/current/bpy.ops.wm.html#bpy.ops.wm.obj_export
            '''
        if (selected_option == "enum_CSV"):
            print("Uhuh")
            


        # data waiting for send
        json_data = json.dumps(export_file)

        TCP_IP = 'localhost'
        TCP_PORT = 1976

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((TCP_IP, TCP_PORT))
        client.send(json_data.encode('utf-8'))
        client.close()
        return {'FINISHED'}
    


class GetFromHoudini(bpy.types.Operator):
    bl_idname = "xnd.pipeline_getfromhou"
    bl_label = "Get from Houdini"
    def execute(self, context):
        realtime_swt = bpy.context.scene.realtime_swt
        if(realtime_swt == 1):
            bpy.app.handlers.s

        thread = threading.Thread(target=GetFromHoudini.thread_update)
        thread.start()
        return {'FINISHED'}

    def thread_update():

        TCP_IP = 'localhost'
        TCP_PORT = 1971

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((TCP_IP, TCP_PORT))
        server.listen(5)


        while True:
            client, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            
            filepath = client.recv(1024).decode('utf-8')
            print(f"Received from Houdini: {filepath}")


            file_io.refresh_ref(filepath)
            # bpy.ops.import_scene.fbx(filepath=request,global_scale=100)


            client.send(b"ACK")
            client.close()




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

        

    

def register():
    

    from bpy.types import WindowManager
    from bpy.props import (
        StringProperty
    )

    WindowManager.file_dir = StringProperty(
        name="Folder Path",
        subtype='DIR_PATH',
        default=""
    )

    bpy.types.Scene.cache_enum = bpy.props.EnumProperty(
        name="cache_enum",
        items=[('enum_FBX', "fbx", ""),
               ('enum_OBJ', "obj", ""),
               ('enum_CSV', "csv", "")],
        default='enum_FBX'
    )

    bpy.types.Scene.realtime_swt = bpy.props.BoolProperty(
        name="Realtime",
        description="Send to houdini by frame",
        default=False
    )

    file_io.register()
    bpy.utils.register_class(ExportFBX)
    bpy.utils.register_class(InstanceToCSV)
    bpy.utils.register_class(SendToHoudini)
    bpy.utils.register_class(GetFromHoudini)
    bpy.utils.register_class(Pipeline_Panel)
    


def unregister():
    

    del bpy.types.Scene.cache_enum
    bpy.utils.unregister_class(Pipeline_Panel)

    file_io.unregister()
    bpy.utils.unregister_class(ExportFBX)
    bpy.utils.unregister_class(InstanceToCSV)
    bpy.utils.unregister_class(SendToHoudini)
    bpy.utils.unregister_class(GetFromHoudini)
