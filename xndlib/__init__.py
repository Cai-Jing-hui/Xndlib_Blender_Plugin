
bl_info = {
    "name": "XndLib",
    "author": "Cai Jinghui",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Edit Tab / Edit Mode Context Menu",
    "warning": "",
    "description": "Xanadu Tool Library",
    "doc_url": "",
    "category": "Pipeline",
}

# Import From Files

if "bpy" in locals():
    import importlib
    importlib.reload(pipeline_tools)
    importlib.reload(interface_tools)
    importlib.reload(material_tools)
else:
    from . import pipeline_tools
    from . import interface_tools
    from . import material_tools


import bpy

# ########################################
# ##### General functions ################
# ########################################

def register():
    pipeline_tools.register()
    interface_tools.register()
    material_tools.register()

def unregister():
    pipeline_tools.unregister()
    interface_tools.unregister()
    material_tools.unregister()

if __name__ == "__main__":
    
    register()