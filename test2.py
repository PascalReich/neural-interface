import cv2
import time
import numpy as np
import keyboard

# this maps the degrees to rotate pacman with the special code that the cv2.rotate function reqiures
rotate = {
    90: cv2.ROTATE_90_CLOCKWISE,
    270: cv2.ROTATE_90_COUNTERCLOCKWISE,
    0: cv2.ROTATE_180
}

#
class Ghost:
    # so that all ghosts dont hit collide - to understand what this really does look up OOP static vars python
    positions = {
        "Blinky": None,
        "Clyde": None,
        "Inky": None,
        "Pinky": None,
    }

    # make ghost instance
    def __init__(self, name, start):
        print("/resources/images/ghosts/" + name + "Left.png")
        self.img = cv2.cvtColor(cv2.imread("resources/images/" + name + "Left.png"), cv2.COLOR_RGB2RGBA)  # read image from disk
        self.name = name
        self.coord = start
        self.size = self.img.shape

    # move the ghost
    def move(self):
        self.positions[self.name] = self.coord  # sync positions
        # do some move action

    # draw ghost
    def draw(self, bg):
        bg[self.coord[1]:self.coord[1] + self.size[1], self.coord[0]:self.coord[0] + self.size[0]] = self.img

    def __repr__(self):  # this makes stuff nice when i print() it
        return self.name + " at " + self.coord.__repr__()


# dont touch, make a tuple(static list) half its size: (100, 100) -> (50, 50)
def half(tup):
    return int(tup[1] / 2), int(tup[0] / 2)


# assuming and image size of maybe 25x25,
# yield all the values at x = 0+xtol (3), 25 - xtol (22) and y = 0+ytol (3), 25-ytol (22)
def generate_pix(img):
    x_tol = 3
    y_tol = 3
    for xval in (x_tol, int(img.shape[1] / 3), int(2 * img.shape[1] / 3), img.shape[1] - x_tol):
        for yval in (y_tol, int(img.shape[0] / 3), int(2 * img.shape[0] / 3), img.shape[0] - y_tol):
            try:
                yield img[xval, yval]
            except IndexError:
                pass


# using the color values yielded from the generator above, check if any are blue (0, 0, 0, 255) (a,r,g,b)
def touching_wall(img):
    for _ in generate_pix(img):
        if not np.array_equal(_, np.asarray([0, 0, 0, 255])):
            return True
    return False


# read images from disk -- normalize them and add transparency
movemap = cv2.imread("resources/images/move_map.png")
movemap = cv2.cvtColor(movemap, cv2.COLOR_RGB2RGBA)
backdrop = cv2.imread("resources/images/backdrop.png")
backdrop = cv2.cvtColor(backdrop, cv2.COLOR_RGB2RGBA)
pacs = [cv2.cvtColor(cv2.imread("resources/images/pacman0.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2RGBA),
        cv2.cvtColor(cv2.imread("resources/images/pacman1.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2RGBA),
        cv2.cvtColor(cv2.imread("resources/images/pacman2.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2RGBA),
        cv2.cvtColor(cv2.imread("resources/images/pacman1.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2RGBA)]

# resize images
movemap = cv2.resize(movemap, half(movemap.shape))
backdrop = cv2.resize(backdrop, half(backdrop.shape))
for pac in range(len(pacs)):
    pacs[pac] = cv2.resize(pacs[pac], half(pacs[pac].shape))

pac = pacs[0]

# generate the next pacman frame (image) when asked
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
backy, backx, channels = backdrop.shape
pacy, pacx, channels = pac.shape

## GLOBAL SETTINGS ##
fps_target = 144
speed = 1
direction = 180
x = int(backx / 2 - pacx / 2)
y = 290
tolerance = 10
ghost_settings = (("Blinky", (0, 0)), ("Clyde", (0, 50)), ("Inky", (50, 0)), ("Pinky", (50, 50)))
del channels

ghosts = [Ghost(i[0], i[1]) for i in ghost_settings]
print(ghosts)
next_pac_frame = next_pac_frame()

while True:

    # frame setup
    start_time = time.time() - 0.0001
    frame = backdrop.copy()  # make copies, not references
    pac_local = next(next_pac_frame)  # get the next pacman frame from the generator defined above

    # read keys
    if keyboard.is_pressed('q'):
        break  # stop the game

        # Explaining touching wall touching_wall(frame[y:pacy + y, x:pacx + x] for keys
        #       When changing direction up and down (w and s) we really only need to be strict about y and its values.
        #       frame[y:pacy + y, x:pacx + x] selects the color values from the top left y (y) to
        #       the bottom left y (pacy + y) and the same with x. I add a little bit opf tolerance, although its more
        #       of a buffer just in case, and i might remove it later

    elif keyboard.is_pressed('w') and not touching_wall(movemap[y - tolerance:pacy + y - tolerance, x:pacx + x]):
        direction = 90
    elif keyboard.is_pressed('s') and not touching_wall(movemap[y + tolerance:pacy + y + tolerance, x:pacx + x]):
        direction = 270
    elif keyboard.is_pressed('a') and not pacx + x - tolerance < 0 and not touching_wall(  # i guess i try to make sure it doesnt go out of bound but i have other checks so i might remove this
            movemap[y:pacy + y, x - tolerance:pacx + x - tolerance]):
        direction = 180
    elif keyboard.is_pressed('d') and not pacx + x + tolerance > backx and not touching_wall(
            movemap[y:pacy + y, x + tolerance:pacx + x + tolerance]):
        direction = 0
    else:
        pass  # other key -- ignore

    # actually move pacman
    # we need to make sure they dont just try and turn in an illegal direction but also never move in one either,
    # so we need to perform similar checks
    if direction == 0 and not touching_wall(movemap[y:pacy + y, x + speed:pacx + x + speed]):
        x += speed
    elif direction == 90 and not touching_wall(movemap[y - speed:pacy + y - speed, x:pacx + x]):
        y -= speed
    elif direction == 180 and not touching_wall(movemap[y:pacy + y, x - speed:pacx + x - speed]):
        x -= speed
    elif direction == 270 and not touching_wall(movemap[y + speed:pacy + y + speed, x:pacx + x]):
        y += speed
    else:
        pass

    # make sure he stays on the map (piecewise functions?)
    x = max(x, 0)
    y = max(y, 0)
    x = min(x, backx - pacx)
    y = min(y, backy - pacy)

    if x == 0:
        x = backx - pacx
    elif x == backx - pacx:
        x = 0

    # rotate pacman in the correct direction using the special code from the rotate dictionary above unless
    # the direction is 180 in which case we dont need to rotate it at all
    pac_local = cv2.rotate(pac_local, rotate[direction]) if direction != 180 else pac_local
    # frame[y:pacy + y, x:pacx + x] = pac_local
    # make an empty, transparent backdrop so we can merge it correctly
    pac_show = np.zeros((backy, backx, 4), dtype='uint8')  # np.array([[[0, 0, 0, 255]] * backx] * backy, dtype='uint8')
    # put the pacman on the backdrop
    pac_show[y:pacy + y, x:pacx + x] = pac_local
    # do calls to ghosts.draw() passing along pac_show as arg
    for ghost in ghosts:
        ghost.draw(pac_show)
    # merge them observing transparency
    frame = cv2.addWeighted(frame, 1.0, pac_show, 10.0, 10)
    # cv2.rectangle(frame, (x, y), (x + pacx, y + pacy), (0, 255, 0), 1) # enable this to draw the bounding box

    # fps cap -- (1.0 / (time.time() - start_time)) calcs fps and so while that is large than the cap, chill.
    while (1.0 / (time.time() - start_time)) > fps_target:
        time.sleep(0.000001)

    # draw the fps and then show the frame
    frame = cv2.putText(frame, 'FPS: {}'.format(round(1.0/(time.time() - start_time))), (0, 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    # show frame
    cv2.imshow("roman i want to die", frame)
    cv2.waitKey(1)  # this step is annoying but it acts as a flush so the frame shows up -- idk j accept it

