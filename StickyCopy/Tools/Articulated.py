import math

from PIL import ImageDraw2, Image


class Attributes:
    def __init__(self, circle=False, color="blue"):
        self.circle = circle
        self.color = color


class Node:
    def __init__(self, parent, length, deg, name=None, attributes=None):
        self.children = []
        self.name = name
        self.attributes = attributes
        self.length = length
        self.alpha = deg * math.pi / 180.
        self.parent = parent
        self.position = self.get_position()

    def add(self, length, deg, name=None, attributes=None):
        child = Node(self, length, deg, name, attributes)
        self.children.append(child)
        return child

    def set_angle(self, deg):
        self.alpha = deg * math.pi / 180.
        self.recalculate()

    def get_nodes(self):
        ret_list = [self]
        for child in self.children:
            ret_list.extend(child.get_nodes())
        return ret_list

    def find(self, name):
        if self.name == name:
            return self
        for child in self.children:
            node = child.find(name)
            if node is not None:
                return node
        return None

    def get_position(self):
        anchor = self.parent.position
        sin = math.sin(self.alpha)
        cos = math.cos(self.alpha)
        return (anchor[0] + sin * self.length, anchor[1] - cos * self.length)

    def recalculate(self):
        self.position = self.get_position()
        for child in self.children:
            child.recalculate()


class Root:
    def __init__(self, position=(300, 300)):
        self.position = position
        self.children = []
        self.draw = Draw(self)

    def add(self, length, deg, name=None, attributes=None) -> Node:
        child = Node(self, length, deg, name, attributes)
        self.children.append(child)
        return child

    def set_position(self, position):
        self.position = position
        self.recalculate()

    def get_position(self):
        return self.position

    def get_nodes(self):
        ret_list = [self]
        for child in self.children:
            ret_list.extend(child.get_nodes())
        return ret_list

    def find(self, name):
        for child in self.children:
            node = child.find(name)
            if node is not None:
                return node
        return None

    def recalculate(self):
        for child in self.children:
            child.recalculate()


class Draw:
    def __init__(self, root: Root):
        self.root = root

    def draw(self, image, shadow=False):
        for child in self.root.children:
            self._draw_sticks(image, child, shadow)
        if not shadow:
            self._draw_joints(image, self.root)

    def _draw_sticks(self, image, node: Node, shadow=False):
        canvas = ImageDraw2.Draw(image)
        if shadow:
            color = "grey"
        else:
            color = "blue" if node.attributes is None else node.attributes.color
        pen = ImageDraw2.Pen(color, width=7, opacity=125)
        brush = ImageDraw2.Brush(color, 125)
        if node.attributes is None or not node.attributes.circle:
            canvas.line(node.parent.position + node.position, pen)
        else:
            pos = ((node.position[0] + node.parent.position[0]) / 2, (node.position[1] + node.parent.position[1]) / 2)
            r = math.sqrt(
                (node.position[0] - node.parent.position[0]) ** 2 + (
                    node.position[1] - node.parent.position[1]) ** 2) / 2
            canvas.ellipse((pos[0] - r, pos[1] - r, pos[0] + r, pos[1] + r), pen, brush)
        canvas.flush()
        for child in node.children:
            self._draw_sticks(image, child, shadow)

    def _draw_joints(self, image, node: Node):
        canvas = ImageDraw2.Draw(image)
        brush = ImageDraw2.Brush("red", 125)
        pos = node.position
        canvas.ellipse((pos[0] - 3.5, pos[1] - 3.5, pos[0] + 3.5, pos[1] + 3.5), None, brush)
        canvas.flush()
        for child in node.children:
            self._draw_joints(image, child)


class Stickman:
    def __init__(self):
        root = Root()
        torso = root.add(length=60, deg=0, name="torso")
        knee_1 = root.add(length=50, deg=120, name="knee_1", attributes=Attributes(color="rgb(80,80,255)"))
        knee_2 = root.add(length=50, deg=-120, name="knee_2")
        head = torso.add(length=35, deg=0, name="head", attributes=Attributes(circle=True))
        foot_1 = knee_1.add(length=50, deg=180, name="foot_1", attributes=Attributes(color="rgb(80,80,255)"))
        foot_2 = knee_2.add(length=50, deg=180, name="foot_2")
        elbow_1 = torso.add(length=40, deg=120, name="elbow_1", attributes=Attributes(color="rgb(80,80,255)"))
        elbow_2 = torso.add(length=40, deg=-120, name="elbow_2")
        hand_1 = elbow_1.add(length=40, deg=0, name="hand_1", attributes=Attributes(color="rgb(80,80,255)"))
        hand_2 = elbow_2.add(length=40, deg=0, name="hand_2")
        self.root = root
        self._draw = Draw(root)

    def draw(self, image, shadow=False):
        self._draw.draw(image, shadow)

    def export(self):
        dic = {"thigh_1": 180 - 180. / math.pi * self.root.find("knee_1").alpha,
               "shin_1": 180 - 180. / math.pi * self.root.find("foot_1").alpha,
               "thigh_2": 180 - 180. / math.pi * self.root.find("knee_2").alpha,
               "shin_2": 180 - 180. / math.pi * self.root.find("foot_2").alpha,
               "upper_arm1": 180 - 180. / math.pi * self.root.find("elbow_1").alpha,
               "lower_arm1": 180 - 180. / math.pi * self.root.find("hand_1").alpha,
               "upper_arm2": 180 - 180. / math.pi * self.root.find("elbow_2").alpha,
               "lower_arm2": 180 - 180. / math.pi * self.root.find("hand_2").alpha,
               "torso": 180 - 180. / math.pi * self.root.find("torso").alpha,
               "head": 180 - 180. / math.pi * self.root.find("head").alpha,
               "pos": (self.root.position[0] / 100 - 1280 / 200, - self.root.position[1] / 100 + 591 / 100)
               }
        return dic


class Stick:
    def __init__(self, length=60):
        root = Root()
        end = root.add(length=length, deg=0, name="end", attributes=Attributes(color="green"))
        self.root = root
        self._draw = Draw(root)

    def draw(self, image, shadow=False):
        if not shadow:
            self._draw.draw(image)

    def export(self):
        dic = {"end": 180 - 180. / math.pi * self.root.find("end").alpha,
               "pos": (self.root.position[0] / 100 - 1280 / 200, -self.root.position[1] / 100 + 591 / 100)
               }
        return dic


class Flag:
    def __init__(self, inverse=False):
        root = Root()
        self.pole = root.add(length=250, deg=0, name="end", attributes=Attributes(color="green"))
        self.root = root
        self.image = Image.new("RGBA", (100, 50), "white")
        self._draw = Draw(root)
        self.inverse = inverse

    def draw(self, image, shadow=False):
        if shadow:
            return
        deg = -180. / math.pi * self.pole.alpha
        img = self.image.rotate(deg, expand=1)
        sin = math.sin(self.pole.alpha)
        cos = math.cos(self.pole.alpha)
        inverse = self.inverse
        dx = int((1 if inverse else -1) * 50 * cos + 225 * sin)
        dy = int(-225 * cos + (1 if inverse else -1) * 50 * sin)
        image.paste(img, (
            self.root.position[0] - int(img.size[0] / 2) + dx, self.root.position[1] - int(img.size[1] / 2) + dy),
                    img)
        self._draw.draw(image)

    def export(self):
        dic = {"pole": 180 - 180. / math.pi * self.root.find("end").alpha,
               "pos": (self.root.position[0] / 100 - 1280 / 200, -self.root.position[1] / 100 + 591 / 100)
               }
        return dic


class Brick:
    def __init__(self, position, large=False):
        root = Root(position)
        self.brick = root.add(length=10, deg=0, name="brick")
        self.large = large
        self.root = root
        self._draw = Draw(root)
        self.image = Image.open("./images/brick_large.png") if large else Image.open("./images/brick_small.png")

    def draw(self, image, shadow=False):
        if shadow:
            return
        img = self.image.rotate(-180. / math.pi * self.root.find("brick").alpha, expand=1)
        image.paste(img, (self.root.position[0] - int(img.size[0] / 2), self.root.position[1] - int(img.size[1] / 2)),
                    img)
        self._draw.draw(image)

    def export(self):
        self.large = self.image.size[0] > 40
        dic = {"large": self.large,
               "end": 180 - 180. / math.pi * self.brick.alpha,
               "pos": (self.root.position[0] / 100 - 1280 / 200, -self.root.position[1] / 100 + 591 / 100)
               }
        return dic


if __name__ == "__main__":
    sticky = Stickman()
    image = Image.new("RGBA", (1280, 720))
    sticky.draw(image)
    image.show()
