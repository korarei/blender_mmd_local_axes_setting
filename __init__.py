bl_info = {
    "name": "mmd_local_axes_setting",
    "description": "This add-on inputs the value of the local axis of the selected bone in fixed axis setting and local axes setting of MMDTools.",
    "author": "Korarei",
    "version": (1, 0, 0),
    "blender": (3, 6, 5),
    "support": "COMMUNITY",
    "category": "Rigging",
    "location": "Properties > bone",
    "warning": "Please install MMDTools",
    "tracker_url": "https://github.com/korarei/blender_mmd_local_axes_setting/issues"
}


if "bpy" in locals():
    import imp
    imp.reload(local_axes)
else:
    from .operators import local_axes

import bpy
from bpy.props import EnumProperty, BoolProperty
    
    
class BONE_PT_MMDLocalAxesPanel(bpy.types.Panel):
    bl_idname = "BONE_PT_mmd_local_axes_setting"
    bl_label = "MMD Local Axes Setting"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "bone"
    
    @classmethod
    def poll(cls, context):
        return context.active_bone


    def draw(self, context):
        bone = context.active_pose_bone or context.active_object.pose.bones.get(context.active_bone.name, None)
        if bone is None:
            return
        
        layout = self.layout

        if bone.is_mmd_shadow_bone:
            layout.label(text='MMD Shadow Bone', icon='INFO')
            return
        
        scene = context.scene
        
        col = layout.column()
        col.label(text = "Setup Fixed Axis")
        box = layout.box()
        col = box.column()
        col.prop(scene, "enable_fixed_axis_checkbox", text = "Enable Fixed Axis Checkbox")
        col = box.column()
        if bone.lock_rotation[:].count(False) == 1:
            col.enabled = False
        col.use_property_split = True
        col.use_property_decorate = False        
        col.prop(scene, "fixed_axis", text = "Fixed Axis:")
        col = box.column()
        col.operator("bone.setup_mmd_fixed_axis")
        
        col = layout.column()
        col.separator()
        
        col.label(text = "Setup Local Axes")
        box = layout.box()
        col = box.column()
        col.prop(scene, "enable_local_axes_checkbox", text = "Enable Local Axes Checkbox")
        col.use_property_split = True
        col.use_property_decorate = False
        col.prop(scene, "local_x_axis", text = "Local X-Axis:")
        col.prop(scene, "local_z_axis", text = "Local Z-Axis:")
        col = box.column()
        col.operator("bone.setup_mmd_local_axes")
        
        
def init_props():
    scene = bpy.types.Scene
    scene.fixed_axis = EnumProperty(
        name = "Source Axis",
        description = "Source Axis",
        items = [
            ("+10", 'X', ""),
            ("+11", 'Y', ""),
            ("+12", 'Z', ""),
            ("-10", "-X", ""),
            ("-11", "-Y", ""),
            ("-12", "-Z", "")
        ],
        default = "+11"
    )
    scene.local_x_axis = EnumProperty(
        name = "Local X Source Axis",
        description = "Local X Source Axis",
        items = [
            ("+10", 'X', ""),
            ("+11", 'Y', ""),
            ("+12", 'Z', ""),
            ("-10", "-X", ""),
            ("-11", "-Y", ""),
            ("-12", "-Z", "")
        ],
        default = "+11"
    )
    scene = bpy.types.Scene
    scene.local_z_axis = EnumProperty(
        name = "Local Z Source Axis",
        description = "Local Z Source Axis",
        items = [
            ("+10", 'X', ""),
            ("+11", 'Y', ""),
            ("+12", 'Z', ""),
            ("-10", "-X", ""),
            ("-11", "-Y", ""),
            ("-12", "-Z", "")
        ],
        default="+10"
    )
    scene.enable_fixed_axis_checkbox = BoolProperty(
        name = "Enable Fixed Axis Checkbox",
        description = "Enable fixed axis checkbox",
        default = True
    )
    scene.enable_local_axes_checkbox = BoolProperty(
        name = "Enable Local Axes Checkbox",
        description = "Enable local axis checkbox",
        default = True
    )


def clear_props():
    scene = bpy.types.Scene
    del scene.fixed_axis
    del scene.local_x_axis
    del scene.local_z_axis
    del scene.enable_fixed_axis_checkbox
    del scene.enable_local_axes_checkbox


classes = [
    BONE_PT_MMDLocalAxesPanel,
    local_axes.BONE_OT_SetupMMDFixedAxis,
    local_axes.BONE_OT_SetupMMDLocalAxes
]
    
translation_dict = {
    "en_US" : {
        ("*", "Setup Fixed Axis") : "Setup Fixed Axis",
        ("*", "Setup Local Axes") : "Setup Local Axes",
        ("*", "Enable Fixed Axis Checkbox") : "Enable Fixed Axis Checkbox",
        ("*", "Enable Local Axes Checkbox") : "Enable Local Axes Checkbox",
        ("*", "Fixed Axis:") : "Fixed Axis:",
        ("*", "Local X-Axis:") : "Local X-Axis:",
        ("*", "Local Z-Axis:") : "Local Z-Axis:",
        ("*", "Load") : "Load",
        ("*", "Source Axis") : "Source Axis",
        ("*", "Local X Source Axis") : "Local X Source Axis",
        ("*", "Local Z Source Axis") : "Local Z Source Axis",
        ("*", "Load MMD fixed axis of selected bones from their bone axes or only rotatable axis") : "Load MMD fixed axis of selected bones from their bone axes or only rotatable axis",
        ("*", "Load MMD local axes of selected bones from their bone axes") : "Load MMD local axes of selected bones from their bone axes",
    },
    "ja_JP" : {
        ("*", "Setup Fixed Axis") : "軸制限の設定",
        ("*", "Setup Local Axes") : "ローカル軸の設定",
        ("*", "Enable Fixed Axis Checkbox") : "軸制限chk有効",
        ("*", "Enable Local Axes Checkbox") : "ローカル軸chk有効",
        ("*", "Enable fixed axis checkbox") : "軸制限チェックボックスを有効にする",
        ("*", "Enable local axis checkbox") : "ローカル軸チェックボックスを有効にする",
        ("*", "Fixed Axis:") : "軸制限:",
        ("*", "Local X-Axis:") : "ローカルX軸:",
        ("*", "Local Z-Axis:") : "ローカルZ軸:",
        ("*", "Load") : "読み込み",
        ("*", "Source Axis") : "変換元の軸",
        ("*", "Local X Source Axis") : "ローカルX軸の変換元",
        ("*", "Local Z Source Axis") : "ローカルZ軸の変換元",
        ("*", "Load MMD fixed axis of selected bones from their bone axes or only rotatable axis") : "選択されたボーンのMMD軸制限に入力されるローカル軸を、そのボーンの軸またはただ1つの回転できる軸から読み込む",
        ("*", "Load MMD local axes of selected bones from their bone axes") : "選択されたボーンのMMDローカル軸を、そのボーンの軸から読み込む",
    },
}   
    
def register():
    init_props()
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.app.translations.register(__name__, translation_dict)


def unregister():
    clear_props()
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.app.translations.unregister(__name__)


if __name__ == "__main__":
    register()