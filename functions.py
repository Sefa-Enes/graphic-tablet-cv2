import cv2
import numpy as np

# Declaring global variables
exit_flag = False
cmm = None
css = None
lowermain = None
uppermain = None
lowerside = None
upperside = None
annotation = []
colorg = (0, 0, 0)
controls_img = np.zeros((100, 200, 3), np.uint8)
controls_img.fill(240)
sizeg = 10
previous = None


def prep():  # Setting up the necessary parameters
    global cmm, css, lowermain, uppermain, lowerside, upperside, controls_img
    # cv2.namedWindow("Controls")
    # cv2.resizeWindow("Controls", 200, 300)

    cv2.rectangle(controls_img, (9, 9), (191, 91), (0, 0, 0), 1)
    cv2.rectangle(controls_img, (10, 10), (190, 90), colorg, -1)
    cv2.imshow("Controls", controls_img)
    cv2.createTrackbar("Config", "Controls", 0, 2, create)
    cv2.createTrackbar("Background", "Controls", 0, 1, empty)
    cv2.createTrackbar("Ink/Erase", "Controls", 0, 1, empty)
    cv2.createTrackbar("Color", "Controls", 0, 7, setColor)
    cv2.createTrackbar("Size", "Controls", 0, 3, size)
    cv2.setTrackbarPos("Size", "Controls", 1)
    cv2.createTrackbar("Clear", "Controls", 0, 1, clear)
    cv2.createTrackbar("Exit", "Controls", 0, 1, end)

    txt = open("config.txt", "r")  # Fetching color values from save file
    cm, cs = map(str.rstrip, txt.readlines())
    txt.close()
    cmm = [int(num) for num in cm.strip("[]").split(",")]
    css = [int(num) for num in cs.strip("[]").split(",")]
    lowermain = np.array([cmm[0], cmm[2], cmm[4]])
    uppermain = np.array([cmm[1], cmm[3], cmm[5]])
    lowerside = np.array([css[0], css[2], css[4]])
    upperside = np.array([css[1], css[3], css[5]])


def clear(num):  # Clearing annotation completely
    global annotation
    if num == 1:
        annotation.clear()
        cv2.setTrackbarPos("Clear", "Controls", 0)


def setColor(num):  # Changing color in the UI and screen
    global colorg, controls_img
    colors = [
        (0, 0, 0),
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 0),
        (0, 255, 255),
        (255, 0, 255),
        (255, 255, 0),
        (255, 255, 255),
    ]
    colorg = colors[num]
    cv2.rectangle(controls_img, (10, 10), (190, 90), colorg, -1)
    cv2.imshow("Controls", controls_img)


def size(num):
    global sizeg
    if num == 0:
        sizeg = 5
    elif num == 1:
        sizeg = 10
    elif num == 2:
        sizeg = 15
    elif num == 3:
        sizeg = 20


def update(none):  # Update color parameters
    global lowermain, uppermain, lowerside, upperside, cmm
    lowermain = np.array([cmm[0], cmm[2], cmm[4]])
    uppermain = np.array([cmm[1], cmm[3], cmm[5]])
    lowerside = np.array([css[0], css[2], css[4]])
    upperside = np.array([css[1], css[3], css[5]])
    # colorDetect(frame)


def empty(x):  # Necessary function for some trackbars
    pass


def save(
    num,
):  # After changing color values with config this function saves it to txt file
    global lowermain, uppermain, lowerside, upperside, cmm, css
    if num == 1:
        # print(lowermain)
        # print(uppermain)
        # print(cmm)
        # print(css)
        file = open("config.txt", "w")
        file.write("{}\n".format(cmm))
        file.write("{}\n".format(css))
        file.close()
        if cv2.getWindowProperty("Main Color", cv2.WND_PROP_VISIBLE) > 0:
            cv2.destroyWindow("Main Color")
            cv2.destroyWindow("1")
        elif cv2.getWindowProperty("Side Color", cv2.WND_PROP_VISIBLE) > 0:
            cv2.destroyWindow("Side Color")
            cv2.destroyWindow("2")
        cv2.setTrackbarPos("Config", "Controls", 0)


def create(a):  # Create trackbar windows depending on the number
    if a == 1:
        cv2.namedWindow("Main Color")
        cv2.resizeWindow("Main Color", 640, 260)
        cv2.createTrackbar("Hue min", "Main Color", cmm[0], 179, update)
        cv2.createTrackbar("Hue max", "Main Color", cmm[1], 179, update)
        cv2.createTrackbar("Sat min", "Main Color", cmm[2], 255, update)
        cv2.createTrackbar("Sat max", "Main Color", cmm[3], 255, update)
        cv2.createTrackbar("Val min", "Main Color", cmm[4], 255, update)
        cv2.createTrackbar("Val max", "Main Color", cmm[5], 255, update)
        cv2.createTrackbar("Save", "Main Color", 0, 1, save)

        if cv2.getWindowProperty("Side Color", cv2.WND_PROP_VISIBLE) > 0:
            cv2.destroyWindow("Side Color")
            cv2.destroyWindow("2")
    elif a == 2:
        cv2.namedWindow("Side Color")
        cv2.resizeWindow("Side Color", 640, 260)
        cv2.createTrackbar("Hue min", "Side Color", css[0], 179, update)
        cv2.createTrackbar("Hue max", "Side Color", css[1], 179, update)
        cv2.createTrackbar("Sat min", "Side Color", css[2], 255, update)
        cv2.createTrackbar("Sat max", "Side Color", css[3], 255, update)
        cv2.createTrackbar("Val min", "Side Color", css[4], 255, update)
        cv2.createTrackbar("Val max", "Side Color", css[5], 255, update)
        cv2.createTrackbar("Save", "Side Color", 0, 1, save)

        if cv2.getWindowProperty("Main Color", cv2.WND_PROP_VISIBLE) > 0:
            cv2.destroyWindow("Main Color")
            cv2.destroyWindow("1")
    else:
        if cv2.getWindowProperty("Main Color", cv2.WND_PROP_VISIBLE) > 0:
            cv2.destroyWindow("Main Color")
            cv2.destroyWindow("1")
        elif cv2.getWindowProperty("Side Color", cv2.WND_PROP_VISIBLE) > 0:
            cv2.destroyWindow("Side Color")
            cv2.destroyWindow("2")


def colorPick(number):  # Assigning color values to variables
    global cmm, css
    if number == 1 and cv2.getWindowProperty("Main Color", cv2.WND_PROP_VISIBLE) > 0:
        cmm[0] = cv2.getTrackbarPos("Hue min", "Main Color")
        cmm[1] = cv2.getTrackbarPos("Hue max", "Main Color")
        cmm[2] = cv2.getTrackbarPos("Sat min", "Main Color")
        cmm[3] = cv2.getTrackbarPos("Sat max", "Main Color")
        cmm[4] = cv2.getTrackbarPos("Val min", "Main Color")
        cmm[5] = cv2.getTrackbarPos("Val max", "Main Color")
        # file = open("config.txt", "+r")
    elif number == 2 and cv2.getWindowProperty("Side Color", cv2.WND_PROP_VISIBLE) > 0:
        css[0] = cv2.getTrackbarPos("Hue min", "Side Color")
        css[1] = cv2.getTrackbarPos("Hue max", "Side Color")
        css[2] = cv2.getTrackbarPos("Sat min", "Side Color")
        css[3] = cv2.getTrackbarPos("Sat max", "Side Color")
        css[4] = cv2.getTrackbarPos("Val min", "Side Color")
        css[5] = cv2.getTrackbarPos("Val max", "Side Color")


def end(num):  # End Program
    return True if num == 1 else False


def draw(img, mask, maskside, bgor):  # Multipurpose function
    global colorg, sizeg, annotation, previous

    bgr = bgor.copy()  # Background
    dot = img if cv2.getTrackbarPos("Background", "Controls") == 1 else bgr
    ret, threshold = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)  #
    contours, hierarchy = cv2.findContours(
        threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    for anot in annotation:  # Drawing previous saved annotations on current board
        cv2.circle(dot, (anot[0], anot[1]), anot[2], anot[3], -1)
        if anot[4] != None:
            cv2.line(
                dot, (anot[4][0], anot[4][1]), (anot[0], anot[1]), anot[3], anot[2] * 2
            )

    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area > 200:
            moments = cv2.moments(contour)
            center_x = int(moments["m10"] / moments["m00"])
            center_y = int(
                moments["m01"] / moments["m00"]
            )  # Assigning current x and y coordinates of pen
            size = 10  # For Cursor sign
            thickness = 2  # For Cursor sign
            color = (
                (170, 170, 170) if colorg == (0, 0, 0) else (0, 0, 0)
            )  # For Cursor sign
            if cv2.getTrackbarPos("Ink/Erase", "Controls") == 0:
                # cv2.line(
                #     dot,
                #     (center_x - size, center_y),
                #     (center_x + size, center_y),
                #     color,
                #     thickness,
                # )
                # cv2.line(
                #     dot,
                #     (center_x, center_y - size),
                #     (center_x, center_y + size),
                #     color,
                #     thickness,
                # )  # Cursor sign
                cv2.circle(dot, (center_x, center_y), sizeg, colorg, -1)
                cv2.circle(dot, (center_x, center_y), sizeg + 1, (170, 170, 170), 2)

            else:
                cv2.circle(dot, (center_x, center_y), 20, (255, 255, 255), -1)
                cv2.circle(dot, (center_x, center_y), 21, (0, 0, 0), 1)

            contourside, _ = cv2.findContours(
                maskside, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            # Our control color for drawing or not
            for contoursi in contourside:
                contourside_area = cv2.contourArea(contoursi)
                # print(contourside_area)
                # contourside_area = 600
                if (
                    contourside_area > 200
                    and cv2.getTrackbarPos("Ink/Erase", "Controls") == 0
                ):  #
                    anot = (center_x, center_y, sizeg, colorg, previous)
                    annotation.append(anot)
                    previous = (anot[0], anot[1])

                elif (
                    contourside_area > 200
                    and cv2.getTrackbarPos("Ink/Erase", "Controls") == 1
                ):
                    erasepoints = []
                    for anot in annotation:
                        if (
                            anot[0] - 20 < center_x < anot[0] + 20
                            and anot[1] - 20 < center_y < anot[1] + 20
                        ):  # Making wider area for eraser, otherwise eraser area is only one pixels
                            erasepoints.append(anot)
                    for point in erasepoints:
                        annotation.remove(point)
                else:
                    previous = None

    if (
        cv2.getTrackbarPos("Config", "Controls") > 0
        or cv2.getTrackbarPos("Background", "Controls") == 1
    ):
        if cv2.getTrackbarPos("Config", "Controls") == 0:
            cv2.imshow("Board", dot)
        elif cv2.getTrackbarPos("Config", "Controls") == 1:
            cv2.imshow("1", mask)
        else:
            cv2.imshow("2", maskside)

    else:
        if cv2.getWindowProperty("1", cv2.WND_PROP_VISIBLE) > 0:
            cv2.destroyWindow("1")
            # cv2.destroyWindow("2")
        cv2.imshow("Board", dot)


def colorDetect(img):
    global lowermain, uppermain, lowerside, upperside, cmm
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lowermain, uppermain)
    maskside = cv2.inRange(imgHSV, lowerside, upperside)
    final = cv2.bitwise_and(img, img, mask=mask)
    final2 = cv2.bitwise_and(img, img, mask=maskside)
    finalli = cv2.bitwise_and(img, img, mask=(mask + maskside))

    return mask, maskside


# contour, hierarchy kısmında retr_external işlem yükü bindiriyor. Onun yerine yalnızca köşeleri alıp bri şekilde halledebilirim
