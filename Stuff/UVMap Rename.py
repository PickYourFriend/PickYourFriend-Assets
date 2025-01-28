import bpy # type: ignore

# Iterate through all objects in the Blender scene
for obj in bpy.data.objects:
    # Check if the object is a mesh
    if obj.type == 'MESH':
        # Iterate through all UV maps in the mesh
        for uv_map in obj.data.uv_layers:
            # Rename UV maps based on their current name
            if uv_map.name == "TEXCOORD.xy":
                uv_map.name = "UV0"
            elif uv_map.name == "TEXCOORD1.xy":
                uv_map.name = "UV1"

print("UV map renaming complete.")
