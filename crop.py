import os
from PIL import Image
import pandas as pd 

def box_crop(input_image,coordinates, parent_dir2):
    # im = Image.open(r'/Users/jinuaugustine/Downloads/test4.jpeg')
    # coordinates = '/Users/jinuaugustine/Downloads/conoor (1).csv'


    im = Image.open(input_image, 'r')
    df = pd.read_csv(coordinates)
    x = 1
    for index, row in df.iterrows():
        directory2 = "Leaf No. {}".format(x)
        path = os.path.join(parent_dir2, directory2)
        os.mkdir(path)

        left = row["Left"]
        top = row['Top']
        right = row['Right']
        bottom = row['Bottom']
        
        im1 = im.crop((left, top, right, bottom))

        path = parent_dir2+"/"+directory2+"/detected_leaf.jpg"
        im1.save(path)
        x += 1
    return None