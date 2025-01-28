using UnityEditor;
using UnityEngine;
using VRC.SDK3.Avatars.Components;
using UnityEditor.Animations;  // To resolve AnimatorController

public class SetupVRCAvatarDescriptorFXLayers : EditorWindow
{
    private GameObject avatarDescriptorObject;
    private AnimatorController baseFX, additiveFX, gestureFX, actionFX, sittingFX, tposeFX;

    private const string PREF_BASE_FX = "BaseFX";
    private const string PREF_ADDITIVE_FX = "AdditiveFX";
    private const string PREF_GESTURE_FX = "GestureFX";
    private const string PREF_ACTION_FX = "ActionFX";
    private const string PREF_SITTING_FX = "SittingFX";
    private const string PREF_TPOSE_FX = "TPoseFX";

    [MenuItem("PickYourFriend/Setup FX Layers")]
    public static void ShowWindow()
    {
        GetWindow<SetupVRCAvatarDescriptorFXLayers>("Setup FX Layers");
    }

    private void OnEnable()
    {
        // Load saved paths
        baseFX = LoadAnimatorController(PREF_BASE_FX);
        additiveFX = LoadAnimatorController(PREF_ADDITIVE_FX);
        gestureFX = LoadAnimatorController(PREF_GESTURE_FX);
        actionFX = LoadAnimatorController(PREF_ACTION_FX);
        sittingFX = LoadAnimatorController(PREF_SITTING_FX);
        tposeFX = LoadAnimatorController(PREF_TPOSE_FX);
    }

    private void OnGUI()
    {
        GUILayout.Label("Setup VRC Avatar Descriptor FX Layers", EditorStyles.boldLabel);

        avatarDescriptorObject = (GameObject)EditorGUILayout.ObjectField("Avatar Descriptor", avatarDescriptorObject, typeof(GameObject), true);

        GUILayout.Label("FX Layers", EditorStyles.boldLabel);

        baseFX = (AnimatorController)EditorGUILayout.ObjectField("Base FX", baseFX, typeof(AnimatorController), false);
        additiveFX = (AnimatorController)EditorGUILayout.ObjectField("Additive FX", additiveFX, typeof(AnimatorController), false);
        gestureFX = (AnimatorController)EditorGUILayout.ObjectField("Gesture FX", gestureFX, typeof(AnimatorController), false);
        actionFX = (AnimatorController)EditorGUILayout.ObjectField("Action FX", actionFX, typeof(AnimatorController), false);
        sittingFX = (AnimatorController)EditorGUILayout.ObjectField("Sitting FX", sittingFX, typeof(AnimatorController), false);
        tposeFX = (AnimatorController)EditorGUILayout.ObjectField("TPose FX", tposeFX, typeof(AnimatorController), false);

        if (avatarDescriptorObject != null)
        {
            VRCAvatarDescriptor avatarDescriptor = avatarDescriptorObject.GetComponent<VRCAvatarDescriptor>();
            if (avatarDescriptor != null)
            {
                if (GUILayout.Button("Insert FX Layers"))
                {
                    InsertFXLayers(avatarDescriptor);
                }
            }
            else
            {
                EditorGUILayout.HelpBox("No VRCAvatarDescriptor found on the selected GameObject.", MessageType.Error);
            }
        }

        if (GUILayout.Button("Save FX Layers"))
        {
            SaveFXLayers();
        }
    }

    private void InsertFXLayers(VRCAvatarDescriptor avatarDescriptor)
    {
        if (baseFX != null) avatarDescriptor.baseAnimationLayers[0].animatorController = baseFX;
        if (additiveFX != null) avatarDescriptor.baseAnimationLayers[1].animatorController = additiveFX;
        if (gestureFX != null) avatarDescriptor.baseAnimationLayers[2].animatorController = gestureFX;
        if (actionFX != null) avatarDescriptor.baseAnimationLayers[3].animatorController = actionFX;

        // Special layers (Sitting and TPose)
        if (sittingFX != null) avatarDescriptor.specialAnimationLayers[0].animatorController = sittingFX;
        if (tposeFX != null) avatarDescriptor.specialAnimationLayers[1].animatorController = tposeFX;

        EditorUtility.SetDirty(avatarDescriptor);
        AssetDatabase.SaveAssets();
        Debug.Log("FX Layers inserted successfully.");
    }

    private void SaveFXLayers()
    {
        SaveAnimatorController(PREF_BASE_FX, baseFX);
        SaveAnimatorController(PREF_ADDITIVE_FX, additiveFX);
        SaveAnimatorController(PREF_GESTURE_FX, gestureFX);
        SaveAnimatorController(PREF_ACTION_FX, actionFX);
        SaveAnimatorController(PREF_SITTING_FX, sittingFX);
        SaveAnimatorController(PREF_TPOSE_FX, tposeFX);

        Debug.Log("FX Layers saved successfully.");
    }

    private AnimatorController LoadAnimatorController(string prefKey)
    {
        string path = EditorPrefs.GetString(prefKey, "");
        if (!string.IsNullOrEmpty(path))
        {
            return AssetDatabase.LoadAssetAtPath<AnimatorController>(path);
        }
        return null;
    }

    private void SaveAnimatorController(string prefKey, AnimatorController controller)
    {
        if (controller != null)
        {
            string path = AssetDatabase.GetAssetPath(controller);
            EditorPrefs.SetString(prefKey, path);
        }
    }
}
