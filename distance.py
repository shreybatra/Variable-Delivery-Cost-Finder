import math

def getDistance(obj1, obj2):
	return math.sqrt((obj1['x']-obj2['x'])*(obj1['x']-obj2['x']) + (obj1['y']-obj2['y'])*(obj1['y']-obj2['y']))
