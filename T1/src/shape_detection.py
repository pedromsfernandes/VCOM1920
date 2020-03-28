import cv2
import numpy as np
import imutils


def circleDetection(image, res, color):
    grayscale = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
    grayscale = cv2.cvtColor(grayscale, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(grayscale, 5)

    cimg = image.copy()

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 50,
                               param1=50, param2=30, minRadius=2, maxRadius=0)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
            # get boundary of this text
            writeText(cimg, color + " circle", 0.6, i[0], i[1])

    return cimg


def writeText(img, text, size, x, y):
    textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, size, 2)[0]
    # get coords based on boundary
    textX = int((x - (textsize[0] / 2)))
    cv2.putText(img, text, (textX, y),
                cv2.FONT_HERSHEY_SIMPLEX, size, (0, 255, 0), 2)


def triangleDetection(image, res, color):
    img = image.copy()
    gray = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 50, 200)
    contours, hier = cv2.findContours(canny, 1, 2)
    tri = []

    if contours is not None and len(contours) != 0:
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
            if len(approx) == 3:
                cv2.drawContours(img, [cnt], 0, (0, 255, 0), 2)
                tri = approx

        if len(tri) != 0:
            x, y = triangleCenter(tri[0], tri[1], tri[2])
            writeText(img, color + " triangle", 0.6, x, y)
            for vertex in tri:
                cv2.circle(img, (vertex[0][0], vertex[0][1]), 5, 255, -1)

    return img


def triangleCenter(vertex1, vertex2, vertex3):
    return [int((vertex1[0][0] + vertex2[0][0] + vertex3[0][0])/3), int((vertex1[0][1] + vertex2[0][1] + vertex3[0][1])/3)]


def lineDetection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    minLineLength = 100
    maxLineGap = 10
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100,
                            minLineLength, maxLineGap)

    if lines is not None:
        for i in range(0, len(lines)):
            for x1, y1, x2, y2 in lines[i]:
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return image


def rectangleDetection(image, res, color):
    img = image.copy()
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 120, 255, 1)

    cv2.imshow('canny', canny)

    # Find contours
    cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Iterate thorugh contours and draw rectangles around contours
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w > 30 and h > 30:
            cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)
            x, y = rectangleCenter(x, y, x+w, y + h)
            writeText(img, color + " rectangle", 0.6, x, y)

    return img


def rectangleCenter(x1, y1, x2, y2):
    return [int((x1 + x2)/2), int((y1 + y2)/2)]