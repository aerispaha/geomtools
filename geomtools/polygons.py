import geojson
from lines import Line, LineSegment
import random, math


class Bolygon(geojson.Polygon):

    """
    polygon class with more fancy properties
    """
    def __init__(self, coordinates):

        self.coordinates = coordinates
        self.xmin = min([xy[0] for xy in self.coordinates])
        self.ymin = min([xy[1] for xy in self.coordinates])
        self.xmax = max([xy[0] for xy in self.coordinates])
        self.ymax = max([xy[1] for xy in self.coordinates])
        self.bbox = [self.xmin, self.ymin, self.xmax, self.ymax]

        #collect the line segments
        self.line_segments = [LineSegment([coordinates[i], coordinates[i+1]])
                              for i in range(len(coordinates)-1)]

        #find angles between each segment
        xysecondtolast = coordinates[-2:][0]


        for i in range(len(coordinates)-1):
            pass


    def __str__(self):

        return geojson.dumps(geojson.Polygon([self.coordinates]))

    pass




class MyPolygon(object):
    def __init__(self, coordinates):

        self.coordinates = coordinates
        self.xmin = min([xy[0] for xy in self.coordinates])
        self.ymin = min([xy[1] for xy in self.coordinates])
        self.xmax = max([xy[0] for xy in self.coordinates])
        self.ymax = max([xy[1] for xy in self.coordinates])
        self.bbox = [self.xmin, self.ymin, self.xmax, self.ymax]


    @property
    def __geo_interface(self):
        return {'type': 'Polygon', 'coordinates':[coordinates]}


    def contains_point(self, point):

        coords = self.coordinates #polygon['coordinates'][0]
        lines = []

        #create positive, zero slope ray from point, check for odd
        #number of intersects with polygon (ray casting algorithm)
        #xy2 = (point[0]+999, point[1])
        ray = Line(m=0, b=point[1], x_min=point[0]) #horiz ray to right of point
        #print ray

        #print line segs
        for i in range(0, len(coords)-1):
            linexy = [coords[i], coords[i+1]]

            #print linexy
            line = LineSegment(linexy)
            if ray.intersects_line(line):
                lines.append(line)


        if len(lines) % 2 != 0:
            #print '{} intersection(s)'.format(len(lines))
            return True
        else:
            return False

def angle(xy1, xy2):
    a = xy2[0] - xy1[0]
    b = xy2[1] - xy1[1]
    ang = math.atan2(b, a)
    #print ang
    return ang

def centriod(coordinates):
    sumx = sum([xy[0] for xy in coordinates])
    sumy = sum([xy[1] for xy in coordinates])
    n = float(len(coordinates))
    return (sumx/n, sumy/n)

def poly_contains_point(polygon, point):

    coords = polygon['coordinates'][0] #polygon['coordinates'][0]
    lines = []

    #create positive, zero slope ray from point, check for odd
    #number of intersects with polygon (ray casting algorithm)
    #xy2 = (point[0]+999, point[1])
    ray = Line(m=0, b=point[1], x_min=point[0]) #horiz ray to right of point

    #print line segs
    print 'checking this ray: {}'.format(ray)
    for i in range(0, len(coords)-1):
        linexy = [coords[i], coords[i+1]]
        #print linexy
        line = LineSegment(linexy)
        if ray.intersects_line(line):
            lines.append(line)

    if len(lines) % 2 != 0:
        print '{} intersection(s)'.format(len(lines))
        return True
    else:
        return False


def random_polygon_inside_polygon(container, numverts=3):
    """
    generate a random simple polygon within the container polygon. Doesn't
    guarantee that it will be completely contained, only that the verticies
    are completely contained.
    """

    i=0
    coords = []
    mycontainer = MyPolygon(container['coordinates'][0])
    while i < numverts:
        #loop through until we have n points within the containter
        xy = (random.uniform(mycontainer.xmin, mycontainer.xmax),
              random.uniform(mycontainer.ymin, mycontainer.ymax))

        if mycontainer.contains_point(xy):
            coords.append(xy)
            i +=1
        else:
            print 'outside vert: {}'.format(xy)

    #sort points by angle about centroid
    centroid = centriod(coords)
    sortedverts = sorted(coords, key=lambda xy: angle(xy, centroid))

    #build polygon with first tuple copied at end
    return geojson.Polygon([sortedverts + [sortedverts[0]]])




def clip_poly(inpolygon, container):

    #check if any of the proposed sides intersect the container, if they do
    #add more verticies to "ride the container"
    in_xys = inpolygon['coordinates'][0]
    clipxys = container['coordinates'][0]

    #collect the edge line segments of each polygon
    inlines = [LineSegment([in_xys[i], in_xys[i+1]]) for i in range(len(in_xys)-1)]
    cliplines = [LineSegment([clipxys[i], clipxys[i+1]]) for i in range(len(clipxys)-1)]
    print 'len cliplines {}\nlen inlines {}'.format(len(cliplines), len(inlines))
    for inline in inlines:
        for clipline in cliplines:
            print 'checking {} vs {}'.format(inline, clipline)
            if inline.intersects_line(clipline):
                print '{} XSECTION {}'.format(inline, clipline)

    print '\n\n opss'
    for clipline in cliplines:
        for inline in inlines:
            if clipline.intersects_line(inline):
                print '{} OPP XSECTION {}'.format(clipline, inline)


    #return cliplines
        # if ray.intersects_line(line):
        #     lines.append(line)
