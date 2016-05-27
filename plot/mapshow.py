import sys
import json
import map_pb2
from google.protobuf import text_format
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def draw_line(line_segment):
    px = []
    py = []
    for p in line_segment.point:
        px.append(float(p.x))
        py.append(float(p.y))
    ax.plot(px,py)
    ax.plot([line_segment.point[-1].x],[line_segment.point[-1].y],'ro')

def draw_arc(arc):
    xy = (arc.center.x, arc.center.y)
    pac = mpatches.Arc(
            xy, 
            arc.radius*2, 
            arc.radius*2, 
            angle=0, 
            theta1=arc.start_angle/3.1415926535*180, 
            theta2=arc.end_angle/3.1415926535*180
            )

    ax.add_patch(pac)
    
f, ax = plt.subplots()

fn = sys.argv[1]
f = open(fn, 'r')
mapdata = f.read()

drivemap = map_pb2.Map()
text_format.Merge(str(mapdata), drivemap)

for lane in  drivemap.lane:
    #print lane.type
    #print lane.central_curve
    #break 
    #print [f.name for f in lane.central_curve.DESCRIPTOR.fields]
    for curve in lane.central_curve.segment:
        if  curve.HasField('line_segment'):
            draw_line(curve.line_segment)
        if  curve.HasField('arc'):
            draw_arc(curve.arc)


plt.show()
