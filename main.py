import cv2
import numpy as np
import functions

feed = cv2.VideoCapture(0)# 1 if using external webcam
bg = cv2.imread("vector.jpg")
win_size = (1440, 810)  # Change for desired size
bg = cv2.resize(bg, win_size)  # Vector image is 1920x1080
functions.prep()

while True:
    _, frame = feed.read()
    frame = cv2.resize(frame, win_size)
    # frame = cv2.rotate(
    #     frame, cv2.ROTATE_180
    # )  # When VideoCapture(1) my camera feed needs rotation
    drawmask, drawmaskside = functions.colorDetect(
        frame
    )  # Colordetect function returns 2 variables
    functions.draw(frame, drawmask, drawmaskside, bg)
    con = cv2.getTrackbarPos(
        "Config", "Controls"
    )  # Checking configuration options for further changes
    functions.colorPick(con)
    if cv2.waitKey(1) & 0xFF == ord("q") or functions.end(
        cv2.getTrackbarPos("Exit", "Controls")
    ):  # Exit statements
        break
