import bpy
import random
import os



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
        row.operator("xnd.texmakerpreset", text="TextureMaker Preset")
        row = box.row()
        row.operator("xnd.randmatcol", text="Random Material Color")



             
        

class RandMatCol(bpy.types.Operator):
    bl_idname = "xnd.randmatcol"
    bl_label = "Random material color"
    bl_description = (
        ""
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
    

class TexMakerPreset(bpy.types.Operator):
    bl_idname = "xnd.texmakerpreset"
    bl_label = "TextureMaker Preset"
    bl_description = (
        "Add a base textureMaker set "
    )

    def execute(self, context):
   
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 拼接目标文件的路径
        preset_folder = os.path.join(current_dir, "preset")
        preset_file = os.path.join(preset_folder, "texturemaker/TextureMaker.py")

        # 执行指定路径下的Python文件
        with open(preset_file, 'r') as file:
            code = file.read()
            exec(code)
        

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RandMatCol)
    bpy.utils.register_class(TexMakerPreset)
    bpy.utils.register_class(Material_Panel)

    # bpy.types.MATERIAL_UL_matslots.append(outlinedraw)
    


def unregister():
    bpy.utils.unregister_class(RandMatCol)
    bpy.utils.unregister_class(TexMakerPreset)
    bpy.utils.unregister_class(Material_Panel)
