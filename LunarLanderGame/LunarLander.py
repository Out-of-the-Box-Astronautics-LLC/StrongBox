
# https://pygame-zero.readthedocs.io/en/stable/resources.html
# https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun

WIDTH = 1280
HEIGHT = 720

moon = Actor('moon_lat0_long0_resized720p.png')
moon.pos = (WIDTH // 2, HEIGHT // 2)
moon.angle = 0

def draw():
    screen.clear()
    moon.draw()
    #screen.fill((128, 0, 0))
    #screen.draw.circle((400, 300), 30, 'white')

def update():
    pass

def on_mouse_down(pos, button):
    if button == mouse.LEFT:
        print(f"You click left button at {pos}")


pgzrun.go()
