import cv2
import numpy as np
import math
import pyvjoy

def advanceCamera():
    j = pyvjoy.VJoyDevice(1)


    def xAxis(angle):
        bearing = 16834 - int((angle / 90) * 16384)
        j.set_axis(pyvjoy.HID_USAGE_X, bearing)


    def reCentre():
        j.set_button(2, 0)
        j.set_button(1, 0)
        j.set_axis(pyvjoy.HID_USAGE_Y, 0x0000)
        j.set_button(1, 0)


    def yAxis(speed):
        j.set_button(2, 0)
        acceleration = int((speed / 100) * 32678)
        j.set_axis(pyvjoy.HID_USAGE_Y, acceleration)


    def Brake():
        j.set_button(1, 0)
        j.set_button(2, 1)


    cap = cv2.VideoCapture(0)
    Dir = "-->"

    while (1):

        _, img = cap.read()
        im = img
        img = img[150:450, 80:500]  # Define RegionOfInterest
        im = cv2.rectangle(im, (500, 150), (80, 450), (0, 255, 0), 2)

        lower = np.array([0, 20, 150])  # HSV ranges for skin color
        upper = np.array([20, 255, 255])

        converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # convert BGR image to HSV image
        mask0 = cv2.inRange(converted, lower, upper)
        mask0 = cv2.morphologyEx(mask0, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask0 = cv2.morphologyEx(mask0, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
        skin = cv2.bitwise_and(img, img, mask=mask0)
        contours, hierarchy = cv2.findContours(mask0, cv2.RETR_TREE,
                                                    cv2.CHAIN_APPROX_SIMPLE)  # fit contours to hand regions

        try:

            cnt = max(contours, key=lambda x: cv2.contourArea(x))
            for ind, ct in enumerate(contours):  # Iterate over all contours in frame
                M = cv2.moments(contours[ind])
                area = int(M["m00"])
                if area in range(6000, 13000):  # Ignore other contours that are not of hands
                    m1 = cv2.moments(contours[0])
                    m2 = cv2.moments(contours[1])
                    x1 = int(m1["m10"] / m1["m00"])
                    y1 = int(m1["m01"] / m1["m00"])
                    x2 = int(m2["m10"] / m2["m00"])
                    y2 = int(m2["m01"] / m2["m00"])
                    slope = math.tan(((y2 - y1) / (x2 - x1))) * 100  # convert the slope into %
                    slope = round(slope, 2)

                    if slope > 0:
                        Dir = "<--"
                    else:
                        Dir = "-->"

                    distance = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
                    distance = round((distance / 300) * 100, 2)  # convert distance from 0 - 300 into %

                    if (distance > 100):  # limit distance to 100
                        distance = 100
                    if slope > 100:  # limit angle to 100
                        slope = 100
                    elif slope < -100:
                        slope = -100

                    cv2.line(im, (x1, y1), (x2, y2), (100, 255, 0), 5)  # plot line between centres of two hands
                    cv2.putText(im, "Turning:" + Dir + str(slope) + "deg", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (255, 255, 255), 2)
                    cv2.putText(im, "Acceleration:" + (str(distance)), (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 255, 0), 2)
                    xAxis(slope)  # set xAxis on Joystick to the slope %
                    yAxis(distance)  # set yAxis on Joystick to speed %

                else:
                    if area > 20000:  # If area is of two hands joined
                        cv2.putText(im, "BRAKE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
                        Brake()

        except ValueError:  # If hands are out of the frame
            reCentre()

        except:
            pass

        cv2.imshow('main cam', im)
        cv2.imshow('segment', skin)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()

