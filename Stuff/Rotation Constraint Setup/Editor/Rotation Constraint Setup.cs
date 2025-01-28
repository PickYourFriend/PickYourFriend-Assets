using UnityEngine;
using UnityEngine.Animations;
using UnityEditor;

public class RotationConstraintWindow : EditorWindow
{
    private GameObject sourceRoot;
    private GameObject targetRoot;

    [MenuItem("PickYourFriend/Rotation Constraint Tool")]
    public static void ShowWindow()
    {
        GetWindow<RotationConstraintWindow>("Rotation Constraint Tool");
    }

    private void OnGUI()
    {
        GUILayout.Label("Setup Constraints", EditorStyles.boldLabel);

        sourceRoot = (GameObject)EditorGUILayout.ObjectField("Source Hierarchy", sourceRoot, typeof(GameObject), true);
        targetRoot = (GameObject)EditorGUILayout.ObjectField("Target Hierarchy", targetRoot, typeof(GameObject), true);

        if (GUILayout.Button("Add Constraints"))
        {
            if (sourceRoot == null || targetRoot == null)
            {
                Debug.LogError("Please assign both source and target hierarchies.");
            }
            else
            {
                AddConstraintsRecursively(sourceRoot.transform, targetRoot.transform);
            }
        }

        GUILayout.Space(10);

        if (GUILayout.Button("Remove All Constraints"))
        {
            if (sourceRoot == null)
            {
                Debug.LogError("Please assign a source hierarchy to remove constraints from.");
            }
            else
            {
                RemoveConstraintsRecursively(sourceRoot.transform);
            }
        }
    }

    private void AddConstraintsRecursively(Transform source, Transform target)
    {
        if (target == null)
        {
            Debug.LogError($"Target hierarchy does not match source hierarchy at {source.name}");
            return;
        }

        if (source.name == "Hips")
        {
            // Add a ParentConstraint to the source object
            ParentConstraint parentConstraint = source.gameObject.AddComponent<ParentConstraint>();
            ConstraintSource constraintSource = new ConstraintSource
            {
                sourceTransform = target,
                weight = 1f
            };
            parentConstraint.AddSource(constraintSource);
            parentConstraint.constraintActive = true; // Constraint is active
            parentConstraint.enabled = false; // Component is disabled
        }
        else
        {
            // Add a RotationConstraint to the source object
            RotationConstraint rotationConstraint = source.gameObject.AddComponent<RotationConstraint>();
            ConstraintSource constraintSource = new ConstraintSource
            {
                sourceTransform = target,
                weight = 1f
            };
            rotationConstraint.AddSource(constraintSource);
            rotationConstraint.constraintActive = true; // Constraint is active
            rotationConstraint.enabled = false; // Component is disabled
        }

        // Recursively add constraints to all children
        for (int i = 0; i < source.childCount; i++)
        {
            Transform childSource = source.GetChild(i);
            Transform childTarget = target.Find(childSource.name);

            AddConstraintsRecursively(childSource, childTarget);
        }
    }

    private void RemoveConstraintsRecursively(Transform source)
    {
        // Remove RotationConstraint
        RotationConstraint rotationConstraint = source.GetComponent<RotationConstraint>();
        if (rotationConstraint != null)
        {
            DestroyImmediate(rotationConstraint);
        }

        // Remove ParentConstraint
        ParentConstraint parentConstraint = source.GetComponent<ParentConstraint>();
        if (parentConstraint != null)
        {
            DestroyImmediate(parentConstraint);
        }

        for (int i = 0; i < source.childCount; i++)
        {
            Transform childSource = source.GetChild(i);
            RemoveConstraintsRecursively(childSource);
        }
    }
}
