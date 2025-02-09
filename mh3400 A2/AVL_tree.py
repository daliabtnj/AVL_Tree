# class that represents a tree node
class Node:
    def __init__(self, height, left, right, key):
        self.height = height   
        self.left = left      
        self.right = right    
        self.key = key          


# class that represents an AVL tree
class AVL_tree:
    
    def __init__(self, root):
        self.root = root    # root node (Node or None)
    
    def search_node(self, value):
        stack = []
        t = self.root
        stack.append([t, 'o'])  
        
        while True:
            if t is None:
                return stack  
            if value > t.key:
                t = t.right
                stack.append([t, 'r'])
            elif value < t.key:
                t = t.left
                stack.append([t, 'l'])
            else:
                return stack 


    # method that recomputes the height of a node t based on the heights of its children, and checks if there is an unbalance
    # difference in children heights > 1 returns true if unbalanced, false otherwise
 
    def compute_height(self, t):
        if t is None:
            return False

        left_h = t.left.height if t.left else 0
        right_h = t.right.height if t.right else 0
        t.height = 1 + max(left_h, right_h)

        # unbalanced if difference > 1
        return abs(left_h - right_h) > 1

    # Helper function : left rotation around node z. after rotation, return new root of that rotated subtree 

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        
        # perform rotation
        y.left = z
        z.right = T2
        
        # update heights
        self.compute_height(z)
        self.compute_height(y)
        return y

    # Helper function : right rotation around node z. after rotation, return new root of that rotated subtree 

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        
        # perform rotation
        y.right = z
        z.left = T3
        
        # update heights
        self.compute_height(z)
        self.compute_height(y)
        return y


    # rotation_tree(a, z, y, x) identifies which of the 4 AVL rotations (LL, LR, RR, RL) to apply based on z->y->x direction, then reattaches the rotated subtree to 'a'.
    def rotation_tree(self, a, z, y, x):
        # if y is z.left (left heavy) or z.right (right heavy)
        left_heavy = (y == z.left)
        # if x is y.left or y.right
        x_left_child = (x == y.left)
        
        # new root of the z-subtree after rotation(s)
        new_subroot = None

        # 1: Left-Left
        if left_heavy and x_left_child:
            new_subroot = self.right_rotate(z)
        # 2: Left-Right
        elif left_heavy and not x_left_child:
            z.left = self.left_rotate(y)
            new_subroot = self.right_rotate(z)
        # 3: Right-Right
        elif not left_heavy and not x_left_child:
            new_subroot = self.left_rotate(z)
        # 4: Right-Left
        else:
            z.right = self.right_rotate(y)
            new_subroot = self.left_rotate(z)

        # reattach new_subroot to 'a'
        if a is None:
            # z was the root
            self.root = new_subroot
        else:
            # see if z was left or right child of a
            if a.left == z:
                a.left = new_subroot
            else:
                a.right = new_subroot


    # we go bottom-up along path and fix the first unbalance 

    def backtrack_height_from_add(self, path):
        # bottom-up
        for i in range(len(path) - 1, -1, -1):
            curr_node = path[i][0]
            if curr_node is None:
                continue
            unbalanced = self.compute_height(curr_node)
            if unbalanced:
                z = curr_node
                a = path[i-1][0] if i > 0 else None

                # pick y the heavier child
                left_h = z.left.height if z.left else 0
                right_h = z.right.height if z.right else 0
                if left_h >= right_h:
                    y = z.left
                else:
                    y = z.right

                # pick x the heavier child of y
                left_h_y = y.left.height if y.left else 0
                right_h_y = y.right.height if y.right else 0
                if left_h_y >= right_h_y:
                    x = y.left
                else:
                    x = y.right

                self.rotation_tree(a, z, y, x)
                break  # stop after first rotation

    # helper, collect all nodes 
    def get_all_nodes_postorder(self, root, out_list):
        """Postorder traversal to get all nodes in bottom-up order."""
        if root is None:
            return
        self.get_all_nodes_postorder(root.left, out_list)
        self.get_all_nodes_postorder(root.right, out_list)
        out_list.append(root)

    # helper, find a node's parent by key 
    def find_parent(self, child_node):
        """Return the parent of child_node (or None if child_node is root)."""
        if child_node is None or child_node == self.root:
            return None
        return self._find_parent_dfs(self.root, child_node)

    def _find_parent_dfs(self, current, target):
        if current is None:
            return None
        if current.left == target or current.right == target:
            return current
        # search down the correct branch
        if target.key < current.key:
            return self._find_parent_dfs(current.left, target)
        else:
            return self._find_parent_dfs(current.right, target)

    # re‐check all nodes for imbalance after removal

    def backtrack_height_from_remove(self, path):
        while True:
            rotated_something = False
            # postorder list of all nodes
            all_nodes = []
            self.get_all_nodes_postorder(self.root, all_nodes)

            for node in all_nodes:
                if self.compute_height(node):
                    # node is unbalanced 
                    z = node
                    a = self.find_parent(z)

                    # pick heavier child y
                    lh = z.left.height if z.left else 0
                    rh = z.right.height if z.right else 0
                    y = z.left if lh >= rh else z.right
                    # pick heavier child x
                    lhy = y.left.height if y.left else 0
                    rhy = y.right.height if y.right else 0
                    x = y.left if lhy >= rhy else y.right

                    self.rotation_tree(a, z, y, x)
                    rotated_something = True
                    break  # break out of for-loop, then re-check everything

            if not rotated_something:
                break  # no more unbalances found, done


    # Add a node. returns the newly created node if success, or none if the value is already in the tree.

    def add_node(self, value):
        # find place with search_node
        path = self.search_node(value)
        last_node = path[-1][0]

        # if found existing key do nothing
        if last_node is not None and last_node.key == value:
            return None

        new_node = Node(1, None, None, value)
        
        # if tree was empty
        if last_node is None and len(path) == 1 and path[0][1] == 'o':
            self.root = new_node
            path[-1][0] = new_node
        else:
            # get direction & parent
            direction = path[-1][1]
            parent = path[-2][0] if len(path) >= 2 else None

            # remove the last [None, direction]
            path.pop()

            # attach new_node to parent
            if parent is None:
                self.root = new_node
            else:
                if direction == 'l':
                    parent.left = new_node
                else:
                    parent.right = new_node

            path.append([new_node, direction])

        # rebalance up the path
        self.backtrack_height_from_add(path)
        return new_node

    # Remove a node with the given value

    def remove_node(self, value):
        # search for node
        path = self.search_node(value)
        last_node = path[-1][0]

        if last_node is None or last_node.key != value:
            return None  # not found

        removed_node = last_node

        # 1 : node has 2 children
        if last_node.left and last_node.right:
            # find successor = min in right subtree
            successor = last_node.right
            successor_path = [[successor, 'r']]
            while successor.left:
                successor = successor.left
                successor_path.append([successor, 'l'])
            
            # copy successor's key into last_node
            last_node.key = successor.key
            # remove successor node ,it has at most 1 child
            subpath = self.search_node(successor.key)
            self._remove_node_no_two_children(successor.key, subpath)

            # rebuild path to last_node which changed key,
            # backtrack for rebalancing
            new_path = self.search_node(last_node.key)
            self.backtrack_height_from_remove(new_path)

        else:
            # CASE B: node has <= 1 child
            self._remove_node_no_two_children(value, path)
            
            # then check rebalancing
            new_path = self.search_node(value)  # ends with None if truly removed
            self.backtrack_height_from_remove(new_path)

        return removed_node


    # Internal helper to remove a node that has at most 1 child.
    def _remove_node_no_two_children(self, value, path):
        node_to_remove = path[-1][0]
        if node_to_remove is None:
            return

        # find parent if any
        parent = None
        if len(path) >= 2:
            parent = path[-2][0]

        # find the single child if it exists
        child = None
        if node_to_remove.left and not node_to_remove.right:
            child = node_to_remove.left
        elif node_to_remove.right and not node_to_remove.left:
            child = node_to_remove.right

        # if removing the root
        if parent is None:
            self.root = child
        else:
            # see if node_to_remove was parent's left or right
            if parent.left == node_to_remove:
                parent.left = child
            else:
                parent.right = child

        # cut references from node_to_remove
        node_to_remove.left = None
        node_to_remove.right = None