bl_info = {
    "name": "Copy Head XYZ to Tail XYZ in Edit Mode",
    "blender": (3, 6, 9),
    "category": "Object",
    "version": (1, 4),
    "author": "Your Name",
    "description": "Copy head XYZ of the first selected bone and paste to tail XYZ of the second selected bone in Edit Mode.",
}

import bpy

class OBJECT_OT_copy_head_xyz_to_tail_xyz(bpy.types.Operator):
    """Copy the head XYZ position of the first selected bone to the tail XYZ position of the second selected bone (Edit Mode)"""
    bl_idname = "object.copy_head_xyz_to_tail_xyz"
    bl_label = "Copy Head XYZ to Tail XYZ"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Ensure we are in Edit Mode
        if bpy.context.mode != 'EDIT_ARMATURE':
            self.report({'ERROR'}, "You need to be in Edit Mode to use this operator.")
            return {'CANCELLED'}
        
        # Get the selected bones in Edit Mode
        selected_bones = bpy.context.selected_bones
        
        # Ensure exactly two bones are selected
        if len(selected_bones) != 2:
            self.report({'ERROR'}, "Please select exactly two bones.")
            return {'CANCELLED'}
        
        # First selected bone (active bone)
        bone_1 = bpy.context.active_bone

        # Second selected bone (last selected bone)
        bone_2 = [b for b in selected_bones if b != bone_1][0]

        # Copy head position of the first bone
        head_position = bone_1.head.copy()

        # Paste it to the tail position of the second bone
        bone_2.tail = head_position

        self.report({'INFO'}, f"Copied head XYZ of {bone_1.name} to tail XYZ of {bone_2.name}.")
        return {'FINISHED'}


# Add the operator to the right-click context menu for Edit Mode
def menu_func(self, context):
    if context.mode == 'EDIT_ARMATURE':
        self.layout.separator()  # Add a separator line
        self.layout.operator(OBJECT_OT_copy_head_xyz_to_tail_xyz.bl_idname, text="Copy Head XYZ to Tail XYZ")

# Register the operator and menu
def register():
    bpy.utils.register_class(OBJECT_OT_copy_head_xyz_to_tail_xyz)
    bpy.types.VIEW3D_MT_armature_context_menu.append(menu_func)

# Unregister the operator and menu
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_copy_head_xyz_to_tail_xyz)
    bpy.types.VIEW3D_MT_armature_context_menu.remove(menu_func)

if __name__ == "__main__":
    register()
