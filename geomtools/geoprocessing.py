"""
Tools for manipulating geometry objects (geojson probably)
"""
from geojson import LineString, Feature, FeatureCollection
import math, random

def select_random_polygons(polygons_collection, fraction):

    """
    Return a random sample of polygons from a collection of polygons. The
    area_fraction parameter controls number of polygons returned based on areas

    polygons_collection -> geojson.FeatureCollection
    fraction -> float 0 to 1

    Example:
        import geojson
        with open (r'path/to/polygons.json') as geojsonfile:
            polygons = geojson.load(geojsonfile)

            #select a sample of 25% of the area
            select_random_polygons(polygons, 0.25)
    """

    polygons = polygons_collection['features']
    total_area = sum([x['properties']['SHAPE_Area'] for x in polygons])
    print 'total_area = {}ac'.format(round(total_area/43560, 2))
    f = selected_area = 0.0 #current area fraction
    selected_polygons = []
    while f <= fraction:

        #select a random shed
        poly = random.choice(polygons)
        selected_polygons.append(poly) #append to our list
        polygons.remove(poly) #so sheds are selected more than once

        #recalculate the area fraction
        selected_area += poly['properties']['SHAPE_Area']
        f = selected_area / total_area

    print 'selected area = {}ac'.format(round(selected_area/43560, 2))

    return selected_polygons

def lines_from_ring_polygons(feature_collection):

    """
    given a FeatureCollection of polygons, this function creates a
    FeatureCollection of lines for each outer vertex in each ringed-polygon.
    Lines are produced from the outer verticies to their closest vertex on the
    inner ring. Useful for using the output lines to cut the ringed polygons.

    Used to split right-of-way rings to represent potential GSI drainage areas.
    """

    #find the closest inner ring vertex to each outer ring vertex,
    #make lines, use these lines to cut the original ringed polygons

    def dist(xy1, xy2):

        a = xy2[0] - xy1[0]
        b = xy2[1] - xy1[1]
        return math.hypot(a, b)

    linefeatures =[]
    for feature in feature_collection['features']:
        #the outer ring
        #print len(feature['geometry']['coordinates'])
        if len(feature['geometry']['coordinates']) > 1:
            outerring = feature['geometry']['coordinates'][0]
            innerring = feature['geometry']['coordinates'][1]

            for outer in outerring:
                dmin = 999999999.0
                pair = [outer, None]

                for inner in innerring:

                    d = dist(outer, inner)
                    if d < dmin:
                        pair[1] = inner
                        dmin = d

                #print pair
                line = LineString(pair)
                feature = Feature(geometry=line)
                linefeatures.append(feature)


    return FeatureCollection(features=linefeatures)
