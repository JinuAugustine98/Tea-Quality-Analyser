from color_analyser import DominantColors

def profiler(img):
    # img = '/Users/jinuaugustine/Downloads/det_leaf.jpg'
    clusters = 5
    dc = DominantColors(img, clusters)
    colors = dc.dominantColors()
    print(colors)
    dc.plotHistogram()

    c_prof = colors.tolist()

    dr1 = c_prof[0][0]
    dg1 = c_prof[0][1]
    db1 = c_prof[0][2]

    print(dr1, dg1, db1)

    dr2 = c_prof[1][0]
    dg2 = c_prof[1][1]
    db2 = c_prof[1][2]

    print(dr2, dg2, db2)

    dr3 = c_prof[2][0]
    dg3 = c_prof[2][1]
    db3 = c_prof[2][2]

    print(dr3, dg3, db3)

    dr4 = c_prof[3][0]
    dg4 = c_prof[3][1]
    db4 = c_prof[3][2]

    print(dr4, dg4, db4)

    dr5 = c_prof[4][0]
    dg5 = c_prof[4][1]
    db5 = c_prof[4][2]

    print(dr5, dg5, db5)
    return c_prof