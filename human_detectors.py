import numpy as np
import cv2


class Human_Detectors(object):
    # Class to detect objects in a frame
    def __init__(self):
        
        self.sub = cv2.createBackgroundSubtractorMOG2()

    def Detect(self, frame):
        """ 
        Detects objects in the single video frame with the following steps:
        1. Convert frame in gray scale
        2. Apply background subtraction
        3. Apply some morphology techniques
        4. Get contours
        5. Get centroid of the contours using cv2.Moments
        6. Draw rectangle around the contour.
        7. Collect all the center points in a list and return the list 
        
        """

        # Convert BGR to GRAY
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #apply background substraction to the grey colored image
        fgmask = self.sub.apply(gray)
        # initialize a kernel to apply to morphological trnasformation to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        # Closing is reverse of Opening, Dilation followed by Erosion
        closing = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
        # Opening is just another name of erosion followed by dilation
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        # increases the white region in the image or size of foreground object increases
        dilation = cv2.dilate(opening, kernel)
        # setting all pixel values above 220 to be 255 - shadow removal
        retvalbin, bins = cv2.threshold(dilation, 220, 255, cv2.THRESH_BINARY)
        _, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        minimum_area = 400
        maximum_area = 50000
        centers = []
        # goes through all contours in a single frame
        for x in range(len(contours)):
            # checks only for the parent contour
            if hierarchy[0, x, 3] == -1:
                #calculate area for each contour to place the bounding box
                contour_area = cv2.contourArea(contours[x])
                if minimum_area<contour_area<maximum_area:
                    #cont_num+=1
                    cont = contours[x]
                    # compute the centre of the contour 
                    M = cv2.moments(cont)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    centroid = (cx,cy)
                    b = np.array([[cx], [cy]])
                    centers.append(np.round(b))
                    # find coordinats of straight bounding rectangle of a contour
                    x_coord, y_coord, width, height = cv2.boundingRect(cont)
                    # draw a rectangle around the contour
                    cv2.rectangle(frame, (x_coord, y_coord), (x_coord + width, y_coord + height), (0, 255, 0), 2)
                    cv2.putText(frame, str(cx) + "," + str(cy), (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX,.3, (0, 0, 255), 1)
                    cv2.drawMarker(frame, (cx, cy), (0, 255, 255), cv2.MARKER_SQUARE, markerSize=6, thickness=2,line_type=cv2.LINE_8)

        return centers
