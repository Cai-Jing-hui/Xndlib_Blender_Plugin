import bpy

bpy.context.scene.render.resolution_x = 2048
bpy.context.scene.render.resolution_y = 2048

camera_name = "Camera_TextureCapturer"

# 检查相机数据是否存在
if camera_name in bpy.data.cameras:
    CamData = bpy.data.cameras[camera_name]
else:
    CamData = bpy.data.cameras.new(camera_name)

CamData.type = 'ORTHO'
CamData.ortho_scale = 1

CamObj = bpy.data.objects.new("Camera_TextureCapturer", CamData)
CamObj.location = (0,0,1)
CamObj.rotation_euler = (0,0,0)
bpy.context.scene.camera = CamObj
bpy.context.scene.collection.objects.link(CamObj)

bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
