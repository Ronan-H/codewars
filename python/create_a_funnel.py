
class Node(object):
    def __init__(self, value=None, parent=None, left_child=None, right_child=None):
        self.value = None if value is None else str(value)
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.visited = False

    def is_empty(self):
        return self.value is None

    def is_top_level(self):
        return self.left_child is None

    def is_empty_or_top_level(self):
        return self.is_empty() or self.is_top_level()

    def has_value(self):
        return self.value is not None

    def is_leaf(self):
        return self.is_top_level() or not (self.left_child.has_value() or self.right_child.has_value())

    def num_children_recursive(self):
        if self.is_empty():
            return 0

        if self.is_top_level():
            return 1

        self.visited = True

        children = [p for p in [self.left_child, self.right_child] if p.has_value() and not p.visited]
        for child in children:
            child.visited = True
        return (1 if self.has_value() else 0) + sum(p.num_children_recursive() for p in children)

    def drip(self):
        original_value = self.value

        if self.is_empty_or_top_level():
            self.value = None
        else:
            num_children_left = self.left_child.num_children_recursive()
            self.reset_visited_recursive()
            num_children_right = self.right_child.num_children_recursive()
            self.reset_visited_recursive()

            if num_children_left >= num_children_right:
                self.value = self.left_child.drip()
            else:
                self.value = self.right_child.drip()

        return original_value

    def reset_visited_recursive(self):
        self.visited = False

        if not self.is_top_level():
            self.left_child.reset_visited_recursive()
            self.right_child.reset_visited_recursive()

    def __str__(self):
        return str(self.value) if self.has_value() else ' '


class Funnel(object):
    def __init__(self):
        self.count = 0
        # create and link up nodes for each funnel value space
        prev_level = [Node() for _ in range(5)]
        for i in range(4, 0, -1):
            level = [Node() for _ in range(i)]

            for j, parent in enumerate(level):
                parent.left_child = prev_level[j]
                parent.right_child = prev_level[j + 1]

            prev_level = level

        self.root = prev_level[0]

    def fill(self, *args):
        for value in args:
            self.fill_one(value)

    def fill_one(self, value):
        if self.count < 15:
            if self.root.is_empty():
                self.root.value = value
            else:
                pool = [self.root]
                space_found = False

                while not space_found:
                    for i, node in enumerate(pool):
                        if node.left_child.is_empty():
                            node.left_child.value = value
                            space_found = True
                            break
                        elif node.right_child.is_empty():
                            node.right_child.value = value
                            space_found = True
                            break

                    children = [n.left_child for n in pool] + [pool[-1].right_child]
                    pool = children

            self.count += 1

    def drip(self):
        if self.count == 0:
            return None

        self.count -= 1
        return self.root.drip()

    def get_levels(self):
        pool = [self.root]
        levels = []

        levels.insert(0, pool)
        for i in range(4):
            pool = [n.left_child for n in pool] + [pool[-1].right_child]
            levels.insert(0, pool)

        return levels

    def __str__(self):
        s = ''
        levels = self.get_levels()

        for i, level in enumerate(levels):
            s += ' ' * i
            s += '\\'
            s += ' '.join([str(n) for n in level])
            s += '/\n'

        return s[:-1]


funnel = Funnel()
# for i in range(1, 10):
#     print(f'Filling with {i}:')
#     funnel.fill(i)
#     print(funnel)

funnel.fill(1, 2, 3)
funnel.drip()
funnel.fill(4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')
print(funnel)

# for i in range(9):
#     print('Dripping...')
#     value = funnel.drip()
#     print(funnel)
#     print(f'Yielded value: {value}')