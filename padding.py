from PIL import Image

def pad(input_image, save_path):
    # imageName = '/Users/jinuaugustine/Downloads/out.png'

    image = Image.open(input_image)

    right = 10
    left = 10
    top = 10
    bottom = 10

    width, height = image.size

    new_width = width + right + left
    new_height = height + top + bottom

    result = Image.new(image.mode, (new_width, new_height), (255, 255, 255))

    result.paste(image, (left, top))

    path = save_path+'/padded.png'

    result.save(path)
    return None