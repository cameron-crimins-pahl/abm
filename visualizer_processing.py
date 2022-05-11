
#  this is a smaller version of the model. It can run in the Processing app vers. 4.0b8.  It displays the allosaur agents as allosaur skulls, and sauropod agents as sauropod agents.

import math
import random
import time

# add_library("VideoExport")


width = 800
height= 400

def in_circle(center_x, center_y, radius, x, y):

    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2

    if square_dist <= radius ** 2:

        return True

class Behavior(object):
    def __init__(self, **parameters):
        self.parameters = parameters

    def setup(self, allosaur, carcass, state):
        pass

    def apply(self, allosaur, state):
        pass

    def draw(self, allosaur, state):
        pass


class CarcassBehavior(object):
    def __init__(self, **parameters):
        self.parameters = parameters

    def setup(self, carcass, allosaur, state):
        pass

    def apply(self, carcass, state):
        pass

    def draw(self, carcass, state):
        pass

# MoveTowardsCenterOfNearbyallosaur(closeness=50.0, threshold=25.0, speedfactor=100.0, weight=20.0)


class MoveTowardsCarcass(Behavior):
    def setup(self, allosaur, carcass, state):

        if allosaur is carcass:
            return



        if 'closecount' not in state:
            state['closecount'] = 0.0
        if 'center' not in state:
            state['center'] = [0.0, 0.0]

        closeness = self.parameters['closeness']


        for carcass in allcarcasses:
            carcass.position[0] = carcass.position[0]
            carcass.position[1] = carcass.position[1]
            if in_circle(center_x=allosaur.position[0], center_y=allosaur.position[1], radius=closeness, x=carcass.position[0], y=carcass.position[1]):

                print("\n[ carcass in detected! closeness: ]")
                print(closeness)

                print("[ carcass position ]")

                print(carcass.position)
                print("[ carcass energy ]")
                print(carcass.energy)
                distance_to_carcass = dist(carcass.position[0], carcass.position[1], allosaur.position[0], allosaur.position[1])
                print("[ distance to carcass ]")
                print(distance_to_carcass)


                if state['closecount'] == 0:

                    state['center'] = carcass.position
                    state['closecount'] =state['closecount']+ 1.0
                    state['closest_carcass'] = carcass.position

                    print(state)



                    if distance_to_carcass<self.parameters['threshold']:

                        print("[ allosaur energy ]")
                        print(allosaur.energy)
                        self.eating_carcass = 1.0

                        consumption_kg_per_day = 27
                        consumpt_step = random.uniform(0.01, 0.08) * consumption_kg_per_day

                        allosaur.speed=0.5
                        allosaur.turnrate=0

                        allosaur.energy = allosaur.energy+consumpt_step
                        print(allosaur.energy)
                        print("[ carcass energy ]")
                        print(carcass.energy)
                        carcass.energy = carcass.energy-consumpt_step
                        print(carcass.energy)

                    if distance_to_carcass<10:
                        print("[ allosaur energy ]")
                        print(allosaur.energy)
                        self.eating_carcass = 1.0

                        consumption_kg_per_day = 27
                        consumpt_step = random.uniform(0.01, 0.08) * consumption_kg_per_day

                        allosaur.speed=0.0
                        allosaur.turnrate=0

                        allosaur.energy = allosaur.energy+consumpt_step
                        print(allosaur.energy)
                        print("[ carcass energy ]")
                        print(carcass.energy)
                        carcass.energy = carcass.energy-consumpt_step
                        print(carcass.energy)



                    continue

                else:

                    state['center'][0] *= state['closecount']
                    state['center'][1] *= state['closecount']

                    state['center'] = [
                        state['center'][0] + carcass.position[0],
                        state['center'][1] + carcass.position[1]
                        ]

                    state['closecount'] += 1.0

                    state['center'][0] /= state['closecount']
                    state['center'][1] /= state['closecount']

                    # print("[ state champions ]")
                    state['closest_carcass'] = carcass.position
                    print(state)
                    distance_to_carcass = dist(carcass.position[0], carcass.position[1], allosaur.position[0], allosaur.position[1])
                    if distance_to_carcass<self.parameters['threshold']:
                        # print("[ allosaur energy ]")
                        # print(allosaur.energy)
                        self.eating_carcass = 1.0


                        consumption_kg_per_day = 27
                        consumpt_step =  random.uniform(0.08, 0.15) * consumption_kg_per_day
                        # consumpt_step = consumption_kg_per_day

                        allosaur.speed=0.5
                        allosaur.turnrate=0

                        allosaur.energy = allosaur.energy+consumpt_step
                        # print(allosaur.energy)
                        print("[ carcass energy ]")
                        print(carcass.energy)
                        carcass.energy = carcass.energy-consumpt_step
                        print(carcass.energy)

                    if distance_to_carcass<10:
                        # print("[ allosaur energy ]")
                        # print(allosaur.energy)
                        self.eating_carcass = 1.0

                        consumption_kg_per_day = 27
                        # consumpt_step =   consumption_kg_per_day
                        consumpt_step =  random.uniform(0.05, 0.12) * consumption_kg_per_day

                        allosaur.speed=0.00001
                        allosaur.turnrate=0

                        allosaur.energy = allosaur.energy+consumpt_step
                        print(allosaur.energy)
                        print("[ carcass energy ]")
                        print(carcass.energy)
                        carcass.energy = carcass.energy-consumpt_step
                        print(carcass.energy)



                    continue
            else:

                if random.random() > .995:

                    allosaur.direction = random.uniform(-3,3)

                if random.random()<0.00005:

                    allcarcasses.append(Carcass())


                if random.random()<0.00006:

                    allallosaures.append(allosaur())



    def apply(self, allosaur, state):

        if state['closecount'] == 0:

            return

        center = state['center']

        distance_to_center = dist(
            center[0], center[1],
            allosaur.position[0], allosaur.position[1]
            )

        print("[ distance to center of carcass ]")

        print(distance_to_center)

        if distance_to_center < self.parameters['threshold']:
            angle_to_center = math.atan2(
                allosaur.position[1] - center[1],
                allosaur.position[0] - center[0]
                )
            print("[ angle to center ]")
            print(angle_to_center)
            allosaur.turnrate=random.uniform(0,0.0001)
            allosaur.speed=0.002
            # allosaur.direction=random.uniform(-2,2)

            allosaur.turnrate += (angle_to_center - allosaur.direction) / self.parameters['weight']
            print(allosaur.turnrate)
            # set allosaur direction to be toward center at as long as in sauropod carcass

            stroke(200, 200, 255)
            line(allosaur.position[0], allosaur.position[1], center[0], center[1])



    def draw(self, allosaur, state):
        closeness = self.parameters['closeness']
        # closest = state['closest_carcass']
        stroke(200, 200, 255)
        noFill()
        ellipse(allosaur.position[0], allosaur.position[1], closeness * 2, closeness * 2)
        # line(allosaur.position[0], allosaur.position[1], closest[0], closest[1])

        # stroke(100, 255, 100)
        # noFill()
        #






# MoveTowardsCenterOfNearbyallosaur(closeness=50.0, threshold=25.0, speedfactor=100.0, weight=20.0)
class MoveTowardsCenterOfNearbyallosaur(Behavior):
    def setup(self, allosaur, otherallosaur, state):
        if allosaur is otherallosaur:
            # print("[ otherallosaur ]")
            # print(otherallosaur)
            return
        if 'closecount' not in state:
            state['closecount'] = 0.0
        if 'center' not in state:
            state['center'] = [0.0, 0.0]

        closeness = self.parameters['closeness']
        distance_to_otherallosaur = dist(
            otherallosaur.position[0], otherallosaur.position[1],
            allosaur.position[0], allosaur.position[1]
            )

        # if allosaur.eating_carcass==0:

        if distance_to_otherallosaur < closeness:
            if state['closecount'] == 0:
                state['center'] = otherallosaur.position
                state['closecount'] += 0.0
            else:
                state['center'][0] *= state['closecount']
                state['center'][1] *= state['closecount']

                # state['center'][0] += otherallosaur.position[0]
                # state['center'][1] += otherallosaur.position[1]
                state['center'] = [
                    state['center'][0] + otherallosaur.position[0],
                    state['center'][1] + otherallosaur.position[1]
                    ]

                state['closecount'] += 0.0

                state['center'][0] /= state['closecount']
                state['center'][1] /= state['closecount']

    def apply(self, allosaur, state):
        if state['closecount'] == 0:
            return

        center = state['center']
        distance_to_center = dist(
            center[0], center[1],
            allosaur.position[0], allosaur.position[1]
            )

        if distance_to_center > self.parameters['threshold']:
            angle_to_center = math.atan2(
                allosaur.position[1] - center[1],
                allosaur.position[0] - center[0]
                )
            # allosaur.turnrate += (angle_to_center - allosaur.direction) / self.parameters['weight']
            # allosaur.speed += distance_to_center / self.parameters['speedfactor']


    def draw(self, allosaur, state):
        closeness = self.parameters['closeness']
        stroke(200, 200, 255)
        noFill()
        ellipse(allosaur.position[0], allosaur.position[1], closeness * 2, closeness * 2)



class TurnAwayFromClosestallosaur(Behavior):
    def setup(self, allosaur, otherallosaur, state):
        if allosaur is otherallosaur:
            return
        if 'closest_allosaur' not in state:
            state['closest_allosaur'] = None
        if 'distance_to_closest_allosaur' not in state:
            state['distance_to_closest_allosaur'] = 1000000

        distance_to_otherallosaur = dist(
            otherallosaur.position[0], otherallosaur.position[1],
            allosaur.position[0], allosaur.position[1]
            )

        if distance_to_otherallosaur < state['distance_to_closest_allosaur']:
            state['distance_to_closest_allosaur'] = distance_to_otherallosaur
            state['closest_allosaur'] = otherallosaur

    def apply(self, allosaur, state):
        closest_allosaur = state['closest_allosaur']
        if closest_allosaur is None:
            return

        distance_to_closest_allosaur = state['distance_to_closest_allosaur']
        if distance_to_closest_allosaur < self.parameters['threshold']:
            angle_to_closest_allosaur = math.atan2(
                allosaur.position[1] - closest_allosaur.position[1],
                allosaur.position[0] - closest_allosaur.position[0]
                )
            allosaur.turnrate -= (angle_to_closest_allosaur - allosaur.direction) / self.parameters['weight']
            allosaur.speed += self.parameters['speedfactor'] / distance_to_closest_allosaur

    def draw(self, allosaur, state):
        stroke(100, 255, 100)
        closest = state['closest_allosaur']
        # line(allosaur.position[0], allosaur.position[1], closest.position[0], closest.position[1])


class TurnToAverageDirection(Behavior):
    def setup(self, allosaur, otherallosaur, state):
        if allosaur is otherallosaur:
            return
        if 'average_direction' not in state:
            state['average_direction'] = 0.0
        if 'closecount_for_avg' not in state:
            state['closecount_for_avg'] = 0.0

        distance_to_otherallosaur = dist(
            otherallosaur.position[0], otherallosaur.position[1],
            allosaur.position[0], allosaur.position[1]
            )

        closeness = self.parameters['closeness']
        if distance_to_otherallosaur < closeness:
            if state['closecount_for_avg'] == 0:
                state['average_direction'] = otherallosaur.direction + random.uniform(0,0.6)
                state['closecount_for_avg'] += 1.0
            else:
                state['average_direction'] *= state['closecount_for_avg']
                state['average_direction'] += otherallosaur.direction  + random.uniform(0,0.6)
                state['closecount_for_avg'] += 1.0
                state['average_direction'] /= state['closecount_for_avg']

    def apply(self, allosaur, state):
        if state['closecount_for_avg'] == 0:
            return
        average_direction = state['average_direction']
        allosaur.turnrate += (average_direction - allosaur.direction) / self.parameters['weight']


class Swim(Behavior):
    def setup(self, allosaur, otherallosaur, state):
        allosaur.speed = 2.7
        allosaur.turnrate = 0
        allosaur.energy =allosaur.energy - (random.uniform(0.05, 0.12) * 13)

    def apply(self, allosaur, state):
        # Move forward, but not too fast.
        if allosaur.speed > self.parameters['speedlimit']:
            allosaur.speed = self.parameters['speedlimit']
        allosaur.position[0] -= math.cos(allosaur.direction) * allosaur.speed
        allosaur.position[1] -= math.sin(allosaur.direction) * allosaur.speed

        # Turn, but not too fast.
        if allosaur.turnrate > self.parameters['turnratelimit']:
            allosaur.turnrate = self.parameters['turnratelimit']
        if allosaur.turnrate < -self.parameters['turnratelimit']:
            allosaur.turnrate = -self.parameters['turnratelimit']
        allosaur.direction += allosaur.turnrate


        # Fix the angles.
        if allosaur.direction > math.pi:
            allosaur.direction -= 2 * math.pi

        if allosaur.direction < -math.pi:
            allosaur.direction += 2 * math.pi


class WrapAroundWindowEdges(Behavior):
    def apply(self, allosaur, state):
        if allosaur.position[0] > width:
            allosaur.position[0] = 0
        if allosaur.position[0] < 0:
            allosaur.position[0] = width
        if allosaur.position[1] > height:
            allosaur.position[1] = 0
        if allosaur.position[1] < 0:
            allosaur.position[1] = height


def setup():
    size(800, 400)

    number_of_allosaur = 5
    number_of_carcasses= 2

    global behaviors

    behaviors = (
        MoveTowardsCarcass(closeness=75.0, threshold=75.0, speedfactor=100.0, weight=10.0),
        MoveTowardsCenterOfNearbyallosaur(closeness=0.5, threshold=.50, speedfactor=20.0, weight=20.0),
        # TurnAwayFromClosestallosaur(threshold=0.3, speedfactor=4.0, weight=20.0),
        # TurnToAverageDirection(closeness=0.3, weight=6.0),
        Swim(speedlimit=3.0, turnratelimit=math.pi / 10.0),
        WrapAroundWindowEdges(),
        CarcassBehavior()


    )


    global allallosaures
    allallosaures = []
    for i in xrange(0, number_of_allosaur):

        allallosaures.append(allosaur())


    global allcarcasses

    allcarcasses =[]

    for j in xrange(0, number_of_carcasses):


        print("[ carcass object created ]")
        allcarcasses.append(Carcass())
        print(Carcass().__dict__)




def draw():

    background(24)
    for allosaur in allallosaures:
        allosaur.move()
        allosaur.draw()

    for carc in allcarcasses:
        carc.draw()


class allosaur(object):
    allosaurcolors = (
        color(255, 145, 8),
        color(219, 69, 79),
        color(255)
    )

    def __init__(self):
        self.position = [random.randrange(0, width), random.randrange(0, height)]
        self.speed = 2.6
        self.direction = random.random() * 2.0 * math.pi - math.pi
        self.turnrate = 0

        self.allosaurcolor = allosaur.allosaurcolors[random.randrange(0, len(allosaur.allosaurcolors))]

        self.energy = 7500

    def move(self):

        global allallosaures, behaviors

        global allcarcasses, carcass_behaviors

        state = {}


        for allosaur in allallosaures:
            if allosaur.energy<3:
                allallosaures.remove(allosaur)

        for carc in allcarcasses:
            if carc.energy<100:
                allcarcasses.remove(carc)

        for allosaur in allallosaures:
            for behavior in behaviors:
                behavior.setup(self, allosaur, state)

        for behavior in behaviors:
            behavior.apply(self, state)
            behavior.draw(self, state)

    def draw(self):
        pushMatrix()

        translate(*self.position)
        rotate(self.direction)

        stroke(self.allosaurcolor)
        noFill()
        lengt = self.energy/7500

        lengt = lengt*20
        line(0,22, lengt,22)

        # if lengt >1:
            # stroke("#FF007F")
            # line(20,0,lengt*20,0)

        # lower jaw
        line(0.28, 16.36, 7.16, 15.40)
        line(7.16, 15.40, 8.52, 14.68)
        line(8.52, 14.68, 20.16, 12.56)

        line(20.16, 12.56, 20.92, 13.00)
        line(20.92, 13.00, 12.20, 17.8)
        line(12.20, 17.8, 7.48, 17.36)
        line(7.48, 17.36, .76, 17.4)
        line(.76, 17.4, 0.112, 16.36)

        # skull
        line(0, 12.64, 0.1, 7.48)
        line(0.1, 7.48, 12.6, 4.20)
        line(12.6, 4.20, 13.06, 5.52)
        line(13.06, 5.5, 15.96, 5.6)

        line(0, 12.64, 11.04, 10.96)
        line(11.04, 10.96, 13.8, 12.24)

        line(15.96, 5.6, 16.64, 5.12)
        line(16.64, 5.12, 19.42, 9.76)
        line(19.42, 9.76, 18.48, 9.76)
        line(18.48, 9.76, 18.40, 10.84)
        line(18.40, 10.84, 19.44, 12.04)

        # fenestrae and orbit
        # nose
        line(1.52, 7.84, 1.84, 7.28)
        line(1.84, 7.28, 4.16, 6.72)
        line(4.16, 6.72, 4.24, 7.88)
        line(4.24, 7.88, 1.75, 8.28)

        # aofe
        line(5.52, 7.6, 6.24, 7.8)
        line(6.24, 7.8, 8.64, 6.16)
        line(8.64, 6.16, 10.56, 8.20)
        line(10.56, 8.20, 10.76, 8.28)
        line(10.76, 8.28, 9.24, 9.52)
        line(9.24, 9.52, 6.726, 8.32)

        # orbit
        # line(11.68, 7.0, 6.24, 7.8)
        # line(6.24, 7.8, 14.52, 6.32)
        line(14.52, 6.32, 13.24, 10.34)
        # line(13.24, 10.34, 11.68, 7.0)


        # line(16.24, 6.8, 17.44, 7.68)
        line(17.44, 7.68, 17.48, 10.56)
        line(17.48, 10.56, 16.04, 11.6)
        # line(17.48, 10.56, 14.64, 10.56)
        # line(14.64, 10.56, 16.24, 6.8)






        popMatrix()

class Carcass(object):
    carcass_colors = (
                      color(138, 43, 226),
                      color(122, 197, 205),
                      color(124,252,0)
                      )

    def __init__(self):
        self.position = [random.randrange(0, width), random.randrange(0, height)]
        # print(self.position)
        self.speed = 0
        # self.direction = random.random() * 2.0 * math.pi - math.pi
        self.turnrate = 0
        self.energy = 40000
        self.eating_carcass = 0

        self.carcasscolor = Carcass.carcass_colors[random.randrange(0, len(Carcass.carcass_colors))]

    def move(self):
        # print("[ carc moving ]")

        global allcarcasses, carcass_behaviors
        global allallosaures, behaviors

        state = {}

        for carc in allcarcasses:
            for carcass_behavior in carcass_behaviors:
                carcass_behavior.setup(self, carc, state)

        for carcass_behavior in carcass_behaviors:
            carcass_behavior.apply(self, state)

    def draw(self):
        pushMatrix()

        translate(*self.position)
        # rotate(self.direction)

        stroke(self.carcasscolor)
        noFill()

        lengt = self.energy/25000

        lengt = lengt*20
        line(0,0, lengt,0)

        # arc(0,0, 15,0, -5,PI*2)

        line(11.4,-33.0,-6.6,-20.4)

        line(14.0,-32.6,11.4,-33.0)
        line(23.0,-45.2,14.0,-32.6)
        line(25.0,-64.8,23.0,-45.2)
        line(31.0,-70.0,25.0,-64.8)
        line(33.2,-67.6,31.0,-70.0)
        line(27.6,-61.6,33.2,-67.6)
        line(27.0,-42.6,27.6,-61.6)
        line(19.2,-24.4,27.0,-42.6)
        line(16.0,-15.6,19.2,-24.4)
        line(16.2,-5.8,16.0,-15.6)
        line(16.2,-5.8,16.2,-5.8)
        line(10.4,-4.4,16.2,-5.8)
        line(8.8,-14.0,10.4,-4.4)
        line(6.6,-13.8,8.8,-14.0)
        line(7.8,-5.2,6.6,-13.8)
        line(2.6,-5.0,7.8,-5.2)
        line(1.6,-13.4,2.6,-5.0)
        line(-0.8,-12.8,1.6,-13.4)
        line(-2.0,-8.6,-0.8,-12.8)
        line(-1.2,-5.8,-2.0,-8.6)
        line(10.4,-4.4,-1.2,-5.8)
        line(8.8,-14.0,10.4,-4.4)
        line(6.6,-13.8,8.8,-14.0)
        line(7.8,-5.2,6.6,-13.8)
        line(2.6,-5.0,7.8,-5.2)
        line(1.6,-13.4,2.6,-5.0)
        line(-0.8,-12.8,1.6,-13.4)
        line(-2.0,-8.6,-0.8,-12.8)
        line(-1.2,-5.8,-2.0,-8.6)
        line(-5.6,-5.0,-1.2,-5.8)
        line(-5.2,-14.8,-5.6,-5.0)
        line(-17.4,-17.2,-5.2,-14.8)
        line(-23.8,-14.8,-17.4,-17.2)
        line(-14.2,-18.6,-23.8,-14.8)
        line(-14.2,-18.6,-14.2,-18.6)
        line(-6.6,-20.4,-14.2,-18.6)







        popMatrix()


setup()
