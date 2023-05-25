import time

import cv2
from math import sqrt

cap = cv2.VideoCapture('video.mp4')

leftCounter = 0
rightCounter = 0

summCx = 0
summCy = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    height = frame.shape[0]
    width = frame.shape[1]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    ret, thresh = cv2.threshold(gray, 105, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        cx = int(x + w / 2)
        cy = int(y + h / 2)
        summCx += cx
        summCy += cy
        print("Center: x=" + str(cx) + ", y=" + str(cy))
        cv2.putText(frame, "Center: x=" + str(cx) + ", y=" + str(cy), (5, 15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0))

        cv2.putText(frame, "Distance to image center: " + str(
            "%.2f" % sqrt((width / 2 - cx) * (width / 2 - cx) + (height / 2 - cy) * (height / 2 - cy))), (5, 30),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0))

        centered = False
        if abs(width / 2 - cx) < 100 and abs(height / 2 - cy) < 100:
            centered = True

        left = False
        if cx < width / 2:
            left = True
            leftCounter += 1
        else:
            rightCounter += 1

        cv2.putText(frame, "Left: " + str(leftCounter), (5, 45), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255) if left else (0, 0, 0))
        cv2.putText(frame, "Right: " + str(rightCounter), (5, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (255, 0, 0) if not left else (0, 0, 0))

        cv2.circle(frame, (cx, cy), int(sqrt(w * w / 4 + h * h / 4)), (0, 255, 0) if centered else (0, 0, 255), 2)

        cv2.line(frame, (cx, 0), (cx, height), (255, 0, 0), 1)
        cv2.line(frame, (0, cy), (width, cy), (255, 0, 0), 1)

        cv2.putText(frame, "Sobj/Simg: " + str("%.2f" % (w * h / width / height * 100)) + "%", (5, 90),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0))

    cv2.imshow('frame', frame)

    waitKey = cv2.waitKey(1)

    if waitKey & 0xFF == ord('p'):
        while cv2.waitKey(1) & 0xFF != ord('p'):
            time.sleep(0.1)

    if waitKey & 0xFF == ord('q'):
        break

    time.sleep(0.1)

print("Avg center: x=" + str("%.2f" % (summCx / (leftCounter + rightCounter + 1))) + ", y=" + str(
    "%.2f" % (summCy / (leftCounter + rightCounter + 1))))

cap.release()
cv2.destroyAllWindows()
