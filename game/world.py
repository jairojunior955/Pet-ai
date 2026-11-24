from ursina import *
from ursina.models.procedural.cone import Cone
import random

class World:
    def __init__(self):
        self.create_ground()
        self.create_forest()
        self.create_rocks()

    def create_ground(self):
        self.ground = Entity(
            model='plane',
            color=color.rgb32(139, 195, 74),
            scale=(40, 1, 40),
            collider='box'
        )

    def create_tree(self, x, z):

        # Objeto principal da árvore
        tree = Entity(
            position=(x, 0, z)
        )

        # Tronco
        Entity(
            parent=tree,
            model='cube',
            color=color.rgb32(101, 67, 33),
            scale=(0.4, 2, 0.4),
            position=(0, 1, 0)
        )

        # Camadas de folhas
        for i in range(3):

            size = 2.5 - (i * 0.5)

            Entity(
                parent=tree,
                model=Cone(resolution=6),
                color=color.rgb32(46, 125, 50),
                scale=(size, 1.8, size),
                position=(0, 1.8 + i * 0.9, 0)
            )

        return tree

    def create_forest(self):

        for i in range(30):

            x = random.uniform(-18, 18)
            z = random.uniform(-18, 18)

            # Deixar o centro livre para o pet
            if abs(x) < 5 and abs(z) < 5:
                continue

            tree = self.create_tree(x, z)

            tree.scale = random.uniform(0.8, 1.5)

    def create_rocks(self):

        for i in range(20):

            x = random.uniform(-18, 18)
            z = random.uniform(-18, 18)

            if abs(x) < 5 and abs(z) < 5:
                continue

            size = random.uniform(0.3, 1.0)

            Entity(
                model='icosphere',
                color=color.rgb32(125, 130, 135),
                scale=(size, size * 0.7, size),
                position=(x, size * 0.2, z),
                rotation=(
                    0,
                    random.uniform(0, 360),
                    0
                )
            )