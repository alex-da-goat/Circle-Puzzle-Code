import math as m

def INCREMENT_CIRCULAR(_num, _limit):
    if _num == _limit-1:
        return 0
    else:
        return _num+1
    
def CARTESIAN_COORDS_TO_POLAR(_coords, _center_coords):
    coords = (_coords[0] - _center_coords[0], _coords[1] - _center_coords[1]) #centered coords
    r = m.sqrt( coords[0]**2 + coords[1]**2 ) #radius
    if coords[0] != 0:
        theta = m.atan(-coords[1] / coords[0])
        if coords[0] < 0:
            theta += m.pi
        theta = (theta + 2*m.pi) % (2*m.pi)
    else:
        if coords[1] < 0:
            theta = 3/2*m.pi
        else:
            theta = m.pi/2
    return (r, theta)

def POLAR_COORDS_TO_CARTESIAN(_coords, _center_coords):
    x = _coords[0] * m.cos(_coords[1])
    y = _coords[0] * m.cos(_coords[1])
    return (_center_coords[0] + x, _center_coords[1] + y)

def NORMALIZE_ANGLE(_angle):
    return (_angle + 2*m.pi) % (2*m.pi)