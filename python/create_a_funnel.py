
class Node(object):
    def __init__(self, value, parent=None, left_child=None, right_child=None):
        self.value = str(value)
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child

    def is_leaf(self):
        return self.left_child is None and self.right_child is None

    def num_children_recursive(self):
        if self.is_leaf():
            return 0

        children = [p for p in [self.left_child, self.right_child] if p is not None]
        return len(children) + sum(p.num_children_recursive() for p in children)

    def safe_left_child(self):
        return self.left_child if self.left_child is not None else Node(' ')

    def safe_right_child(self):
        return self.right_child if self.right_child is not None else Node(' ')

    def drip(self):
        original_value = self.value

        if self.left_child is None and self.right_child is None:
            return None

        if self.left_child.num_children_recursive() >= self.right_child.num_children_recursive():
            val = self.left_child.drip()
            if val is None:
                pass
            else:
                self.value = val
        else:
            self.value = self.right_child.drip()

        return original_value


class Funnel(object):
    def __init__(self):
        self.count = 0
        self.root = None

    def fill(self, *args):
        for value in args:
            self.fill_one(value)

    def fill_one(self, value):
        new_node = Node(value)
        if self.count < 15:
            if self.root is None:
                self.root = new_node
            else:
                pool = [self.root]
                space_found = False

                while not space_found:
                    for i, node in enumerate(pool):
                        if node.left_child is None:
                            node.left_child = new_node
                            space_found = True
                            break
                        elif node.right_child is None:
                            node.right_child = new_node
                            space_found = True

                            if i < len(pool) - 1:
                                pool[i + 1].left_child = new_node
                            break

                    children = [n.left_child for n in pool] + [pool[-1].right_child]
                    pool = children

            self.count += 1

    def drip(self):
        if self.count == 0:
            return None

        return self.root.drip()

    def get_levels(self):
        pool = [self.root]
        levels = []

        levels.insert(0, [n.value for n in pool])
        for i in range(4):
            pool = [n.safe_left_child() for n in pool] + [pool[-1].safe_right_child()]
            levels.insert(0, [n.value for n in pool])

        return levels

    def __str__(self):
        s = ''
        levels = self.get_levels()

        for i, level in enumerate(levels):
            s += ' ' * i
            s += '\\'
            s += ' '.join(level)
            s += '/\n'

        return s


funnel = Funnel()
for i in range(10):
    funnel.fill(i)
    print(funnel)