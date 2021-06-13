import cv2


def image_rotate_cw(image):
    return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)


def image_rotate_ccw(image):
    return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)


def image_divide(image, width_divide=3, height_divide=2):
    height, width = image.shape[:2]
    dw = int(width / width_divide)
    dh = int(height / height_divide)
    player_view = []

    for hi in range(0, height_divide):
        for wi in range(0, width_divide):
            player_view.append(image[dh * hi : dh * (hi + 1), dw * wi : dw * (wi + 1)])

    for i, pv in enumerate(player_view):
        cv2.imwrite(f"pv_{i}.jpg", pv)


def calibration(image):
    pass
