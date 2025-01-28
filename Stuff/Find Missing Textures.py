bl_info = {
    "name": "Find Missing Textures",
    "blender": (3, 6, 9),
    "category": "Object",
    "version": (1, 0),
    "author": "Your Name",
    "description": "Search for missing textures in the 'Textures' folder relative to the .blend file.",
}

import bpy
import os

class OBJECT_OT_find_missing_textures(bpy.types.Operator):
    """Search for missing textures in the 'Textures' folder relative to the .blend file"""
    bl_idname = "object.find_missing_textures"
    bl_label = "Find Missing Textures"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Ensure the .blend file is saved
        blend_dir = os.path.dirname(bpy.data.filepath)
        if not blend_dir:
            self.report({'ERROR'}, "Please save the .blend file first.")
            return {'CANCELLED'}
        
        # Define the relative textures folder path
        textures_folder = os.path.join(blend_dir, "Textures")
        
        # Check if the "Textures" folder exists
        if not os.path.exists(textures_folder):
            self.report({'ERROR'}, f"Textures folder not found: {textures_folder}")
            return {'CANCELLED'}
        
        # Track missing and found textures
        missing_textures = 0
        found_textures = 0
        
        # Iterate over all image textures in the file
        for image in bpy.data.images:
            # If the texture file doesn't exist or is empty
            if image.filepath == "" or not os.path.exists(bpy.path.abspath(image.filepath)):
                # Get the texture name and search in the "Textures" folder
                texture_name = os.path.basename(image.filepath)
                texture_path = os.path.join(textures_folder, texture_name)
                
                # If the texture exists in the "Textures" folder, relink it
                if os.path.exists(texture_path):
                    image.filepath = bpy.path.relpath(texture_path)
                    found_textures += 1
                    print(f"Found and linked: {texture_path}")
                else:
                    missing_textures += 1

        # Report results
        if found_textures > 0:
            self.report({'INFO'}, f"Linked {found_textures} textures from the 'Textures' folder.")
        if missing_textures > 0:
            self.report({'WARNING'}, f"Could not find {missing_textures} textures.")
        
        return {'FINISHED'}


# Add the operator to the right-click context menu for Object Mode
def menu_func(self, context):
    if context.mode == 'OBJECT':
        self.layout.separator()  # Add a separator line
        self.layout.operator(OBJECT_OT_find_missing_textures.bl_idname, text="Find Missing Textures")

# Register the operator and menu
def register():
    bpy.utils.register_class(OBJECT_OT_find_missing_textures)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)

# Unregister the operator and menu
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_find_missing_textures)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)

if __name__ == "__main__":
    register()
