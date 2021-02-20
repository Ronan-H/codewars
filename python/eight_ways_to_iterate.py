
DIRECTION_UP, DIRECTION_LEFT, DIRECTION_DOWN, DIRECTION_RIGHT = range(1,5)

class Table:
    def __init__(self,data):
        self.data = data

    def walk(self, dir0, dir1):
        height = len(self.data)
        width = len(self.data[0])
        
        dirs = [dir0, dir1]
        going_right = DIRECTION_RIGHT in dirs
        going_down = DIRECTION_DOWN in dirs
        
        x_start = 0 if going_right else width - 1
        y_start = 0 if going_down else height - 1
        x_step = 1 if going_right else -1
        y_step = 1 if going_down else -1
        x_stop = width if going_right else -1
        y_stop = height if going_down else -1
        
        y_range = range(y_start, y_stop, y_step)
        x_range = range(x_start, x_stop, x_step)
        
        column_first = dir0 in [DIRECTION_LEFT, DIRECTION_RIGHT]
        
        if column_first:
            for y in y_range:
                for x in x_range:
                    yield self.data[y][x]
        else:
            for x in x_range:
                for y in y_range:
                    yield self.data[y][x]
