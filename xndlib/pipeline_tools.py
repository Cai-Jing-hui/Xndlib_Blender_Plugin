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
      
       
       


    

def register():
    

   

   

    file_io.register()
    bpy.utils.register_class(Pipeline_Panel)
    


def unregister():
    

    bpy.utils.unregister_class(Pipeline_Panel)

    file_io.unregister()