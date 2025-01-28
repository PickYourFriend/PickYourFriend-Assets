import bpy

def select_face_mesh():
    # Finds and selects the 'face' or 'Face' mesh in the scene
    obj = bpy.context.scene.objects.get('face') or bpy.context.scene.objects.get('Face')
    if obj:
        bpy.context.view_layer.objects.active = obj
        return obj
    return None

def get_shape_key_data(obj):
    # Returns the shape key data if available
    if obj and obj.data.shape_keys:
        return obj.data.shape_keys
    return None

def create_shape_key_from_mix(shape_key_name, shape_key_value_dict):
    obj = select_face_mesh()
    if not obj:
        print("No mesh named 'face' or 'Face' found.")
        return
    shape_keys = get_shape_key_data(obj)
    if not shape_keys:
        print("No shape keys found on the object.")
        return

    for key_name, value in shape_key_value_dict.items():
        if key_name in shape_keys.key_blocks:
            shape_keys.key_blocks[key_name].value = value
    bpy.ops.object.shape_key_add(from_mix=True)
    shape_keys.key_blocks[-1].name = shape_key_name
    bpy.ops.object.shape_key_clear()

def set_shape_key_order(key_name, index):
    """Sets the order of the shape key in the stack."""
    obj = select_face_mesh()
    if obj and obj.data.shape_keys:
        shape_keys = obj.data.shape_keys.key_blocks
        if key_name in shape_keys:
            key_block = shape_keys[key_name]
            current_index = list(shape_keys).index(key_block)
            obj.active_shape_key_index = current_index

            for _ in range(abs(current_index - index)):
                if current_index > index:
                    bpy.ops.object.shape_key_move(type='UP')
                elif current_index < index:
                    bpy.ops.object.shape_key_move(type='DOWN')

def manage_shape_keys():
    obj = select_face_mesh()
    if not obj:
        print("No mesh named 'face' or 'Face' found.")
        return
    
    shape_keys = get_shape_key_data(obj)
    if not shape_keys:
        print("No shape keys found on the object.")
        return

    # Create Blink variations
    create_shape_key_from_mix("Blink", {"Eye_WinkB_L": 1, "Eye_WinkB_R": 1})
    create_shape_key_from_mix("Blink Happy", {"Eye_WinkA_L": 1, "Eye_WinkA_R": 1})
    create_shape_key_from_mix("Blink Straight", {"Eye_WinkC_L": 1, "Eye_WinkC_R": 1})

    # Create Ah, Oh, and Ch
    create_shape_key_from_mix("Ah", {"Mouth_A01": 1})
    create_shape_key_from_mix("Oh", {"Mouth_A01": 0.5, "Mouth_Line02": 1})
    create_shape_key_from_mix("Ch", {"Mouth_Open01": 1})

    # Create VRC-specific phoneme shapes
    create_shape_key_from_mix("vrc.v_aa", {"Ah": 1})
    create_shape_key_from_mix("vrc.v_ch", {"Ch": 1})
    create_shape_key_from_mix("vrc.v_dd", {"Ah": 0.3, "Ch": 0.7})
    create_shape_key_from_mix("vrc.v_e", {"Ch": 0.5})
    create_shape_key_from_mix("vrc.v_ff", {"Ah": 0.2, "Ch": 0.4})
    create_shape_key_from_mix("vrc.v_ih", {"Ah": 0.5, "Ch": 0.2})
    create_shape_key_from_mix("vrc.v_kk", {"Ah": 0.7, "Ch": 0.4})
    create_shape_key_from_mix("vrc.v_nn", {"Ah": 0.2, "Ch": 0.7})
    create_shape_key_from_mix("vrc.v_oh", {"Oh": 1})
    create_shape_key_from_mix("vrc.v_ou", {"Ah": 0.2, "Oh": 0.8})
    create_shape_key_from_mix("vrc.v_pp", {"Ah": 0.0001})
    create_shape_key_from_mix("vrc.v_rr", {"Ch": 0.5, "Oh": 0.3})
    create_shape_key_from_mix("vrc.v_sil", {"Ah": 0.0001})
    create_shape_key_from_mix("vrc.v_ss", {"Ch": 0.8})
    create_shape_key_from_mix("vrc.v_th", {"Ah": 0.4, "Oh": 0.15})

    # Reorder the shape keys starting from Blink
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

# Automatically run the script
if __name__ == "__main__":
    manage_shape_keys()
