import bpy
    
    
class BONE_OT_SetupMMDLocalAxes(bpy.types.Operator):
    bl_idname = "bone.setup_mmd_local_axes"
    bl_label = "Load"
    bl_description = "Load MMD local axes of selected bones from their bone axes"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_bone
    
    
    def execute(self, context):
        scene = context.scene
        local_x_axis = scene.local_x_axis
        local_z_axis = scene.local_z_axis
        enable_local_axes_checkbox = scene.enable_local_axes_checkbox
        
        obj_mode = context.active_object.mode
        bpy.ops.object.mode_set(mode = "POSE")
        
        excluded_bones = []
        for b in context.selected_pose_bones:
            if not b.is_mmd_shadow_bone:
                mmd_bone = b.mmd_bone
                mmd_bone.enabled_local_axes = enable_local_axes_checkbox
                axes = b.bone.matrix_local.to_3x3().transposed()
                mmd_bone.local_axis_x = int(local_x_axis[0 : 2]) * axes[int(local_x_axis[-1])].xzy
                mmd_bone.local_axis_z = int(local_z_axis[0 : 2]) * axes[int(local_z_axis[-1])].xzy
            else:
                excluded_bones.append(b.name)
                    
        bpy.ops.object.mode_set(mode = obj_mode)
        print("Excluded Bones:\n", excluded_bones)

        return {'FINISHED'}
    
    
class BONE_OT_SetupMMDFixedAxis(bpy.types.Operator):
    bl_idname = "bone.setup_mmd_fixed_axis"
    bl_label = "Load"
    bl_description = "Load MMD fixed axis of selected bones from their bone axes or only rotatable axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_bone
    
    
    def execute(self, context):
        scene = context.scene
        fixed_axis = scene.fixed_axis
        enable_fixed_axis_checkbox = scene.enable_fixed_axis_checkbox
        
        obj_mode = context.active_object.mode
        bpy.ops.object.mode_set(mode = "POSE")
        
        excluded_bones = []  
        for b in context.selected_pose_bones:
            if not b.is_mmd_shadow_bone:
                mmd_bone = b.mmd_bone
                lock_rotation = b.lock_rotation[:]
                mmd_bone.enabled_fixed_axis = enable_fixed_axis_checkbox
                axes = b.bone.matrix_local.to_3x3().transposed()
                if lock_rotation.count(False) == 1:
                    mmd_bone.fixed_axis = axes[lock_rotation.index(False)].xzy
                else:
                    mmd_bone.fixed_axis = int(fixed_axis[0 : 2]) * axes[int(fixed_axis[-1])].xzy
            else:
                excluded_bones.append(b.name)
                    
        bpy.ops.object.mode_set(mode = obj_mode)
        print("Excluded Bones:\n", excluded_bones)

        return {'FINISHED'}