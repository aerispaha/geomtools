class Line(object):

    def __init__(self, m, b, x_min = None, x_max=None, y_min=None, y_max=None):
        self.m = m
        self.b = b
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def intersects_line(self, otherline):
        """
        test if a line intersects another. Works for continuous lines, rays, and
        line segments.
        """
        print '{} vs {}'.format(self, otherline)
        #check if parellel
        if (self.m == otherline.m):
            #print 'parellel lines'
            return False

        #check if both lines are contiuous
        limits = [self.x_min, self.x_max, otherline.x_min, otherline.x_max]
        if all(val is None for val in limits):
            #continuous lines (no limits), not parallel, so they must intersect
            #print 'all continuous'
            return True

        #calculate point of intersection of continuous lines, y = mx + b
        #if one of the slopes is None, use the x calculated above
        if self.m is not None and otherline.m is not None:
            x = (self.b - otherline.b) / (otherline.m - self.m)
            y = self.m * x + self.b

        elif self.m is None:
            x = self.x_min #(vertical line), set x intercept point
            y = otherline.m * x + otherline.b

        elif otherline.m is None:
            x = otherline.x_min #(vertical line), set x intercept point
            y = self.m * x + self.b

        #Check if the intersection point is in range of each line (ray or segment)
        if (x >= max(filter(None, [self.x_min, x])) and
            x <= min(filter(None, [self.x_max, x])) and
            x >= max(filter(None, [otherline.x_min, x])) and
            x <= min(filter(None, [otherline.x_max, x])) and

            y >= max(filter(None, [self.y_min, y])) and
            y <= min(filter(None, [self.y_max, y])) and
            y >= max(filter(None, [otherline.y_min, y])) and
            y <= min(filter(None, [otherline.y_max, y]))
            ):
            #print '{} intersects --> {}'.format(self, otherline)
            return True
        #
        #
        # #confirm if point within bounds of line segments
        # if (
        #     (x >= self.x_min and x <= self.x_max) and
        #     (x >= otherline.x_min and x <= otherline.x_max)
        #     ):
        #     print (x, y)
        #     return True
        else:
            #print 'intersects outside limits of line segs, {}'.format((x, y))
            return False

    def __str__(self):

        if self.m is None:
            return 'x = {} (vertical line)'.format(self.x_min)

        else:
            return 'y = {}x + {}, ({} <= x < {})'.format(round(self.m, 3),
                                                     round(self.b, 3),
                                                     self.x_min,
                                                     self.x_max)

class LineSegment(Line):

    def __init__(self, xypair):

        x1, y1, x2, y2 = xypair[0] + xypair[1]
        self.xypair = xypair

        #try to calc slope if line is valid
        if (x2 - x1) != 0:
            self.m = (y2 - y1) / (x2 - x1)
            self.b = y1 - self.m * x1
        else:
            self.m = None #undefined
            self.b = None #undefined

        self.x_min = min(x1, x2)
        self.x_max = max(x1, x2)
        self.y_min = min(y1, y2)
        self.y_max = max(y1, y2)


    # def __str__(self):
    #
    #     return 'y = {}x + {}, ({} <= x < {})'.format(round(self.m, 3),
    #                                                  round(self.b, 3),
    #                                                  self.x_min,
    #                                                  self.x_max)
