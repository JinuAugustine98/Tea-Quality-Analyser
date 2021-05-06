import pandas as pd

test_image = '/Users/jinuaugustine/Downloads/test4.jpeg'
detected_leaf_coordinates = '/Users/jinuaugustine/Downloads/conoor.csv'

df = pd.read_csv(detected_leaf_coordinates)
no_leaves = len(df.index)
print(no_leaves)