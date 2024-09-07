bl_info = {
    "name": "PickYourFriend's Useful Script",
    "author": "Me",
    "version": (1, 2, 0),
    "blender": (3, 3, 1),
    "location": "3D View > Sidebar > PickYourFriend",
    "description": "Renames the bones, manages shape keys, and updates materials.",
    "warning": "",
    "doc_url": "",
    "support": 'COMMUNITY',
    "category": "VRC",
    "tracker_url": "",
    "doc_url": ""
}

import bpy

def rename_bones(context):
    obj = context.object

    namelist = [
        # Main Hierarchy
        ("Hips", "Bip001Pelvis"),
        ("Spine", "Bip001Spine"),
        ("Chest", "Bip001Spine1"),
        ("Upper Chest", "Bip001Spine2"),
        ("Neck", "Bip001Neck"),
        ("Head", "Bip001Head"),
        ("Right shoulder", "Bip001RClavicle"),
        ("Left shoulder", "Bip001LClavicle"),
        ("Right arm", "Bip001RUpperArm"),
        ("Right elbow", "Bip001RForearm"),
        ("Right wrist", "Bip001RHand"),
        ("Left arm", "Bip001LUpperArm"),
        ("Left elbow", "Bip001LForearm"),
        ("Left wrist", "Bip001LHand"),
        ("Right leg", "Bip001RThigh"),
        ("Right knee", "Bip001RCalf"),
        ("Right ankle", "Bip001RFoot"),
        ("Right toe", "Bip001RToe0"),
        ("Left leg", "Bip001LThigh"),
        ("Left knee", "Bip001LCalf"),
        ("Left ankle", "Bip001LFoot"),
        ("Left toe", "Bip001LToe0"),
        # Right Hand
        ("Thumb1_R", "Bip001RFinger0"),
        ("Thumb2_R", "Bip001RFinger01"),        
        ("Thumb3_R", "Bip001RFinger02"),
        ("IndexFinger1_R", "Bip001RFinger1"),
        ("IndexFinger2_R", "Bip001RFinger11"),
        ("IndexFinger3_R", "Bip001RFinger12"),
        ("MiddleFinger1_R", "Bip001RFinger2"),
        ("MiddleFinger2_R", "Bip001RFinger21"),
        ("MiddleFinger3_R", "Bip001RFinger22"),
        ("RingFinger1_R", "Bip001RFinger3"),
        ("RingFinger2_R", "Bip001RFinger31"),
        ("RingFinger3_R", "Bip001RFinger32"),
        ("LittleFinger1_R", "Bip001RFinger4"),
        ("LittleFinger2_R", "Bip001RFinger41"),
        ("LittleFinger3_R", "Bip001RFinger42"),
        # Left Hand
        ("Thumb1_L", "Bip001LFinger0"),
        ("Thumb2_L", "Bip001LFinger01"),
        ("Thumb3_L", "Bip001LFinger02"),
        ("IndexFinger2_L", "Bip001LFinger11"),
        ("IndexFinger1_L", "Bip001LFinger1"),
        ("IndexFinger3_L", "Bip001LFinger12"),
        ("MiddleFinger1_L", "Bip001LFinger2"),
        ("MiddleFinger2_L", "Bip001LFinger21"),
        ("MiddleFinger3_L", "Bip001LFinger22"),
        ("RingFinger1_L", "Bip001LFinger3"),
        ("RingFinger2_L", "Bip001LFinger31"),
        ("RingFinger3_L", "Bip001LFinger32"),
        ("LittleFinger1_L", "Bip001LFinger4"),
        ("LittleFinger2_L", "Bip001LFinger41"),
        ("LittleFinger3_L", "Bip001LFinger42"),
        # Possible Eye Names
        ("Eye_L", "+EyeBoneLA02"),
        ("Eye_R", "+EyeBoneRA02"),
        ("Eye_L", "EyeBoneLA02"),
        ("Eye_R", "EyeBoneRA02")
    ]

    for newname, name in namelist:
        pb = obj.pose.bones.get(name)
        if pb is None:
            continue
        pb.name = newname

def manage_shape_keys(context):
    obj = context.object
    
    # Check if there are any shape keys with "vrc" in their name
    vrc_shape_key_exists = any("vrc" in key.name for key in bpy.data.shape_keys["Key.001"].key_blocks)

    if vrc_shape_key_exists:
        # Remove shape keys starting from index 35, 18 times
        bpy.context.object.active_shape_key_index = 35
        for _ in range(18):
            bpy.ops.object.shape_key_remove(all=False)

    def create_shape_key_from_mix(shape_key_name, shape_key_value_dict):
        for key_name, value in shape_key_value_dict.items():
            bpy.data.shape_keys["Key.001"].key_blocks[key_name].value = value
        bpy.ops.object.shape_key_add(from_mix=True)
        obj.active_shape_key_index = len(bpy.data.shape_keys["Key.001"].key_blocks) - 1
        bpy.data.shape_keys["Key.001"].key_blocks[-1].name = shape_key_name
        bpy.ops.object.shape_key_clear()
    
    def move_shape_key(name, positions):
        obj.active_shape_key_index = [i for i, key in enumerate(bpy.data.shape_keys["Key.001"].key_blocks) if key.name == name][0]
        for _ in range(positions):
            bpy.ops.object.shape_key_move(type='DOWN')
    
    create_shape_key_from_mix("Ah", {"Mouth_A01": 1})
    create_shape_key_from_mix("Oh", {"Mouth_A01": 0.5, "Mouth_Line02": 1})
    create_shape_key_from_mix("Ch", {"Mouth_Open01": 1})
    create_shape_key_from_mix("Blink", {"Eye_WinkB_L": 1, "Eye_WinkB_R": 1})
    create_shape_key_from_mix("Blink Happy", {"Eye_WinkA_L": 1, "Eye_WinkA_R": 1})
    create_shape_key_from_mix("Blink Straight", {"Eye_WinkC_L": 1, "Eye_WinkC_R": 1})
    create_shape_key_from_mix("vrc.v_aa", {"Ah": 1})
    create_shape_key_from_mix("vrc.v_ch", {"Ch": 1})
    create_shape_key_from_mix("vrc.v_dd", {"Ah": 0.3, "Ch": 0.7})
    create_shape_key_from_mix("vrc.v_e", {"Ah": 0.5, "Ch": 0.2})
    create_shape_key_from_mix("vrc.v_ff", {"Ah": 0.2, "Ch": 0.4})
    create_shape_key_from_mix("vrc.v_ih", {"Ch": 0.7, "Oh": 0.3})
    create_shape_key_from_mix("vrc.v_kk" , {"Ah": 0.7, "Ch": 0.4})            
    create_shape_key_from_mix("vrc.v_nn", {"Ah": 0.2, "Ch": 0.7})
    create_shape_key_from_mix("vrc.v_oh", {"Oh": 1})
    create_shape_key_from_mix("vrc.v_ou", {"Ah": 0.2, "Oh": 0.8})
    create_shape_key_from_mix("vrc.v_pp", {"Ah": 0.0004, "Oh": 0.0004})
    create_shape_key_from_mix("vrc.v_rr", {"Ch": 0.5, "Oh": 0.3})
    create_shape_key_from_mix("vrc.v_sil", {"Ah": 0.0002, "Ch": 0.0002})
    create_shape_key_from_mix("vrc.v_ss", {"Ch": 0.8})
    create_shape_key_from_mix("vrc.v_th", {"Ah": 0.4, "Oh": 0.15})

    move_shape_key("vrc.v_th", 2)
    move_shape_key("vrc.v_ss", 2)
    move_shape_key("vrc.v_sil", 2)
    move_shape_key("vrc.v_rr", 2)
    move_shape_key("vrc.v_pp", 2)
    move_shape_key("vrc.v_ou", 2)    
    move_shape_key("vrc.v_oh", 2)
    move_shape_key("vrc.v_nn", 2)
    move_shape_key("vrc.v_kk", 2)
    move_shape_key("vrc.v_ih", 2)
    move_shape_key("vrc.v_ff", 2)
    move_shape_key("vrc.v_e", 2)
    move_shape_key("vrc.v_dd", 2)
    move_shape_key("vrc.v_ch", 2)
    move_shape_key("vrc.v_aa", 2)
    move_shape_key("Blink Straight", 2)
    move_shape_key("Blink Happy", 2)
    move_shape_key("Blink", 2)

def update_materials():
    # Function to set alpha mode to NONE for images
    def set_alpha_mode_none(image):
        if image and image.alpha_mode != 'NONE':
            image.alpha_mode = 'NONE'
            print(f"Set alpha mode to NONE for image '{image.name}'")

    # Function to replace Principled BSDF with Background shader
    def replace_shader_nodes(material):
        if material.node_tree is None:
            material.use_nodes = True

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Find all Principled BSDF nodes
        principled_bsdf_nodes = [node for node in nodes if node.type == 'BSDF_PRINCIPLED']
        for node in principled_bsdf_nodes:
            # Create Background shader node
            background_node = nodes.new(type='ShaderNodeBackground')
            shader_output = nodes.get('Material Output') or nodes.new(type='ShaderNodeOutputMaterial')

            # Find and store existing texture node if present
            texture_node = None
            for link in node.inputs['Base Color'].links:
                if link.from_node.type == 'TEX_IMAGE':
                    texture_node = link.from_node
                    set_alpha_mode_none(texture_node.image)  # Set alpha mode to NONE
                    break

            # Remove the Principled BSDF node
            node_location = node.location
            nodes.remove(node)
            
            # Move Background shader node to the location of removed Principled BSDF
            background_node.location = node_location

            # Connect existing texture node if present
            if texture_node:
                texture_node.location = (node_location.x - 200, node_location.y)
                links.new(texture_node.outputs['Color'], background_node.inputs['Color'])

            # Connect the Background shader node to the output
            if shader_output:
                links.new(background_node.outputs['Background'], shader_output.inputs['Surface'])

    # Select all mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')

    # Apply changes to all selected mesh objects
    selected_objects = bpy.context.selected_objects.copy()  # Copy to avoid modifying the original list while iterating
    for obj in selected_objects:
        if obj.type == 'MESH':
            for mat_slot in obj.material_slots:
                if mat_slot.material:
                    replace_shader_nodes(mat_slot.material)
                    print(f"Replaced Principled BSDF with Background shader in material '{mat_slot.material.name}'")

    # Deselect all mesh objects
    bpy.ops.object.select_all(action='DESELECT')

class RenameBonesOperator(bpy.types.Operator):
    """Renames bones in the selected object if in edit mode"""
    bl_idname = "object.rename_bones_operator"
    bl_label = "Rename Bones"

    def execute(self, context):
        rename_bones(context)
        return {'FINISHED'}

class ShapeKeyManagerOperator(bpy.types.Operator):
    """Creates and setups shape keys"""
    bl_idname = "object.shape_key_manager_operator"
    bl_label = "Generate Shape Keys"

    def execute(self, context):
        manage_shape_keys(context)
        return {'FINISHED'}

class UpdateMaterialsOperator(bpy.types.Operator):
    """Replaces Principled BSDF with Background shader and sets alpha mode to NONE"""
    bl_idname = "object.update_materials_operator"
    bl_label = "Set Materials"

    def execute(self, context):
        update_materials()
        return {'FINISHED'}

class VIEW3D_PT_my_custom_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "PickYourFriend"
    bl_label = "PickYourFriend's Useful Script"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.rename_bones_operator", text="Rename Bones")
        layout.operator("object.shape_key_manager_operator", text="Setup Shapekeys")
        layout.operator("object.update_materials_operator", text="Setup Materials")

def register():
    bpy.utils.register_class(RenameBonesOperator)
    bpy.utils.register_class(ShapeKeyManagerOperator)
    bpy.utils.register_class(UpdateMaterialsOperator)
    bpy.utils.register_class(VIEW3D_PT_my_custom_panel)

def unregister():
    bpy.utils.unregister_class(RenameBonesOperator)
    bpy.utils.unregister_class(ShapeKeyManagerOperator)
    bpy.utils.unregister_class(UpdateMaterialsOperator)
    bpy.utils.unregister_class(VIEW3D_PT_my_custom_panel)

if __name__ == "__main__":
    register()