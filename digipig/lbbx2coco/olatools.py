import re
import numpy as np

def ret_area_of_bb(bb):
    area = int( bb[2]*bb[3] )
    return area

def intify_filename(filename):
    img_id = filename.replace("Mon", "1").replace("Tue", "2").replace("Wed", "3").replace("Thu", "4").replace("Fri", "5").replace("Sat", "6").replace("Sun", "7")
    img_id = img_id.replace("noon", "1").replace("orning", "0") #why? because of inconsistent naming

    #intify string
    listOfAllDigitsInFilename = (re.findall('\d+', img_id ))
    stringOfAllDigitsInFilename = ''.join(listOfAllDigitsInFilename)
    id = int(stringOfAllDigitsInFilename)
    return id

def create_polygon_from_point(xy_center_list):

    half_of_BB_dim = 50/2 #this works for tails in batch1

    x_min = int( xy_center_list[0] - half_of_BB_dim )
    y_min = int( xy_center_list[1] - half_of_BB_dim )
    x_max = int( xy_center_list[0] + half_of_BB_dim )
    y_max = int( xy_center_list[1] + half_of_BB_dim )

    polygon = [[x_min, y_min,
                x_min, y_max,
                x_max, y_max,
                x_max, y_min]]

    return polygon

def create_BB_from_polygon(polygon):
    x_min = int(polygon[0])
    y_min = int(polygon[1])
    x_max = y_max = 0

    for i in range(len(polygon)):
        if (i % 2) == 0:             #this is x coordinates
            if polygon[i]<x_min:
                x_min = polygon[i]
            elif polygon[i]>x_max:
                x_max = polygon[i]
        else:                        #this is y coordinates
            if polygon[i]<y_min:
                y_min = polygon[i]
            elif polygon[i]>y_max:
                y_max = polygon[i]

    height = int(x_max-x_min)
    width = int(y_max - y_min)
    bb = [x_min, y_min, width, height]

    return bb

def get_xy_pairs_vector_from_xyxy_list(xyxy_list):
    if (len(xyxy_list)%2) != 0:
        print("list: ", xyxy_list)
        print("len list: ", len(xyxy_list)%2)
        print("go figure! ") 
        #logging.warning("this is wrong polygon list must be even")
        return 0
    xy_pairs = [[0,0] for i in range(int(len(xyxy_list)/2))]
    for i in range(len(xy_pairs)):
        xy_pairs[i]= [xyxy_list[i*2],xyxy_list[i*2+1]]
    return xy_pairs
