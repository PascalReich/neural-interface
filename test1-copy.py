import cv2
import time
import numpy as np
import concurrent.futures as futures

executor = futures.ThreadPoolExecutor()

rotate = {
    90: cv2.ROTATE_90_CLOCKWISE,
    270: cv2.ROTATE_90_COUNTERCLOCKWISE,
    0: cv2.ROTATE_180
}


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

dotmap = cv2.imread("resources/images/dotmap.png")
dotmap = cv2.cvtColor(dotmap, cv2.COLOR_RGB2RGBA)

# resize images
movemap = cv2.resize(movemap, (480, 640))  # half(backdrop.shape))
backdrop = cv2.resize(backdrop, (480, 640))  # 810,1080
dotmap = cv2.resize(dotmap, (480, 640))
# print(half(movemap.shape))
for pac in range(len(pacs)):
    pacs[pac] = cv2.resize(pacs[pac], half(pacs[pac].shape))

pac = pacs[0]


def addDots(fra):
    start = (25, 75)
    end = (465, 585)

    for pelx in range(start[0], end[0], 20):
        for pely in range(start[1], end[1], 19):
            if np.array_equal(dotmap[pely][pelx], np.asarray([0, 0, 0, 255])):
                fra = cv2.circle(fra, (pelx, pely), 1, (0, 255, 255), 2)

    return True


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
fps_target = 60
speed = 2
direction = 90
x = int(backx / 2 - pacx / 2)
y = 349
# 597
tolerance = 10
ghost_settings = (("Blinky", (0, 0)), ("Clyde", (0, 50)), ("Inky", (50, 0)), ("Pinky", (50, 50)))
del channels

ghosts = [Ghost(i[0], i[1]) for i in ghost_settings]
# print(ghosts)
next_pac_frame = next_pac_frame()

while True:

    # frame setup
    start_time = time.time() - 0.00001
    movemap = movemap.copy()
    frame1 = backdrop.copy()
    pac_local = next(next_pac_frame)
    drawDots = executor.submit(addDots, frame1)

    # read keys
    key = cv2.waitKey(1)
    # print(key)
    if key == ord('q'):
        break
    elif key == ord('w') and not touching_wall(movemap[y - tolerance:pacy + y - tolerance, x:pacx + x]):
        direction = 90
    elif key == ord('s') and not touching_wall(movemap[y + tolerance:pacy + y + tolerance, x:pacx + x]):
        direction = 270
    elif key == ord('a') and not pacx + x - tolerance < 0 and not touching_wall(
            movemap[y:pacy + y, x - tolerance:pacx + x - tolerance]):
        direction = 180
    elif key == ord('d') and not pacx + x + tolerance > backx and not touching_wall(
            movemap[y:pacy + y, x + tolerance:pacx + x + tolerance]):
        direction = 0
    else:
        pass

    # if cv2.getWindowProperty("roman",0) != 0:
    #    break

    # actually move pacman
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

    # make sure he stays on the map
    x = max(x, 0)
    y = max(y, 0)
    x = min(x, backx - pacx)
    y = min(y, backy - pacy)

    if x == 0:
        x = backx - pacx
    elif x == backx - pacx:
        x = 0

    start = (25, 75)
    end = (465, 585)
    """
    for pelx in range(start[0], end[0], 20):
        for pely in range(start[1], end[1], 19):
            if np.array_equal(dotmap[pely][pelx], np.asarray([0, 0, 0, 255])):
                frame1 = cv2.circle(frame1, (pelx, pely), 2, (100, 100, 100))"""

    pac_local = cv2.rotate(pac_local, rotate[direction]) if direction != 180 else pac_local
    # frame[y:pacy + y, x:pacx + x] = pac_local
    pac_show = np.zeros((backy, backx, 4), dtype='uint8')  # np.array([[[0, 0, 0, 255]] * backx] * backy, dtype='uint8')
    pac_show[y:pacy + y, x:pacx + x] = pac_local
    futures.wait([drawDots])
    frame1 = cv2.addWeighted(frame1, 1.0, pac_show, 10.0, 10)
    # cv2.rectangle(frame, (x, y), (x + pacx, y + pacy), (0, 255, 0), 1) # enable this to draw the bounding box

    # fps cap
    """
    start = (25, 75)
    end = (465, 585)

    for pelx in range(start[0], end[0], 20):
        for pely in range(start[1], end[1], 19):
            if np.array_equal(dotmap[pely][pelx], np.asarray([0, 0, 0, 255])):
                frame1 = cv2.circle(frame1, (pelx, pely), 2, (100, 100, 100))"""

    """
    for pelx in range(start[0], 225, 21):
        for pely in range(start[1], end[1], 18):
            if np.array_equal(frame[pely][pelx], np.asarray([0, 0, 0, 255])) and np.array_equal(frame[pely + 5][pelx], np.asarray([0, 0, 0, 255])) and np.array_equal(frame[pely - 5][pelx], np.asarray([0, 0, 0, 255])):
                frame1 = cv2.circle(frame1, (pelx, pely), 2, (100, 100, 100))

    for pelx in range(255, end[0], 22):
        if pelx == 275:
            continue
        for pely in range(start[1], end[1], 18):
            if np.array_equal(frame[pely][pelx], np.asarray([0, 0, 0, 255])) and np.array_equal(frame[pely + 5][pelx], np.asarray([0, 0, 0, 255])) and np.array_equal(frame[pely - 5][pelx], np.asarray([0, 0, 0, 255])):
                frame1 = cv2.circle(frame1, (pelx, pely), 2, (100, 100, 100))"""

    # xs = (25, 60, 110, 160, 215, 265, 315, 365, 415, 450)
    # ys = (80, 150, 205, 260, 310, 360, 420, 470, 525, 580)

    """
    frame1 = cv2.circle(frame1, (100, 0), 2, (100, 100, 100))
    
    for pelx in xs:
        for yval in range(ys[0], ys[len(ys)-1], 12):
            if np.array_equal(frame[yval][pelx], np.asarray([0, 0, 0, 255])) and np.array_equal(frame[yval - 10][pelx], np.asarray([0, 0, 0, 255])) and np.array_equal(frame[yval + 10][pelx], np.asarray([0, 0, 0, 255])):
                frame1 = cv2.circle(frame1, (pelx, yval), 2, (0, 0, 255))
            #print(frame[yval, pelx])

    for pely in ys:
        pass
        #frame1 = cv2.line(frame1, (0, pely), (backx, pely), (0, 0, 255), 2)"""

    # print(np.array_equal(frame1, frame))

    # print(drawDots.result())

    while (1.0 / (time.time() - start_time)) > (fps_target + 0.02):
        time.sleep(0.000001)

    # draw the fps and then show the frame
    frame1 = cv2.putText(frame1, 'FPS: {}'.format(round(1.0 / (time.time() - start_time))), (0, 15),
                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    # cv2.imshow("roman", frame)
    cv2.imshow("roman", frame1)
