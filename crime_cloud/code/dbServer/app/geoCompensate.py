#!/usr/bin/env python3

class GeoCompensate():

    # The approximate area of Yarra, the smallest district in our LGA file
    THRESHOLD = 0.00205152

    def geoCompensate(self, box):

        xmax = box[2][0]
        xmin = box[0][0]
        ymax = box[2][1]
        ymin = box[0][1]

        area = (ymax - ymin) * (xmax - xmin)

        if area <= self.THRESHOLD:
            x_coordinate = (xmax + xmin) / 2
            y_coordinate = (ymax + ymin) / 2
            return [x_coordinate, y_coordinate]
        else:
            return []


  