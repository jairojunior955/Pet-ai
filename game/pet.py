from ursina import *
from ursina.models.procedural.cone import Cone
import math

class Fox(Entity):

    def __init__(self, position=(0,0,0)):
        super().__init__(position=position)


        self.orange = color.rgb32(224, 117, 42)
        self.dark_orange = color.rgb32(185, 85, 30)
        self.cream = color.rgb32(255, 239, 215)
        self.dark = color.rgb32(60, 42, 35)
        self.black = color.rgb32(25, 25, 25)

        self.elapsed_time = 0

        self.visual = Entity(parent=self)

        self.create_body()
        self.create_head()
        self.create_ears()
        self.create_eyes()
        self.create_snout()
        self.create_legs()
        self.create_tail()

    def create_body(self):

        self.body = Entity(
            parent=self.visual,
            model='sphere',
            color=self.orange,
            scale=(1.1, 0.85, 1.35),
            position=(0, 0.75, 0)
        )

        self.chest = Entity(
            parent=self.visual,
            model='sphere',
            color=self.cream,
            scale=(0.72, 0.72, 0.45),
            position=(0, 0.75, -0.48)
        )

    def create_head(self):

        self.head = Entity(
            parent=self.visual,
            position=(0, 1.25, -0.55)
        )

        Entity(
            parent=self.head,
            model='sphere',
            color=self.orange,
            scale=(1.3, 1.05, 1.1)
        )

    def create_ears(self):

        for side in [-1, 1]:

            Entity(
                parent=self.head,
                model=Cone(resolution=4),
                color=self.dark_orange,
                scale=(0.38, 0.65, 0.38),
                position=(side * 0.43, 0.62, 0),
                rotation_z=-side * 15
            )

            Entity(
                parent=self.head,
                model=Cone(resolution=4),
                color=self.dark,
                scale=(0.23, 0.43, 0.17),
                position=(side * 0.43, 0.58, -0.13),
                rotation_z=-side * 15
            )

    def create_eyes(self):

        self.eyes = []

        for side in [-1, 1]:

            eye = Entity(
                parent=self.head,
                model='sphere',
                color=self.black,
                scale=(0.15, 0.19, 0.09),
                position=(side * 0.27, 0.06, -0.49)
            )

            self.eyes.append(eye)

    def create_snout(self):

        # Bochechas brancas
        for side in [-1, 1]:

            Entity(
                parent=self.head,
                model='sphere',
                color=self.cream,
                scale=(0.52, 0.36, 0.40),
                position=(side * 0.25, -0.20, -0.40)
            )

        # Focinho
        Entity(
            parent=self.head,
            model='sphere',
            color=self.cream,
            scale=(0.48, 0.32, 0.50),
            position=(0, -0.16, -0.48)
        )

        # Nariz
        Entity(
            parent=self.head,
            model='sphere',
            color=self.black,
            scale=(0.20, 0.13, 0.12),
            position=(0, -0.10, -0.73)
        )

    def create_legs(self):

        self.legs = []

        for x in [-0.34, 0.34]:
            for z in [-0.38, 0.38]:

                leg = Entity(
                    parent=self.visual,
                    model='sphere',
                    color=self.dark_orange,
                    scale=(0.28, 0.58, 0.30),
                    position=(x, 0.34, z)
                )

                Entity(
                    parent=self.visual,
                    model='sphere',
                    color=self.dark,
                    scale=(0.31, 0.23, 0.37),
                    position=(x, 0.115, z - 0.04)
                )

                self.legs.append(leg)

    def create_tail(self):

        # Pivô da cauda
        self.tail = Entity(
            parent=self.visual,
            position=(0, 0.75, 0.58)
        )

        # Parte alaranjada
        Entity(
            parent=self.tail,
            model='sphere',
            color=self.orange,
            scale=(0.52, 0.55, 1.15),
            position=(0, 0.18, 0.45),
            rotation_x=-20
        )

        # Ponta branca
        Entity(
            parent=self.tail,
            model='sphere',
            color=self.cream,
            scale=(0.36, 0.38, 0.52),
            position=(0, 0.34, 0.94),
            rotation_x=-20
        )

    def update(self):

        self.elapsed_time += time.dt

        # Respiração
        breathing = math.sin(
            self.elapsed_time * 2.5
        ) * 0.015

        self.visual.scale_y = 1 + breathing

        # Movimento suave da cauda
        self.tail.rotation_y = math.sin(
            self.elapsed_time * 2
        ) * 15

        # Piscar os olhos a cada quatro segundos
        blinking = self.elapsed_time % 4 < 0.12

        for eye in self.eyes:
            eye.scale_y = 0.015 if blinking else 0.19