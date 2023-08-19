import bpy
import os
from bpy.types import Panel


class Interface_Panel(bpy.types.Panel):
    bl_idname = "XND_PT_Interface_Panel"
    bl_label = "Interface Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "XndLib"

    def draw(self, context):
        box = self.layout.box()
        row = box.row()
        row.label(text="Interface")
        row = box.row()
        row.operator("xnd.interface_showname", text="Show name")
        row = box.row()



             
        

class MoveNewCollection(bpy.types.Operator):
    bl_idname = "xnd.newcollection"
    bl_label = "Link Collection"
    bl_description = (
        "Move objs to same name collection"
    )

    def execute(self, context):
    
        # 获取所选物体
        selected_objects = bpy.context.selected_objects

        if len(selected_objects) > 0:
            # 获取当前物体
            current_object = selected_objects[0]
            
            # 创建集合
            collection_name = current_object.name
            collection = bpy.data.collections.new(collection_name)
            bpy.context.scene.collection.children.link(collection)
            
            # 将所选物体移到集合中
            for obj in selected_objects:
                obj.users_collection[0].objects.unlink(obj)
                collection.objects.link(obj)

        return {'FINISHED'}
    
class ShowName(bpy.types.Operator):
    bl_idname = "xnd.interface_showname"
    bl_label = "Show Object Name"
    bl_description = (
        "Show objects name switch"
    )

    def execute(self, context):
    
        # 获取所选物体
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            obj.show_name = not obj.show_name
        return {'FINISHED'}
    

def outlinedraw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="XndLib")
        row = layout.row()
        row.separator()
        row = layout.row()
        row.operator("xnd.newcollection", text="Move to collection")
        # .arg = 'Move objs to same name collection'


def register():
    bpy.utils.register_class(MoveNewCollection)
    bpy.utils.register_class(Interface_Panel)
    bpy.utils.register_class(ShowName)

    bpy.types.OUTLINER_MT_object.append(outlinedraw)
    


def unregister():
    bpy.utils.unregister_class(MoveNewCollection)
    bpy.utils.unregister_class(Interface_Panel)
    bpy.utils.unregister_class(ShowName)
