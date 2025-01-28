bl_info = {
    "name": "PickYourFriend's Useful Script",
    "author": "Me",
    "version": (1, 4, 0),
    "blender": (3, 3, 6),
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

def batch_rename_bones():
    # Ensure we are in Pose Mode and have an Armature selected
    if bpy.context.object and bpy.context.object.type == 'ARMATURE':
        bpy.ops.object.mode_set(mode='EDIT')
        
        armature = bpy.context.object
        for bone in armature.data.edit_bones:
            # Replace '+' with a blank space in the bone name
            if '+' in bone.name:
                bone.name = bone.name.replace('+', '')
        
        bpy.ops.object.mode_set(mode='OBJECT')

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
        ("Thumb1_R", "DMZR01"),
        ("Thumb2_R", "DMZR02"),        
        ("Thumb3_R", "DMZR03"),
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
        ("Thumb1_L", "DMZL01"),
        ("Thumb2_L", "DMZL02"),
        ("Thumb3_L", "DMZL03"),
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

def select_face_mesh():
    # Switch to Object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    
    # Look for meshes named 'face' or 'Face' and select them
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and obj.name in ['face', 'Face']:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            return obj
    return None

def get_shape_key_data(obj):
    # Return the shape key block that contains the shape keys, regardless of naming
    if obj.data.shape_keys:
        return obj.data.shape_keys
    return None

def manage_shape_keys(context):
    obj = select_face_mesh()
    if not obj:
        print("No mesh named 'face' or 'Face' found.")
        return
    
    shape_keys = get_shape_key_data(obj)
    if not shape_keys:
        print("No shape keys found on the object.")
        return

    # Check for required mouth shape keys
    required_mouth_keys = ["Mouth_A01", "Mouth_Line02", "Mouth_Open01"]
    mouth_keys_exist = all(key in shape_keys.key_blocks for key in required_mouth_keys)

    if not mouth_keys_exist:
        print("None of the required mouth shape keys exist. Stopping the script.")
        return
    
    # Function to create shape keys from a mix of existing ones
    def create_shape_key_from_mix(shape_key_name, shape_key_value_dict):
        for key_name, value in shape_key_value_dict.items():
            if key_name in shape_keys.key_blocks:
                shape_keys.key_blocks[key_name].value = value
        bpy.ops.object.shape_key_add(from_mix=True)
        shape_keys.key_blocks[-1].name = shape_key_name
        bpy.ops.object.shape_key_clear()


    # Create the specific mouth shape keys
    create_shape_key_from_mix("Ah", {"Mouth_A01": 1})
    create_shape_key_from_mix("Oh", {"Mouth_A01": 0.5, "Mouth_Line02": 1})
    create_shape_key_from_mix("Ch", {"Mouth_Open01": 1})

    # Create the blink shape keys
    create_shape_key_from_mix("Blink", {"Eye_WinkB_L": 1, "Eye_WinkB_R": 1})
    create_shape_key_from_mix("Blink Happy", {"Eye_WinkA_L": 1, "Eye_WinkA_R": 1})
    create_shape_key_from_mix("Blink Straight", {"Eye_WinkC_L": 1, "Eye_WinkC_R": 1})

    # Create the visemes using the specific keys
    create_shape_key_from_mix("vrc.v_aa", {"Ah": 1})  # aa = Ah:1
    create_shape_key_from_mix("vrc.v_ch", {"Ch": 1})   # ch = Ch:1
    create_shape_key_from_mix("vrc.v_dd", {"Ah": 0.3, "Ch": 0.7})  # dd = Ah:0.3 and Ch:0.7
    create_shape_key_from_mix("vrc.v_e", {"Ch": 0.5})   # e = Ch:0.5
    create_shape_key_from_mix("vrc.v_ff", {"Ah": 0.2, "Ch": 0.4})  # ff = Ah: 0.2 and Ch: 0.4
    create_shape_key_from_mix("vrc.v_ih", {"Ah": 0.5, "Ch": 0.2})  # ih = Ah: 0.5 and Ch: 0.2
    create_shape_key_from_mix("vrc.v_kk", {"Ah": 0.7, "Ch": 0.4})  # kk = Ah: 0.7 and Ch: 0.4
    create_shape_key_from_mix("vrc.v_nn", {"Ah": 0.2, "Ch": 0.7})  # nn = Ah: 0.2 and Ch: 0.7
    create_shape_key_from_mix("vrc.v_oh", {"Oh": 1})  # oh = Oh:1
    create_shape_key_from_mix("vrc.v_ou", {"Ah": 0.2, "Oh": 0.8})  # ou = Ah: 0.2 and Oh: 0.8
    create_shape_key_from_mix("vrc.v_pp", {"Ah": 0.0001})  # pp = Ah: 0.0001
    create_shape_key_from_mix("vrc.v_rr", {"Ch": 0.5, "Oh": 0.3})  # rr = Ch: 0.5 and Oh: 0.3
    create_shape_key_from_mix("vrc.v_sil", {"Ah": 0.0001})  # sil = Ah: 0.0001
    create_shape_key_from_mix("vrc.v_ss", {"Ch": 0.8})  # ss = Ch:0.8
    create_shape_key_from_mix("vrc.v_th", {"Ah": 0.4, "Oh": 0.15})  # th = Ah:0.4 and Oh:0.15

    # Set the shape key order directly using active_shape_key_index
    def set_shape_key_order(key_name, index):
        if key_name in shape_keys.key_blocks:
            obj.active_shape_key_index = shape_keys.key_blocks.find(key_name)
            # Move to requested position
            for _ in range(obj.active_shape_key_index - index):
                bpy.ops.object.shape_key_move(type='UP')

    # Reorder the shape keys
    set_shape_key_order("Blink", 1)
    set_shape_key_order("Blink Happy", 2)
    set_shape_key_order("Blink Straight", 3)
    set_shape_key_order("vrc.v_aa", 4)
    set_shape_key_order("vrc.v_ch", 5)
    set_shape_key_order("vrc.v_dd", 6)
    set_shape_key_order("vrc.v_e", 7)
    set_shape_key_order("vrc.v_ff", 8)
    set_shape_key_order("vrc.v_ih", 9)
    set_shape_key_order("vrc.v_kk", 10)
    set_shape_key_order("vrc.v_nn", 11)
    set_shape_key_order("vrc.v_oh", 12)
    set_shape_key_order("vrc.v_ou", 13)
    set_shape_key_order("vrc.v_pp", 14)
    set_shape_key_order("vrc.v_rr", 15)
    set_shape_key_order("vrc.v_sil", 16)
    set_shape_key_order("vrc.v_ss", 17)
    set_shape_key_order("vrc.v_th", 18)

    # Deselect all objects after the process
    bpy.ops.object.select_all(action='DESELECT')


def update_materials():
    # Function to set alpha mode to NONE for images
    def set_alpha_mode_none(image):
        if image and image.alpha_mode != 'NONE':
            image.alpha_mode = 'NONE'
            print(f"Set alpha mode to NONE for image '{image.name}'")

    # Select all mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')

    # Apply changes to all selected mesh objects
    selected_objects = bpy.context.selected_objects.copy()
    for obj in selected_objects:
        if obj.type == 'MESH':
            for mat_slot in obj.material_slots:
                if mat_slot.material and mat_slot.material.node_tree:
                    nodes = mat_slot.material.node_tree.nodes
                    # Find all image texture nodes
                    image_texture_nodes = [node for node in nodes if node.type == 'TEX_IMAGE']
                    for node in image_texture_nodes:
                        set_alpha_mode_none(node.image)

    # Deselect all mesh objects
    bpy.ops.object.select_all(action='DESELECT')

class RenameBonesOperator(bpy.types.Operator):
    """Renames bones in the selected object if in edit mode"""
    bl_idname = "object.rename_bones_operator"
    bl_label = "Rename Bones"

    def execute(self, context):
        rename_bones(context)
        batch_rename_bones()
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