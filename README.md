## AVL Tree Implementation

This project implements an AVL Tree in Python
### Files Included:

- **AVL_tree.py**: Contains the skeleton of the AVL tree implementation class.
- **test.py**: Test file to validate the implementation of various AVL tree methods.
- **print_tree.py**: Utility file for displaying the AVL tree structure in the console.

### AVL Tree Class Methods Implemented:

1. **search_node(self, value)**:
   - Performs binary search in the AVL tree to find a node with the specified value.
   - Returns the path from the root to the found node, indicating the direction taken at each step ('l' for left, 'r' for right, 'o' for root).

2. **compute_height(self, t)**:
   - Recomputes the height of a node and checks for imbalance between its left and right children.
   - Returns `True` if the node is unbalanced, `False` otherwise.

3. **rotation_tree(self, a, z, y, x)**:
   - Applies rotation movement to adjust the AVL tree structure after insertion or deletion.
   - Updates node heights accordingly.

4. **backtrack_height_from_add(self, path)**:
   - Checks for and corrects any imbalance in the AVL tree after adding a node.
   - Takes the path from the root to the newly added node as input.

5. **backtrack_height_from_remove(self, path)**:
   - Checks for and corrects any imbalance in the AVL tree after removing a node.
   - Takes the path from the root to the removed node (or its replacement) as input.

6. **add_node(self, value)**:
   - Adds a node with the specified value to the AVL tree.
   - Returns the node created or `None` if the value is already present in the tree.

7. **remove_node(self, value)**:
   - Removes a node with the specified value from the AVL tree.
   - Returns the removed node or `None` if no such node exists in the tree.

### Usage:

1. Clone the repository and place all files in your working directory.
   
2. Ensure Python 3.x is installed on your system.

3. Run `test.py` to execute the test cases and validate the functionality of the AVL tree methods.

```bash
python test.py
```

### Notes:

- Ensure all files (`AVL_tree.py`, `test.py`, and `print_tree.py`) are in the same directory for proper functionality.
- Comment your code thoroughly to assist in understanding and grading.
