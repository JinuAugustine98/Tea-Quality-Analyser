import cv2
import numpy as np

def contour_area(input_image, save_path, calibration):
    img = cv2.imread(input_image, cv2.IMREAD_UNCHANGED)

    #convert img to grey
    img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #set a thresh
    thresh = 100

    #get threshold image
    ret,thresh_img = cv2.threshold(img_grey, thresh, 100, cv2.THRESH_BINARY)
    #find contours
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort in descending order of area
    desc = contours.sort (key = lambda x: cv2.contourArea (x), reverse = True)

    out = np.zeros_like (img)

    # Extract the second largest contour
    cv2.drawContours (out, [contours [1]], -1, color = 255, thickness = -1)
    pixel_area = cv2.contourArea(contours [1])
    actual_area = pixel_area/calibration
    print("Calculated Area: {}cm2".format(actual_area))

    path1 = save_path+'/contour_area.png'
    cv2.imwrite (path1, out)

    #create an empty image for contours
    img_contours = np.zeros(img.shape)
    # draw the contours on the empty image
    cv2.drawContours(img_contours, contours, -1, (0,255,0), 3)
    #save image
    path2 = save_path+'/contours.png'
    cv2.imwrite(path2,img_contours)
    return actual_area