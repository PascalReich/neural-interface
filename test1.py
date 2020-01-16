import cv2
import time
import numpy as np

rotate = {
    90: cv2.ROTATE_90_CLOCKWISE,
    270: cv2.ROTATE_90_COUNTERCLOCKWISE,
    0: cv2.ROTATE_180
}

class PowerUp:
    
    brightness = [1, 0]
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def draw(self):
        
        pass
    
    def blink(self, img):
        if self.brightness[1] is 0:
            #darken
        elif self.brightness[1] is 1:
            #brighten/remove dark
        pass
    
    @classmethod
    def update_blink(cls):
        if cls.brightness[0] is 1:
            cls.brightness[1] = 0
        elif cls.brightness[0] is 0:
            cls.brightness[1] = 1
        
        
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        
        pass

class Ghost:
    positions = {  # so that all ghosts dont hit each other
        "Blinky": None,
        "Clyde": None,
        "Inky": None,
        "Pinky": None,
    }

    def __init__(self, name, start):
        self.img = cv2.imread("/resources/images/" + name + ".png")
        self.name = name
        self.coord = start

    def move(self):
        self.positions[self.name] = self.coord  # sync positions
        # do some move action

    def __repr__(self):
        return self.name + " at " + self.coord.__repr__()
    
    def draw(self, frame):
        
        pass


# dont touch
def half(tup):
    return int(tup[1] / 2), int(tup[0] / 2)


# complicated
def generate_pix(img):
    x_tol = 3
    y_tol = 3
    for xval in (x_tol, int(img.shape[1] / 2), img.shape[1] - x_tol):
        for yval in (y_tol, int(img.shape[0] / 2), img.shape[0] - y_tol):
            try:
                yield img[xval, yval]
            except IndexError:
                pass


# what do you think it does?
def touching_wall(img):
    for _ in generate_pix(img):
        if not np.array_equal(_, np.asarray([0, 0, 0, 255])):
            return True
    return False

# read images from disk
movemap = cv2.imread("resources/images/move_map.png")
movemap = cv2.cvtColor(movemap, cv2.COLOR_RGB2RGBA)
backdrop = cv2.imread("resources/images/backdrop.png")
backdrop = cv2.cvtColor(backdrop, cv2.COLOR_RGB2RGBA)
pacs = [cv2.cvtColor(cv2.imread("./resources/images/pacman0.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2RGBA),
        cv2.cvtColor(cv2.imread("./resources/images/pacman1.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2RGBA),
        cv2.cvtColor(cv2.imread("./resources/images/pacman2.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2RGBA),
        cv2.cvtColor(cv2.imread("./resources/images/pacman1.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2RGBA)]
pacdot = cv2.imread("resources/images/pacdot.png")
pacdot = cv2.cvtColor(pacdot, cv2.COLOR_RGB2RGBA)
powerup = cv2.imread("resources/images/powerup.png")
powerup = cv2.cvtColor(powerup, cv2.COLOR_RGB2RGBA)

# resize images
powerup = cv2.resize(powerup, half(powerup.shape))
pacdot = cv2.resize(pacdot, half(pacdot.shape))
movemap = cv2.resize(movemap, (480, 640))# half(backdrop.shape))
backdrop = cv2.resize(backdrop, (480, 640)) #810,1080
#print(half(movemap.shape))
for pac in range(len(pacs)):
    pacs[pac] = cv2.resize(pacs[pac], half(pacs[pac].shape))

pac = pacs[0]


def next_pac_frame():
    while True:
        for step in pacs:
            for i in range(10):
                yield step.copy()


"""
for i in range(len(pac)):
    for j in range(len(pac[i])):
        if np.array_equal(pac[i][j], np.array([0, 0, 0, 0])):
            pac[i][j] = np.array([0, 0, 0, 0])"""

# cv2.imshow("test", np.zeros((30, 30, 4)))
# print(backdrop.shape)
# initialize vars
backy, backx, channels = movemap.shape
pacy, pacx, channels = pac.shape

## GLOBAL SETTINGS ##
fps_target = 144
speed = 1
direction = 90
x = int(backx / 2 - pacx / 2)
y = 349
#597
tolerance = 10
ghost_settings = (("Blinky", (0, 0)), ("Clyde", (0, 50)), ("Inky", (50, 0)), ("Pinky", (50, 50)))
del channels

ghosts = [Ghost(i[0], i[1]) for i in ghost_settings]
#print(ghosts)
next_pac_frame = next_pac_frame()

while True:

    # frame setup
    start_time = time.time() - 0.00001
    frame = movemap.copy()
    frame1 = backdrop.copy()
    pac_local = next(next_pac_frame)
    
    # read keys
    key = cv2.waitKey(1)
    #print(key)
    if key == ord('q'):
        break
    elif key == ord('w') and not touching_wall(frame[y - tolerance:pacy + y - tolerance, x:pacx + x]):
        direction = 90
    elif key == ord('s') and not touching_wall(frame[y + tolerance:pacy + y + tolerance, x:pacx + x]):
        direction = 270
    elif key == ord('a') and not pacx + x - tolerance < 0 and not touching_wall(
            frame[y:pacy + y, x - tolerance:pacx + x - tolerance]):
        direction = 180
    elif key == ord('d') and not pacx + x + tolerance > backx and not touching_wall(
            frame[y:pacy + y, x + tolerance:pacx + x + tolerance]):
        direction = 0
    else:
        pass
    
    #if cv2.getWindowProperty("roman",0) != 0:
    #    break

    # actually move pacman
    if direction == 0 and not touching_wall(frame[y:pacy + y, x + speed:pacx + x + speed]):
        x += speed
    elif direction == 90 and not touching_wall(frame[y - speed:pacy + y - speed, x:pacx + x]):
        y -= speed
    elif direction == 180 and not touching_wall(frame[y:pacy + y, x - speed:pacx + x - speed]):
        x -= speed
    elif direction == 270 and not touching_wall(frame[y + speed:pacy + y + speed, x:pacx + x]):
        y += speed
    else:
        pass

    # make sure he stays on the map
    x = max(x, 0)
    y = max(y, 0)
    x = min(x, backx - pacx)
    y = min(y, backy - pacy)

    if x == 0:
        x = backx - pacx
    elif x == backx - pacx:
        x = 0
    
    
    #loop through intervals of the spaces between dots on one axis on black spaces then in that loop while testing for one x value make another similar loop but with y variable
    
    #make a for loop with len that draws the dots and tracks if a certain dot has been on pacmans loc and if so then stop drawing that dot's number using else variable

    pac_local = cv2.rotate(pac_local, rotate[direction]) if direction != 180 else pac_local
    # frame[y:pacy + y, x:pacx + x] = pac_local
    pac_show = np.zeros((backy, backx, 4), dtype='uint8')  # np.array([[[0, 0, 0, 255]] * backx] * backy, dtype='uint8')
    pac_show[y:pacy + y, x:pacx + x] = pac_local
    frame1 = cv2.addWeighted(frame1, 1.0, pac_show, 10.0, 10)
    #cv2.rectangle(frame, (x, y), (x + pacx, y + pacy), (0, 255, 0), 1) # enable this to draw the bounding box

    # fps cap

    while (1.0 / (time.time() - start_time)) > (fps_target + 0.02):
        time.sleep(0.000001)

    # draw the fps and then show the frame
    frame1 = cv2.putText(frame1, 'FPS: {}'.format(round(1.0 / (time.time() - start_time))), (0, 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    cv2.imshow("roman", frame1)