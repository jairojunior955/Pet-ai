from ursina import *
from ursina.shaders import lit_with_shadows_shader, unlit_shader
from game.world import World

app = Ursina()

# Janela
window.title = 'Pet ai'
window.borderless = False
window.fullscreen = False
window.size = (1280, 720)

Entity.default_shader = lit_with_shadows_shader

world = World()

Sky(shader=unlit_shader)

AmbientLight(
    color=color.rgba32(150, 150, 150, 255)
)

sun = DirectionalLight(shadows=True)
sun.look_at(Vec3(1, -1, -1))

EditorCamera()

camera.position = (15, 15, -20)
camera.look_at(Vec3(0, 0, 0))

app.run()