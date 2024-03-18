from hexagons import Hexagons

rh = Hexagons('./sagittal/Convex', 6)

rh.format_key_points()
rh.create_mesh('./sagittal')

#pixels to microns 
#wall: .02mm of the diameter of the hexagon 
# mm size: .35mm diameter