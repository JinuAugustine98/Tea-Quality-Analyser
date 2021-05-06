from PIL import Image
import pandas as pd 

def box_crop(input_image,coordinates):
    # im = Image.open(r'/Users/jinuaugustine/Downloads/test4.jpeg')
    # coordinates = '/Users/jinuaugustine/Downloads/conoor (1).csv'   
    im = Image.open(input_image, 'r')
    df = pd.read_csv(coordinates)
    x = 1
    for index, row in df.iterrows():
        left = row["Left"]
        top = row['Top']
        right = row['Right']
        bottom = row['Bottom']
        
        im1 = im.crop((left, top, right, bottom))

        im1.save("/Users/jinuaugustine/Documents/Fine Leaf/Processing/detected_leaf_"+str(x)+".jpg")
        x += 1
    return None