from ursina import *
from ursina.models.procedural.cone import Cone
from game.states import PetState

import math
import random

class Fox(Entity):

    def __init__(self, position=(0,0,0)):
        super().__init__(position=position)


        self.orange = color.rgb32(224, 117, 42)
        self.dark_orange = color.rgb32(185, 85, 30)
        self.cream = color.rgb32(255, 239, 215)
        self.dark = color.rgb32(60, 42, 35)
        self.black = color.rgb32(25, 25, 25)

        self.elapsed_time = 0
        self.state = PetState.IDLE
        self.state_timer = 0
        self.state_duration = 3
        self.move_speed = 1.5
        self.rotation_speed = 5
        self.world_limit = 4
        self.target_position = Vec3(*position)

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

                # Pivô da pata
                leg = Entity(
                    parent=self.visual,
                    position=(x, 0.55, z)
                )

                # Parte superior
                Entity(
                    parent=leg,
                    model='sphere',
                    color=self.dark_orange,
                    scale=(0.28, 0.58, 0.30),
                    position=(0, -0.21, 0)
                )

                # Pé
                Entity(
                    parent=leg,
                    model='sphere',
                    color=self.dark,
                    scale=(0.31, 0.23, 0.37),
                    position=(0, -0.435, -0.04)
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

    def change_state(self, new_state):

        self.state = new_state
        self.state_timer = 0

        if new_state == PetState.IDLE:

            self.state_duration = random.uniform(2, 5)

        elif new_state == PetState.WALKING:

            self.choose_target()

        elif new_state == PetState.RESTING:

            self.state_duration = random.uniform(5, 10)

        #print(f"Estado atual: {self.state.value}")

    def choose_target(self):

        x = random.uniform(
            -self.world_limit,
            self.world_limit
        )

        z = random.uniform(
            -self.world_limit,
            self.world_limit
        )

        self.target_position = Vec3(x, 0, z)

        print(f"Novo destino: {self.target_position}")

    def choose_next_action(self):

        next_state = random.choices(
            [
                PetState.WALKING,
                PetState.RESTING
            ],
            weights=[75, 25],
            k=1
        )[0]

        self.change_state(next_state)

    
    def walk(self):

        direction = self.target_position - self.position
        direction.y = 0

        remaining_distance = direction.length()

        # Verificar se chegou ao destino
        if remaining_distance < 0.15:

            self.change_state(PetState.IDLE)
            return

        direction = direction.normalized()

        # Movimento com velocidade constante
        movement = min(
            self.move_speed * time.dt,
            remaining_distance
        )

        self.position += direction * movement

        # Calcular rotação desejada
        target_rotation = math.degrees(
            math.atan2(-direction.x, -direction.z)
        )

        # Encontrar o menor ângulo de rotação
        angle_difference = (
            target_rotation
            - self.rotation_y
            + 180
        ) % 360 - 180

        # Rotação suave
        self.rotation_y += angle_difference * min(
            time.dt * self.rotation_speed,
            1
        )

    
    def animate_pet(self):

        # Respiração
        breathing = math.sin(
            self.elapsed_time * 2.5
        ) * 0.015

        self.visual.scale_y = 1 + breathing

        # Movimento da cauda
        self.tail.rotation_y = math.sin(
            self.elapsed_time * 2
        ) * 15

        # Animação dos olhos
        blinking = self.elapsed_time % 4 < 0.12

        for eye in self.eyes:

            if self.state == PetState.RESTING:
                eye.scale_y = 0.015
            else:
                eye.scale_y = 0.015 if blinking else 0.19

        if self.state == PetState.WALKING:

            # Balanço do corpo
            self.visual.y = abs(
                math.sin(self.elapsed_time * 8)
            ) * 0.06

            # Animação das patas
            phases = [0, math.pi, math.pi, 0]

            for i, leg in enumerate(self.legs):

                leg.rotation_x = math.sin(
                    self.elapsed_time * 8 + phases[i]
                ) * 25

        else:

            # Retornar à posição original
            self.visual.y = lerp(
                self.visual.y,
                0,
                min(time.dt * 5, 1)
            )

            for leg in self.legs:

                leg.rotation_x = lerp(
                    leg.rotation_x,
                    0,
                    min(time.dt * 5, 1)
                )

    def update(self):

        self.elapsed_time += time.dt
        self.state_timer += time.dt

        if self.state == PetState.IDLE:

            if self.state_timer >= self.state_duration:

                self.choose_next_action()

        elif self.state == PetState.WALKING:

            self.walk()

        elif self.state == PetState.RESTING:

            if self.state_timer >= self.state_duration:

                self.change_state(PetState.IDLE)

        self.animate_pet()
