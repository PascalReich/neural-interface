import cv2
import time
import numpy as np


def half(tup):
    return int(tup[1] / 2), int(tup[0] / 2)


def generate_pix(img):
    x_tol = 3
    y_tol = 3
    for xval in (x_tol, int(img.shape[1]/2), img.shape[1] - x_tol):
        for yval in (y_tol, int(img.shape[0]/2), img.shape[0] - y_tol):
            try:
                yield img[xval, yval]
            except IndexError:
                pass
        # for _ in range(1, img.shape[1] - 8):
        #    yield img[xval, _]
    # for top in range(5)


def touching_wall(img):
    for _ in generate_pix(img):
        if not np.array_equal(_, np.asarray([0, 0, 0, 255])):
            return True
    return False


backdrop = cv2.imread("resources/images/move map.png")
backdrop = cv2.cvtColor(backdrop, cv2.COLOR_RGB2RGBA)
pac = cv2.imread("resources/images/pacman0.png")
pac = cv2.cvtColor(pac, cv2.COLOR_RGB2RGBA)

backdrop = cv2.resize(backdrop, half(backdrop.shape))
pac = cv2.resize(pac, half(pac.shape))

print(backdrop.shape)
fps_target = 144
speed = 1
backy, backx, channels = backdrop.shape
pacy, pacx, channels = pac.shape
direction = 180
x = int(backx / 2 - pacx / 2)
y = 290
tolerance = 5
del channels

while True:

    start_time = time.time()
    frame = backdrop.copy()

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('w') and not touching_wall(frame[y - tolerance:pacy + y - tolerance, x:pacx + x]):
        direction = 90
    elif key == ord('s') and not touching_wall(frame[y + tolerance:pacy + y + tolerance, x:pacx + x]):
        direction = 270
    elif key == ord('a') and not pacx + x - tolerance < 0 and not touching_wall(frame[y:pacy + y, x - tolerance:pacx + x - tolerance]):
        direction = 180
    elif key == ord('d') and not pacx + x + tolerance > backx and not touching_wall(frame[y:pacy + y, x + tolerance:pacx + x + tolerance]):
        direction = 0
    else:
        pass
        # print("dumbass")

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
        # raise Exception("i bet nico messed it up")

    x = max(x, 0)
    y = max(y, 0)
    x = min(x, backx - pacx)
    y = min(y, backy - pacy)
    # print(x, backx, pacx)

    # print(touching_wall(frame[y:pacy + y, x:pacx + x]))
    frame[y:pacy + y, x:pacx + x] = pac
    # cv2.rectangle(frame, (x, y), (x + pacx, y + pacy), (0, 255, 0), 1)

    while (1.0 / (time.time() - start_time)) > (fps_target + 0.02):
        time.sleep(0.000001)

    frame = cv2.putText(frame, f'FPS: {round(1.0 / (time.time() - start_time))}', (0, 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    cv2.imshow("roman i want to die", frame)

