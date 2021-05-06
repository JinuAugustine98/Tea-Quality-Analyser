import cv2 as cv

def pad(input_image, save_path):
    # imageName = '/Users/jinuaugustine/Downloads/out.png'

    src = cv.imread(cv.samples.findFile(input_image), cv.IMREAD_COLOR)

    borderType = cv.BORDER_CONSTANT

    top = int(0.05 * src.shape[0])  # shape[0] = rows
    bottom = top
    left = int(0.05 * src.shape[1])  # shape[1] = cols
    right = left

    value = [255, 255, 255]
            
    dst = cv.copyMakeBorder(src, top, bottom, left, right, borderType, None, value)

    path = save_path+'/padded.png'
    cv.imwrite(path, dst)
    return None
