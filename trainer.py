import os
import cv2
import pandas as pd
from sklearn.utils.extmath import density 
import mysql.connector
from mysql.connector import connect, Error
from measure import smart_measure
from crop import box_crop
from color_profiler import DominantColors
from padding import pad
from dominant_color import colorify
from contour import contour_area


try:
    db = mysql.connector.connect(
        host="soli-db.ciksb20swlbf.ap-south-1.rds.amazonaws.com",
        user='teaquality',
        password='Quality@123',
        database="db_tea_quality_record"
        )
    print("MySQL Database Connected Successfully!")
except Error as e:
    print(e)


test_image = '/Users/jinuaugustine/Documents/Solidaridad/Tea-Quality-Analyser/conoor test data/3.jpeg'
detected_leaf_coordinates = '/Users/jinuaugustine/Documents/Solidaridad/Tea-Quality-Analyser/conoor test data/drive-download-20210507T080641Z-001/conoor3.csv'

df = pd.read_csv(detected_leaf_coordinates)
no_leaves = len(df.index)
batch = 4

parent_dir1 = "/Users/jinuaugustine/Documents/Solidaridad/Tea-Quality-Analyser/Processing"
directory1 = "Leaf Batch {}".format(batch)
path = os.path.join(parent_dir1, directory1)
os.mkdir(path)
print("\nDirectory {} created".format(directory1))

parent_dir2 = "/Users/jinuaugustine/Documents/Solidaridad/Tea-Quality-Analyser/Processing/Leaf Batch {}".format(batch)

calibration = smart_measure(test_image, parent_dir2)
print("\nDetected Calibration: {}pixel/cm2".format(calibration))

print("\n\nCropping Detected {} Leaves.....".format(no_leaves))
box_crop(test_image, detected_leaf_coordinates, parent_dir2)

print("\n\nStarting Pre-Processing of Cropped Leaves.....")

j = 1
total_area = 0
density = 0.05605907050990364

data1 = []
quality = 1     #1=Good 0=Bad
db = pd.DataFrame(data1, columns = ['Leaf Batch', 'Detected Leaf', 'Left Position', 'Top Position', 'Right Position', 'Bottom Position', 'Dominant Color 1 (R)','Dominant Color 1 (G)','Dominant Color 1 (B)','Dominant Color 1 Hz','Dominant Color 2 (R)','Dominant Color 2 (G)','Dominant Color 2 (B)', 'Dominant Color 2 Hz', 'Dominant Color 3 (R)','Dominant Color 3 (G)','Dominant Color 3 (B)','Dominant Color 3 Hz', 'Dominant Color 4 (R)','Dominant Color 4 (G)','Dominant Color 4 (B)','Dominant Color 4 Hz', 'Dominant Color 5 (R)','Dominant Color 5 (G)','Dominant Color 5 (B)','Dominant Color 5 Hz', 'Calibration', 'Leaf Area', 'Leaf Density', 'Leaf Weight', 'Quality'])
columns = list(df)
for x in range(no_leaves):

    left = df['Left'].iloc[j-1]
    top = df['Top'].iloc[j-1]
    right = df['Right'].iloc[j-1]
    bottom = df['Bottom'].iloc[j-1]

    img_path = "/Users/jinuaugustine/Documents/Solidaridad/Tea-Quality-Analyser/Processing/Leaf Batch {}/Leaf No. {}".format(batch, j)

    profile_path = img_path+"/detected_leaf.jpg"
    print("\nAnalysing Color Profile of Leaf {}".format(j))

    clusters = 5
    dc = DominantColors(profile_path, img_path, clusters)
    colors = dc.dominantColors()
    print(colors)
    hist = dc.plotHistogram()

    c_prof = colors.tolist()
    
    dr1 = c_prof[0][0]
    dg1 = c_prof[0][1]
    db1 = c_prof[0][2]

    dr2 = c_prof[1][0]
    dg2 = c_prof[1][1]
    db2 = c_prof[1][2]

    dr3 = c_prof[2][0]
    dg3 = c_prof[2][1]
    db3 = c_prof[2][2]

    dr4 = c_prof[3][0]
    dg4 = c_prof[3][1]
    db4 = c_prof[3][2]

    dr5 = c_prof[4][0]
    dg5 = c_prof[4][1]
    db5 = c_prof[4][2]

    d1hz = hist[0]
    d2hz = hist[1]
    d3hz = hist[2]
    d4hz = hist[3]
    d5hz = hist[4]


    print("\nPadding Leaf {}".format(j))
    pad(profile_path, img_path)

    color_path = img_path+'/padded.png'
    print("\nFinding Dominant Color of Leaf {}".format(j))
    colorify(color_path, img_path)


    try:
        contour_path = img_path+'/dominant_color.jpg'
        print("\nFinding Contour and Area of Leaf {}".format(j))
        lf_area = contour_area(contour_path, img_path, calibration)
    except:
        contour_path = profile_path
        print("\nFinding Contour and Area of Leaf {}".format(j))
        lf_area = contour_area(contour_path, img_path, calibration)

    lf_weight = lf_area*density
    total_area+=lf_area
    j+=1

    values = [batch, j, left, top, right, bottom, dr1, dg1, db1, d1hz, dr2, dg2, db2, d2hz, dr3, dg3, db3, d3hz, dr4, dg4, db4, d4hz, dr5, dg5, db5, d5hz, calibration, lf_area, density, lf_weight, quality]
    zipped = zip(columns, values)
    new_dict = dict(zipped)
    data1.append(new_dict)

db = db.append(data1, True)
# print(df)
# db.to_csv('/Users/jinuaugustine/Documents/Tea-Quality-Analyser/Processing/leaf_data.csv')

# total_area+=105
# known_weight = 11.72
# calc_density = known_weight/total_area
# print("\n\nLeaf Density: {}gm/cm2".format(calc_density))
weight = total_area*density
print("\nTotal Leaf Area: {}cm2".format(total_area))
print("\nTotal Weight Calculated: {}gm".format(weight))