from copy import deepcopy

def edge_detection(rle):
    image = Image([int(s) for s in rle.split(" ")])
    image.edge_detect()
    return image.to_rle()


class Image:
    def __init__(self, rle):
        self.w = rle[0]
        self.h = sum(rle[2::2])
        self.img = [n for seq in [[rle[i]] * rle[i + 1] for i in range(1, len(rle), 2)] for n in seq]
        #print("Input img: ", self.img)
        self.len = len(self.img)

    def edge_detect(self):
        copy = []

        for i in range(self.len):
            copy.append(self.edge_detect_index(i))

        self.img = copy

    def edge_detect_index(self, index):
        highest = None

        for y_off in range(-1, 2):
            for x_off in range(-1, 2):
                if x_off == y_off == 0:
                    continue

                off_index = index + x_off

                if off_index // self.w != index // self.w:
                    continue

                off_index += (y_off * self.w)

                if 0 <= off_index < self.len:
                    val = abs(self.img[index] - self.img[off_index])
                    if highest is None or val > highest:
                        highest = val

        return highest

    def to_rle(self):
        #print("Processed img: ", self.img)
        result = [self.w]
        on = self.img[0]
        counter = 1

        for v in self.img[1:]:
            if v != on:
                result.append(on)
                result.append(counter)
                on = v
                counter = 0
            counter += 1

        result.append(on)
        result.append(counter)

        return result


#print("Input : ", [int(s) for s in "7 15 4 100 15 25 2 175 2 25 5 175 2 25 5".split(" ")])
#print("Result: ", edge_detection("7 15 4 100 15 25 2 175 2 25 5 175 2 25 5"))
#print("Actual: ", [int(s) for s in "7 85 5 0 2 85 5 75 10 150 2 75 3 0 2 150 2 0 4".split(" ")])

print(edge_detection("10 35 500000000 200 500000000"))