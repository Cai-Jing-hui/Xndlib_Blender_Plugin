import bpy
import random



from bpy.types import Panel


class Material_Panel(bpy.types.Panel):
    bl_idname = "XND_PT_Material_Panel"
    bl_label = "Material Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "XndLib"

    def draw(self, context):
        box = self.layout.box()
        row = box.row()
        row.label(text="Material")
        row = box.row()
        row.operator("xnd.randmatcol", text="Random Material Color")



             
        

class RandMatCol(bpy.types.Operator):
    bl_idname = "xnd.randmatcol"
    bl_label = "Random material color"
    bl_description = (
        "Move objs to same name collection"
    )

    def execute(self, context):
    
        # 获取当前选中的物体
        selected_objects = bpy.context.selected_objects

        # 遍历选中的每个物体
        for obj in selected_objects:
            # 遍历每个物体的所有材质球
            for slot in obj.material_slots:
                if slot.material is not None:
                    # 处理每个材质球
                    material = slot.material
                    random.seed(slot)
                    material.diffuse_color = (random.random(), random.random(), random.random(),1)

        return {'FINISHED'}
    

# def outlinedraw(self, context):
#         layout = self.layout
#         row = layout.row()
#         row.label(text="XndLib")
#         row = layout.row()
#         row.separator()
#         row = layout.row()
#         row.operator("xnd.randmatcol", text="Random ID Color")
#         # .arg = 'Move objs to same name collection'


def register():
    bpy.utils.register_class(RandMatCol)
    bpy.utils.register_class(Material_Panel)

    # bpy.types.MATERIAL_UL_matslots.append(outlinedraw)
    


def unregister():
    bpy.utils.unregister_class(RandMatCol)
    bpy.utils.unregister_class(Material_Panel)
