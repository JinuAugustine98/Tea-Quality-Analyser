from PIL import Image

def resizer(image):
    # image = Image.open('/Users/jinuaugustine/Downloads/det_leaf.jpg', 'r')
    image_size = image.size
    width = image_size[0]
    height = image_size[1]

    if(width != height):
        bigside = width if width > height else height

        background = Image.new('RGBA', (bigside, bigside), (255, 255, 255, 255))
        offset = (int(round(((bigside - width) / 2), 0)), int(round(((bigside - height) / 2),0)))

        background.paste(image, offset)
        background.save('/Users/jinuaugustine/Documents/Fine Leaf/Processing/out.png')
        print("Image has been resized !")

    else:
        print("Image is already a square, it has not been resized !")
    return background