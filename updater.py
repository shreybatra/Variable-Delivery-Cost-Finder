from pymongo import MongoClient
import numpy as np
from time import time
import math
import distance

client = MongoClient()
db = client.minor
boys = db.boys
reqdb = db.reqdb

workshop = {'x':0,'y':0}
old_time = time()

radius = 0.1

def getAllReqs():
	result = reqdb.find()

	ans = []

	for r in result:
		ans.append(r['x'])
		ans.append(r['y'])

	return np.array(ans).reshape(int(len(ans)/2),2)

def getAllBoys():
	result = boys.find()

	ans = []

	for r in result:
		ans.append(r['curr_x'])
		ans.append(r['curr_y'])

	return np.array(ans).reshape(int(len(ans)/2),2)

def updateBoys():
	result = boys.find()

	print(result.count())

	new_x = 0
	new_y = 0

	for p in result:
		if p['curr_x'] == 0.0 and p['curr_y']==0.0:
			for un_req in p['unhandled_reqs']:
				p['handled_reqs'].append(un_req)
			## changeeeeee

			boys.update_one({'id':p['id']},{'$set':{'handled_reqs':p['handled_reqs'],'unhandled_reqs':[]}})
			

			if len(p['handled_reqs'])>0:
				new_x,new_y = getNewXY((p['curr_x'],p['curr_y']),(p['handled_reqs'][0]['x'],p['handled_reqs'][0]['y']))
			else:
				new_x,new_y = getNewXY((p['curr_x'],p['curr_y']),(workshop['x'],workshop['y']))

		elif len(p['handled_reqs'])>0 and p['curr_x'] == p['handled_reqs'][0]['x'] and p['curr_y']==p['handled_reqs'][0]['y']:

			p['handled_reqs'].pop(0)
			boys.update_one({'id':p['id']},{'$set':{'handled_reqs':p['handled_reqs']}})

			if len(p['handled_reqs'])>0:

				new_x,new_y = getNewXY((p['curr_x'],p['curr_y']),(p['handled_reqs'][0]['x'],p['handled_reqs'][0]['y']))
			else:

				new_x,new_y = getNewXY((p['curr_x'],p['curr_y']),(workshop['x'],workshop['y']))
			
			

		else:
			if len(p['handled_reqs'])>0:
				if distance.getDistance({'x':p['curr_x'],'y':p['curr_y']},{'x':p['handled_reqs'][0]['x'],'y':p['handled_reqs'][0]['y']}) <= radius:
					new_x = p['handled_reqs'][0]['x']
					new_y = p['handled_reqs'][0]['y']
				else:
					new_x,new_y = getNewXY((p['curr_x'],p['curr_y']),(p['handled_reqs'][0]['x'],p['handled_reqs'][0]['y']))
			else:
				if distance.getDistance({'x':p['curr_x'],'y':p['curr_y']},{'x':workshop['x'],'y':workshop['y']}) <= radius:
					new_x = workshop['x']
					new_y = workshop['y']
				else:
					new_x,new_y = getNewXY((p['curr_x'],p['curr_y']),(workshop['x'],workshop['y']))
			## changeeee
		boys.update_one({'id':p['id']},{'$set':{'curr_x':new_x,'curr_y':new_y}})




def getNewXY(pos1,pos2):
	x1 = float(pos1[0])
	y1 = float(pos1[1])
	x2 = float(pos2[0])
	y2 = float(pos2[1])

	if x2-x1 == 0:
		if y1>=y2:
			return (x1,y1-0.1)
		else:
			return (x1,y1+0.1)
	else:

		m = (y2-y1)/(x2-x1)
		c = y1 - m*x1


		A = (m*m + 1)
		B = 2*(m*c - m*y1 - x1)
		C = y1*y1 - radius*radius + x1*x1 - 2*c*y1 + c*c

		temp = math.sqrt(B*B - 4*A*C)
		nx1 = (-B + temp)/(2*A)
		nx2 = (-B - temp)/(2*A)

		ny1 = m*nx1 + c
		ny2 = m*nx2 + c

		dist1 = distance.getDistance({'x':x2,'y':y2},{'x':nx1,'y':ny1})
		dist2 = distance.getDistance({'x':x2,'y':y2},{'x':nx2,'y':ny2})

		if dist1<=dist2:
			return (nx1,ny1)
		else:
			return (nx2,ny2)



def main():
	
	global old_time
	old_time = time()
	while True:
		new_time = time()
		
		if new_time >= old_time + 0.1:
			#print('Hello')
			old_time = new_time
			updateBoys()
			print('Done')



