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
    

   

    bpy.types.Scene.realtime_swt = bpy.props.BoolProperty(
        name="Realtime",
        description="Send to houdini by frame",
        default=False
    )

    file_io.register()
    bpy.utils.register_class(SendToHoudini)
    bpy.utils.register_class(GetFromHoudini)
    bpy.utils.register_class(Pipeline_Panel)
    


def unregister():
    

    bpy.utils.unregister_class(Pipeline_Panel)

    file_io.unregister()
    bpy.utils.unregister_class(SendToHoudini)
    bpy.utils.unregister_class(GetFromHoudini)
