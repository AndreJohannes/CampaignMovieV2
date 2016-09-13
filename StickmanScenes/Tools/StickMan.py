import math
import pickle

from vapory import vapory


class Stickman:
    def __init__(self, dict_of_angles, crossarm=False, falda=False):
        width = 0.07
        right_pelvis = [width, 0, 0]
        left_pelvis = [-width, 0, 0]
        rad = (dict_of_angles["torso"]) * math.pi / 180.
        neck = [1.5 * width, 0 - 0.6 * math.cos(rad), 0.6 * math.sin(rad)]
        right_shoulder = [1.5 * width, neck[1], neck[2]]
        left_shoulder = [- 1.5 * width, neck[1], neck[2]]
        self.left_shoulder = left_shoulder
        right_knee = self.get_point(right_pelvis, dict_of_angles["thigh_1"], 0, .5)
        right_foot = self.get_point(right_knee, dict_of_angles["shin_1"], 0, .5)
        left_knee = self.get_point(left_pelvis, dict_of_angles["thigh_2"], 0, .5)
        left_foot = self.get_point(left_knee, dict_of_angles["shin_2"], 0, .5)
        left_elbow = self.get_point(left_shoulder, dict_of_angles["upper_arm1"], 0, .4)
        left_elbow = (left_elbow[0] - 0.04, left_elbow[1], left_elbow[2])
        left_hand = self.get_point(left_elbow, dict_of_angles["lower_arm1"], 0, .4)
        right_elbow = self.get_point(right_shoulder, dict_of_angles["upper_arm2"], -0, .4)
        right_elbow = (right_elbow[0] + 0.04, right_elbow[1], right_elbow[2])
        right_hand = self.get_point(right_elbow, dict_of_angles["lower_arm2"], -0, .4)
        if crossarm:
            left_hand = (-left_hand[0], left_hand[1], left_hand[2])
        self.left_hand = left_hand
        self.right_hand = right_hand

        texture = vapory.Texture(vapory.Pigment('color', [0.0 * e for e in [0.20, 0.20, 0.20]]),
                                 vapory.Finish('phong', 0.0))
        deg = (dict_of_angles["torso"])
        self.torso = vapory.Box([-width, 0, -width / 2], [width, 0.6, width / 2], texture,
                                "rotate", [-deg - 180, 0, 0],
                                "translate", [0, 0, 0])
        self.lower_left_leg = self.get_rounded_cylinder(left_knee, left_foot, 0.07 / 2, texture)
        self.upper_left_leg = self.get_rounded_cylinder(left_pelvis, left_knee, 0.07 / 2, texture)
        self.lower_right_leg = self.get_rounded_cylinder(right_knee, right_foot, 0.07 / 2, texture)
        self.upper_right_leg = self.get_rounded_cylinder(right_pelvis, right_knee, 0.07 / 2, texture)
        self.hip = self.get_rounded_cylinder(left_pelvis, right_pelvis, 0.07 / 2, texture)
        self.left_flank = self.get_rounded_cylinder([-width, 0, 0], [-width, neck[1], neck[2]], 0.07 / 2, texture)
        self.right_flank = self.get_rounded_cylinder([width, 0, 0], [width, neck[1], neck[2]], 0.07 / 2, texture)
        self.shoulder = self.get_rounded_cylinder(left_shoulder, right_shoulder, width / 2, texture)
        self.upper_left_arm = self.get_rounded_cylinder(left_shoulder, left_elbow, width / 2, texture)
        self.lower_left_arm = self.get_rounded_cylinder(left_elbow, left_hand, width / 2, texture)
        self.upper_right_arm = self.get_rounded_cylinder(right_shoulder, right_elbow, width / 2, texture)
        self.lower_right_arm = self.get_rounded_cylinder(right_elbow, right_hand, width / 2, texture)
        rad = (dict_of_angles["head"]) * math.pi / 180.
        self.head = vapory.Sphere(
            [0, neck[1] - (0.35 / 2 + width) * math.cos(rad), neck[2] + (0.35 / 2 + width) * math.sin(rad)], 0.35 / 2,
            texture)
        self.body = vapory.Union(self.torso, self.lower_left_leg, self.upper_left_leg, self.lower_right_leg,
                                 self.upper_right_leg, self.hip, self.left_flank, self.right_flank, self.shoulder,
                                 self.upper_left_arm, self.lower_left_arm, self.upper_right_arm, self.lower_right_arm,
                                 self.head)
        if (falda):
            falda = vapory.Triangle(left_pelvis, left_knee, right_knee, texture)
            self.body.args.append(falda)
            p1 = [0, neck[1] - (2.72 - 2.96), neck[2] + 1.57 - 1.74]
            p2 = [0, neck[1] - (3.17 - 2.96), neck[2] + 1.60 - 1.74]
            p3 = [0, neck[1] - (2.72 - 2.96), neck[2] + 1.68 - 1.74]
            hair = vapory.Triangle(p1, p2, p3, texture)
            hair = hair.add_args(["rotate", [0 * 180. / math.pi * rad, 0, 0]])
            self.body.args.append(hair)
            p1 = [0, neck[1] - (3.01 - 2.96), neck[2] + 1.62 - 1.74]
            p2 = [0, neck[1] - (3.26 - 2.96), neck[2] + 1.59 - 1.74]
            p3 = [0, neck[1] - (3.26 - 2.96), neck[2] + 1.54 - 1.74]
            hair = vapory.Triangle(p1, p2, p3, texture)
            hair = hair.add_args(["rotate", [0 * 180. / math.pi * rad, 0, 0]])
            self.body.args.append(hair)
            p1 = [0, neck[1] - (3.26 - 2.96), neck[2] + (1.59 + 1.54) / 2. - 1.74]
            hair = vapory.Sphere(p1, 0.025, texture)
            hair = hair.add_args(["rotate", [0 * 180. / math.pi * rad, 0, 0]])
            self.body.args.append(hair)
        # self.body = self.body.add_args(["scale", [0.5, 0.5, 0.5]])
        pos = dict_of_angles["pos"]
        self.body = self.body.add_args(["translate", [0, pos[1], pos[0]]])

    def get_rounded_cylinder(self, start, end, radius, texture):
        cylinder = vapory.Cylinder(start, end, radius, texture)
        tip_1 = vapory.Sphere(start, radius, texture)
        tip_2 = vapory.Sphere(end, radius, texture)
        return vapory.Union(cylinder, tip_1, tip_2)

    def get_point(self, start, alpha, beta, length):
        (x, y, z) = start
        alpha = math.pi * alpha / 180.
        beta = math.pi * beta / 180.
        x = x + length * math.sin(beta) * math.sin(alpha)
        y = y - length * math.cos(alpha)
        z = z + length * math.cos(beta) * math.sin(alpha)
        return (x, y, z)

    def add_objects(self, list):
        list.append(self.body)


if __name__ == "__main__":
    camera = vapory.Camera('orthographic', 'angle', 50,
                           'location', [10.0, 1.0, 0.0],
                           'look_at', [0.0, 1.0, 0.0])

    sun = vapory.LightSource([1500, 2500, 2500], 'color', 1)

    sky = vapory.Sphere([0, 0, 0], 1, 'hollow',
                        vapory.Texture(vapory.Pigment('gradient', [0, 1, 0],
                                                      vapory.ColorMap([0, 'color', 'White'],
                                                                      [1, 'color', 'White']),
                                                      'quick_color', 'White'),
                                       vapory.Finish('ambient', 1, 'diffuse', 0)),
                        'scale', 10000)

    ground = vapory.Box([-4, 0, -4], [4, -0.1, 4],
                        vapory.Texture(vapory.Pigment('color', [1.1 * e for e in [0.40, 0.45, 0.85]])),
                        vapory.Finish('phong', 0.1))

    frames = pickle.load(open("frames.p", "rb"))
    i = 0
    for frame in frames:
        def getOrientation(pos1, pos2):
            return math.atan2(pos2[0] - pos1[0], -pos2[1] + pos1[1])


        pos = (frame["crotch"][0] - 216) / 100.
        thigh_1 = -180. / math.pi * getOrientation(frame["knee_1"], frame["crotch"])
        thigh_2 = -180. / math.pi * getOrientation(frame["knee_2"], frame["crotch"])
        shin_1 = -180. / math.pi * getOrientation(frame["foot_1"], frame["knee_1"])
        shin_2 = -180. / math.pi * getOrientation(frame["foot_2"], frame["knee_2"])
        upper_arm1 = -180. / math.pi * getOrientation(frame["elbow_1"], frame["neck"])
        upper_arm2 = -180. / math.pi * getOrientation(frame["elbow_2"], frame["neck"])
        lower_arm1 = -180. / math.pi * getOrientation(frame["hand_1"], frame["elbow_1"])
        lower_arm2 = -180. / math.pi * getOrientation(frame["hand_2"], frame["elbow_2"])
        angles = {"pos": pos, "thigh_1": thigh_1, "thigh_2": thigh_2, "shin_1": shin_1, "shin_2": shin_2,
                  "upper_arm1": upper_arm1, "upper_arm2": upper_arm2, "lower_arm1": lower_arm1,
                  "lower_arm2": lower_arm2}
        objects = [sun, sky, ground]
        Stickman(angles).add_objects(objects)
        scene = vapory.Scene(camera, objects,
                             included=['colors.inc', 'textures.inc'])
        scene.render('./images/stickman{}.png'.format(i), width=1200, height=800, antialiasing=.0001)
        i += 1
