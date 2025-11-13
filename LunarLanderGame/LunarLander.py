
# https://pygame-zero.readthedocs.io/en/stable/resources.html
# https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun

WIDTH = 1280
HEIGHT = 720

moon = Actor('moon_lat0_long0_resized720p.png')
moon.pos = (WIDTH // 2, HEIGHT // 2)
moon.angle = 0

landerPosition = (0, HEIGHT // 2)
landerVelocity = (10, 0)

thurstLevel = 0
fuelRemaining = 100

def initalize():
    music.play('rocketman')

def draw():
    moon.draw()

def update_fuel():
    if keyboard.up:
        sounds.thrust.play()
        fuelRemaining -= 1 
        screen.draw.text(f"Fuel: {fuelRemaining}%", (10, 10))

def lander_draw():
    screen.clear()
    #screen.fill((0, 0, 0))
    screen.draw.circle(landerPosition, 30, 'white')

def on_mouse_down(pos, button):
    if button == mouse.LEFT:
        print(f"You click left button at {pos}")
        
        
def update():
    
    if keyboard.k_1:
        thurstLevel = 0
    elif keyboard.k_2:
        thurstLevel = 1
    elif keyboard.k_3:
        thurstLevel = 2  

    clock.schedule_unique(update_fuel, 0.250) 


pgzrun.go()
