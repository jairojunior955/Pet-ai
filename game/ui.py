from ursina import *

class PetUI(Entity):
    def __init__(self, pet):
        super().__init__(parent=camera.ui)

        self.pet = pet

        self.panel = Entity(
            parent = self,
            model =  'quad',
            color = color.rgba32(20, 25, 30, 210),
            scale = (0.35, 0.18),
            position = (-0.67, 0.37)
        )

        self.title = Text(
            parent = self,
            text = "Pet AI - Raposa",
            position = (-0.82, 0.44),
            scale = 1.2
        )

        self.state_text = Text(
            parent=self,
            text="Estado: Parada",
            position=(-0.82, 0.39),
            scale=0.9
        )

        self.position_text = Text(
            parent=self,
            text="",
            position=(-0.82, 0.34),
            scale=0.9
        )

    def update(self):

            self.state_text.text = (
                f"Estado: {self.pet.state.value}"
            )

            self.position_text.text = (
                f"X: {self.pet.x:.1f} "
                f"Z: {self.pet.z:.1f}"
            )

