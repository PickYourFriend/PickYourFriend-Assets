import bpy

# Define constants
REMOVABLE_IDENTIFIERS = ["JNT", "Bip", "BIP"]
LEFT_IDENTIFIER = "Left"
RIGHT_IDENTIFIER = "Right"
SHORT_LEFT = "L"
SHORT_RIGHT = "R"
IGNORED_WORDS = ["Root"]  # Bones containing these words will be skipped

def clean_bone_names():
    """Part 1: Remove unwanted keywords and fix underscores in bone names."""
    armature = bpy.context.active_object

    if armature is None or armature.type != 'ARMATURE':
        print("Error: Select an armature object in Object Mode.")
        return

    bpy.ops.object.mode_set(mode='EDIT')

    for bone in armature.data.edit_bones:
        original_name = bone.name
        if any(ignored in original_name for ignored in IGNORED_WORDS):
            print(f"Skipping bone (contains ignored word): {original_name}")
            continue

        new_name = original_name
        for word in REMOVABLE_IDENTIFIERS:
            new_name = new_name.replace(word, "")

        new_name = new_name.strip("_").replace("__", "_")

        if new_name != original_name:
            bone.name = new_name
            print(f"Cleaned bone name: {original_name} -> {new_name}")

    print("Part 1: Bone cleaning complete.")

def rearrange_left_right_identifiers():
    """Part 2: Ensure 'L' or 'R' are at the end, handling 'Left' and 'Right' inside names."""
    armature = bpy.context.active_object

    if armature is None or armature.type != 'ARMATURE':
        print("Error: Select an armature object in Object Mode.")
        return

    bpy.ops.object.mode_set(mode='EDIT')

    for bone in armature.data.edit_bones:
        original_name = bone.name
        if any(ignored in original_name for ignored in IGNORED_WORDS):
            print(f"Skipping bone (contains ignored word): {original_name}")
            continue

        if original_name.endswith("_L") or original_name.endswith("_R"):
            print(f"Skipping bone (already ends with _L or _R): {original_name}")
            continue

        new_name = original_name

        # If "Left" or "Right" is at the start, do nothing
        if new_name.startswith(LEFT_IDENTIFIER) or new_name.startswith(RIGHT_IDENTIFIER):
            print(f"Skipping bone (Left/Right at start): {original_name}")
            continue

        # If "Left" or "Right" is in the middle or at the end, move it to the end
        if LEFT_IDENTIFIER in new_name:
            new_name = new_name.replace(LEFT_IDENTIFIER, "").strip("_") + "_L"
        elif RIGHT_IDENTIFIER in new_name:
            new_name = new_name.replace(RIGHT_IDENTIFIER, "").strip("_") + "_R"

        if new_name != original_name:
            bone.name = new_name
            print(f"Reformatted bone name: {original_name} -> {new_name}")

    print("Part 2: Left/Right rearrangement complete.")

def clean_double_underscores_and_suffixes():
    """Part 3: Replace double underscores and fix numbered suffixes."""
    armature = bpy.context.active_object

    if armature is None or armature.type != 'ARMATURE':
        print("Error: Select an armature object in Object Mode.")
        return

    bpy.ops.object.mode_set(mode='EDIT')

    sequential_counter = 1  

    for bone in armature.data.edit_bones:
        original_name = bone.name
        if any(ignored in original_name for ignored in IGNORED_WORDS):
            print(f"Skipping bone (contains ignored word): {original_name}")
            continue

        new_name = original_name.replace("__", "_")

        if "." in new_name and new_name.split(".")[-1].isdigit():
            new_name = ".".join(new_name.split(".")[:-1])

            if new_name.endswith("_L") or new_name.endswith("_R"):
                new_name = new_name[:-2] + f"_{sequential_counter}" + new_name[-2:]
            else:
                new_name = new_name + f"_{sequential_counter}"

            sequential_counter += 1

        if new_name != original_name:
            bone.name = new_name
            print(f"Fixed suffix and cleaned name: {original_name} -> {new_name}")

    print("Part 3: Double underscore cleanup and suffix handling complete.")

def main():
    clean_bone_names()  
    rearrange_left_right_identifiers()  
    clean_double_underscores_and_suffixes()  
    bpy.ops.object.mode_set(mode='OBJECT')  
    print("Bone renaming process completed successfully.")

main()
