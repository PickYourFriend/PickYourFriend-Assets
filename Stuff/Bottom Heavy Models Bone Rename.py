import bpy  # type: ignore

# Define the name mapping dictionary
bone_name_mapping = {
    "Spine0": "Hips",
    "Spine1": "Spine",
    "Spine2": "Chest",
    "Spine3": "Upper Chest",
    "Clavicle.L": "Left shoulder",
    "Clavicle.R": "Right shoulder",
    "Shoulder.L": "Left arm",
    "Shoulder.R": "Right arm",
    "Forearm.L": "Left elbow",
    "Forearm.R": "Right elbow",
    "Hand.L": "Left wrist",
    "Hand.R": "Right wrist",
    "Hip.L": "Left leg",
    "Hip.R": "Right leg",
    "Shin.L": "Left knee",
    "Shin.R": "Right knee"
}

# Iterate through all objects in the scene
for obj in bpy.data.objects:
    # Check if the object is an armature
    if obj.type == 'ARMATURE':
        # Enter edit mode to rename bones
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Iterate through each bone in the armature
        for bone in obj.data.edit_bones:
            # Check if the bone name exists in the mapping dictionary
            if bone.name in bone_name_mapping:
                # Rename the bone
                new_name = bone_name_mapping[bone.name]
                bone.name = new_name
                print(f"Renamed {bone.name} to {new_name}")
        
        # Return to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

print("Bone renaming complete.")
