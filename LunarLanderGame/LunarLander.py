
# https://pygame-zero.readthedocs.io/en/stable/resources.html
# https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun

WIDTH = 1280
HEIGHT = 720

moon = Actor('moon_lat0_long0_resized720p.png')
moon.pos = (WIDTH // 2, HEIGHT // 2)
moon.angle = 0

targetPos = (0, 0)
landerPosition = (0, HEIGHT // 2)
landerVelocity = (10, 0)

thrustLevel = 0
isThrustOn = False
targetSelected = False
fuelRemaining = 100

def initalize():
    music.play('rocketman')

def draw():
    global landerPosition, fuelRemaining, thrustLevel, targetSelected, targetPos

    screen.clear()
    moon.draw()
    screen.draw.circle(landerPosition, 30, 'white')

    if targetSelected:
        screen.draw.circle(targetPos, 15, 'red')

    if fuelRemaining <= 0:
        screen.draw.text("Game Over", (WIDTH // 2 - 100, HEIGHT // 2))
    else:
        screen.draw.text(f"Fuel: {fuelRemaining}%", (10, 10))
        if thrustLevel == 0 or not isThrustOn:
            screen.draw.text("Thrust: OFF", (10, 40))
        elif thrustLevel == 1:
            screen.draw.text("Thrust: MIN", (10, 40))
        elif thrustLevel == 2:
            screen.draw.text("Thrust: MAX", (10, 40))


def update_fuel(thrustLevel):
    global fuelRemaining, landerPosition, targetPos, isThrustOn

    if keyboard.up and thrustLevel > 0 and fuelRemaining > 0:
        sounds.thrust.play()
        isThrustOn = True

    if isThrustOn:
        fuelRemaining -= 1
        xDelta = targetPos[0] - landerPosition[0]
        yDelta = targetPos[1] - landerPosition[1]
        if xDelta < 0:
            landerPosition = (landerPosition[0] - thrustLevel * 10, landerPosition[1])
        elif xDelta > 0:
            landerPosition = (landerPosition[0] + thrustLevel * 10, landerPosition[1])

        if yDelta < 0:
            landerPosition = (landerPosition[0], landerPosition[1] - thrustLevel * 10)
        elif yDelta > 0:
            landerPosition = (landerPosition[0], landerPosition[1] + thrustLevel * 10)
        draw()

    if keyboard.down or thrustLevel == 0 or fuelRemaining <= 0:
        sounds.thrust.stop()
        isThrustOn = False
        draw()

def on_mouse_down(pos, button):
    global landerPosition, targetSelected, targetPos
    if button == mouse.LEFT:
        targetSelected = True
        targetPos = pos
        draw()
        print(f"You click left button at {pos}")


def update():
    global thrustLevel, isThrustOn

    if keyboard.up and thrustLevel > 0 and fuelRemaining > 0:
        isThrustOn = True

    if keyboard.down or thrustLevel == 0 or fuelRemaining <= 0:
        isThrustOn = False

    if keyboard.k_1:
        thrustLevel = 0
    elif keyboard.k_2:
        thrustLevel = 1
    elif keyboard.k_3:
        thrustLevel = 2

    update_fuel(thrustLevel)
    #clock.schedule_unique(update_fuel, 0.250)


pgzrun.go()
