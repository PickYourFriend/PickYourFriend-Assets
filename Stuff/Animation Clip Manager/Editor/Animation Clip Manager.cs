using UnityEditor;
using UnityEngine;
using System.Collections.Generic;

public class AnimationClipEditor : EditorWindow
{
    private Animator selectedAnimator; // Field for Animator
    private AnimationClip selectedClip;
    private Dictionary<string, EditorCurveBinding> bindings = new Dictionary<string, EditorCurveBinding>();
    private Dictionary<string, AnimationCurve> curves = new Dictionary<string, AnimationCurve>();
    private Vector2 scrollPosition;

    [MenuItem("PickYourFriend/Animation Clip Editor")]
    public static void ShowWindow()
    {
        GetWindow<AnimationClipEditor>("Animation Clip Editor");
    }

    private void OnGUI()
    {
        // Always display Animator field
        EditorGUILayout.LabelField("Select Animator", EditorStyles.boldLabel);
        selectedAnimator = (Animator)EditorGUILayout.ObjectField(selectedAnimator, typeof(Animator), true);

        // Always display Animation Clip field
        EditorGUILayout.LabelField("Select Animation Clip", EditorStyles.boldLabel);
        selectedClip = (AnimationClip)EditorGUILayout.ObjectField(selectedClip, typeof(AnimationClip), false);

        // Check if the selected clip is valid and retrieve curves
        if (selectedClip != null)
        {
            // Clear previous curves and get all curves from the selected animation clip
            bindings.Clear();
            curves.Clear();
            var editorBindings = AnimationUtility.GetCurveBindings(selectedClip);
            
            foreach (var binding in editorBindings)
            {
                AnimationCurve curve = AnimationUtility.GetEditorCurve(selectedClip, binding);
                bindings[binding.propertyName] = binding;
                curves[binding.propertyName] = curve;
            }

            // Create a scroll view for left and right hand values
            scrollPosition = EditorGUILayout.BeginScrollView(scrollPosition);
            EditorGUILayout.BeginHorizontal();

            // Left Hand Column
            EditorGUILayout.BeginVertical(GUILayout.Width(200));
            EditorGUILayout.LabelField("Left Hand", EditorStyles.boldLabel);
            if (GUILayout.Button("Copy Left to Right"))
            {
                CopyHandValues("LeftHand", "RightHand");
            }
            DisplayHandCurves("LeftHand");

            EditorGUILayout.EndVertical();

            // Right Hand Column
            EditorGUILayout.BeginVertical(GUILayout.Width(200));
            EditorGUILayout.LabelField("Right Hand", EditorStyles.boldLabel);
            if (GUILayout.Button("Copy Right to Left"))
            {
                CopyHandValues("RightHand", "LeftHand");
            }
            DisplayHandCurves("RightHand");

            EditorGUILayout.EndVertical();
            EditorGUILayout.EndHorizontal();
            EditorGUILayout.EndScrollView();
        }
    }

    private void DisplayHandCurves(string handPrefix)
    {
        string[] fingersOrder = new string[] { "Thumb", "Index", "Middle", "Ring", "Little" };

        foreach (var finger in fingersOrder)
        {
            List<KeyValuePair<string, AnimationCurve>> fingerCurves = new List<KeyValuePair<string, AnimationCurve>>();

            // Collect curves for the current finger
            foreach (var kvp in curves)
            {
                if (kvp.Key.StartsWith(handPrefix + "." + finger))
                {
                    fingerCurves.Add(kvp);
                }
            }

            // Sort curves for the current finger according to the desired order
            fingerCurves.Sort((a, b) => GetFingerCurveOrder(a.Key).CompareTo(GetFingerCurveOrder(b.Key)));

            // Display sorted curves for the current finger
            foreach (var kvp in fingerCurves)
            {
                DisplayCurve(kvp);
            }
        }
    }

    private int GetFingerCurveOrder(string propertyName)
    {
        if (propertyName.EndsWith("1 Stretched")) return 0;
        if (propertyName.EndsWith("2 Stretched")) return 1;
        if (propertyName.EndsWith("3 Stretched")) return 2;
        if (propertyName.EndsWith("Spread")) return 3;
        return 4; // Default case for unrecognized properties
    }

    private void DisplayCurve(KeyValuePair<string, AnimationCurve> kvp)
    {
        var curve = kvp.Value;
        string simpleName = GetSimplePropertyName(kvp.Key);
        bool isInAnimationMode = AnimationMode.InAnimationMode(); // Check if in animation mode

        // Create a horizontal layout for property name and value fields
        EditorGUILayout.BeginHorizontal();
        EditorGUILayout.LabelField(simpleName, GUILayout.Width(150));

        // Create fields for each keyframe
        for (int i = 0; i < curve.length; i++)
        {
            Keyframe key = curve[i];
            EditorGUI.BeginChangeCheck(); // Start tracking changes

            // Grayed out fields when not in play mode or animation mode
            GUI.enabled = EditorApplication.isPlaying || isInAnimationMode; 
            float newValue = EditorGUILayout.FloatField(key.value, GUILayout.Width(100));
            GUI.enabled = true; // Re-enable for future inputs

            // Check if the value has changed
            if (EditorGUI.EndChangeCheck())
            {
                // Record the state for undo/redo
                Undo.RecordObject(selectedClip, "Edit Animation Curve");

                // Update keyframe value directly
                key.value = newValue;
                curve.MoveKey(i, key);

                // Apply the updated curve back to the animation clip
                AnimationUtility.SetEditorCurve(selectedClip, bindings[kvp.Key], curve);
                EditorUtility.SetDirty(selectedClip); // Mark the animation clip as dirty

                // Force update the animator if needed
                if (selectedAnimator != null)
                {
                    selectedAnimator.Rebind(); // Ensure Animator updates
                }
            }
        }
        EditorGUILayout.EndHorizontal();
    }

    private string GetSimplePropertyName(string fullPropertyName)
    {
        // Simplify property names for display
        return fullPropertyName.Replace("LeftHand.", "").Replace("RightHand.", "").Replace(".", " ");
    }

    private void CopyHandValues(string sourcePrefix, string targetPrefix)
    {
        // Record the state for undo/redo
        Undo.RecordObject(selectedClip, "Copy Hand Values");

        foreach (var kvp in curves)
        {
            if (kvp.Key.StartsWith(sourcePrefix))
            {
                string targetKey = kvp.Key.Replace(sourcePrefix, targetPrefix);
                if (curves.ContainsKey(targetKey))
                {
                    AnimationCurve sourceCurve = kvp.Value;
                    AnimationCurve targetCurve = curves[targetKey];

                    for (int i = 0; i < sourceCurve.length; i++)
                    {
                        Keyframe key = sourceCurve[i];
                        targetCurve.MoveKey(i, new Keyframe(key.time, key.value));
                    }

                    AnimationUtility.SetEditorCurve(selectedClip, bindings[targetKey], targetCurve);
                    EditorUtility.SetDirty(selectedClip); // Mark the animation clip as dirty
                }
            }
        }
    }
}
