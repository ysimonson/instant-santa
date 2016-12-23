import cv2
import sys

hat = cv2.imread("assets/opencv/hat.png", -1)
beard = cv2.imread("assets/opencv/beard.png", -1)
cascade = cv2.CascadeClassifier("assets/opencv/haarcascade_frontalface_alt.xml")

def detect(img):
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.CASCADE_SCALE_IMAGE, (20, 20))

    if len(rects) == 0:
        return []

    rects[:, 2:] += rects[:, :2]
    return rects

def get_image_scale(img, x1, y1, x2, y2):
    img_height, img_width, _ = img.shape
    scaled_img_width = x2 - x1
    scaled_img_height = int((float(scaled_img_width) / img_width) * img_height)
    return img_width, img_height, scaled_img_width, scaled_img_height

def insert_image(base_img, img, x, y, width, height):
    scaled_img = cv2.resize(img, (width, height))

    for c in range(0, 3):
        base_img[y : y + height, x : x + width, c] = \
            scaled_img[:, :, c] * (scaled_img[:, :, 3] / 255.0) + base_img[y : y + height, x : x + width, c] * (1.0 - scaled_img[:, :, 3] / 255.0)

def santas(rects, img):
    if len(rects) == 0:
        raise Exception("No faces")

    for x1, y1, x2, y2 in rects:
        hat_width, hat_height, scaled_hat_width, scaled_hat_height = get_image_scale(hat, x1, y1, x2, y2)
        insert_image(img, hat, x1, max(0, y1 - scaled_hat_height / 2), scaled_hat_width, scaled_hat_height)

        beard_width, beard_height, scaled_beard_width, scaled_beard_height = get_image_scale(beard, x1, y1, x2, y2)
        insert_image(img, beard, x1, y1 + scaled_beard_height / 2, scaled_beard_width, scaled_beard_height)

    return img
