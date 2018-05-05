import pymongo
from pymongo import MongoClient
import distance
import math
import Compute_Cluster as cc
import areaFinder as af


client = MongoClient()
db = client.minor
boys = db.boys
reqdb = db.reqdb

#boys.remove()
#reqdb.remove()


variable_cost = 10
per_km = 1
per_person = 10


workshop = {'x':0.0,'y':0.0}


class FindPerson():

	def __init__(self):
		pass

	def FindBestPerson(self, req):

		persons = boys.find()

		if persons.count()==0:
			return None

		best_dist = math.inf
		best_pos = 0
		best_person = None

		for person in persons:
			total_dist_old = person['total_distance']

			old_x = 0
			old_y = 0

			if len(person['handled_reqs'])!=0:
				old_x = person['handled_reqs'][-1]['x']
			else:
				old_x = person['curr_x']

			if len(person['handled_reqs'])!=0:
				old_y = person['handled_reqs'][-1]['y']
			else:
				old_y = person['curr_y']

			
			if len(person['handled_reqs'])>0:
				distance_to_workshop = distance.getDistance(workshop,{'x':person['handled_reqs'][-1]['x'],'y':person['handled_reqs'][-1]['y']})
			else:
				distance_to_workshop = distance.getDistance(workshop,{'x':person['curr_x'],'y':person['curr_y']})

			pos = 0
			
			old_x = 0
			old_y = 0

			min_distance = math.inf

			if len(person['unhandled_reqs'])==0:
				#min_distance = 0
				pass
			else:
				distance_to_workshop = 0



			for i,r in enumerate(person['unhandled_reqs']):
				if min_distance >= (distance.getDistance(req,r) + distance.getDistance(req,{'x':old_x,'y':old_y})):
					min_distance = (distance.getDistance(req,r) + distance.getDistance(req,{'x':old_x,'y':old_y}))
					pos = i

				old_x = r['x']
				old_y = r['y']

			
			if min_distance >= (distance.getDistance(req,{'x':old_x,'y':old_y})):
				min_distance = (distance.getDistance(req,{'x':old_x,'y':old_y}))
				if old_x==0.0 and old_y==0.0:
					pos = 0
				else:
					pos = len(person['unhandled_reqs']) - 1
			



			if (min_distance+total_dist_old+distance_to_workshop)<best_dist:
				best_dist = (min_distance+total_dist_old+distance_to_workshop)
				best_pos = pos
				best_person = person['id']

		

		return {'best_dist':best_dist,'best_pos':best_pos,'best_person':best_person}




	def NewPerson(self, req):
		dist = distance.getDistance(req,workshop)
		return dist


	def GetPerson(self,req):

		best_person = self.FindBestPerson(req)

		#print(af.ReturnConstituency(req['x'],req['y']))
		req_in_consti = af.ReturnConstituency(req['x'],req['y'])[2]

		global total_count_reqs

		frac = req_in_consti/total_count_reqs

		print('Fraction of reqs - ', frac)

		global count

		if best_person==None:
			count = count + 1
			min_dist = self.NewPerson(req)
			print('Total Cost - ',min_dist*per_km + per_person + variable_cost*(1-frac))
			person = {}
			person['id'] = count
			person['curr_x'] = float(workshop['x'])
			person['curr_y'] = float(workshop['y'])
			person['unhandled_reqs'] = [req]
			person['handled_reqs'] = []
			person['total_distance'] = 0

			boys.insert_one(person)

			return person
		
		new_person = self.NewPerson(req)

		#print('Best Dist - ',best_person['best_dist'])
		if best_person['best_dist']*per_km < new_person*per_km + per_person:

			l = list(boys.find({'id':best_person['best_person']}))
			#td = l['total_distance'] + 
			l = l[0]

			l['unhandled_reqs'].insert(best_person['best_pos'],req)

			boys.update_one({'id':best_person['best_person']},{'$set':{'unhandled_reqs':l['unhandled_reqs']}})
			boys.update_one({'id':best_person['best_person']},{'$set':{'unhandled_reqs':l['unhandled_reqs']}})
			
			print('Total Cost - ',best_person['best_dist']*per_km + variable_cost*(1-frac))
			return best_person
		else:
			count = count + 1
			min_dist = self.NewPerson(req)
			person = {}
			person['id'] = count
			person['curr_x'] = float(workshop['x'])
			person['curr_y'] = float(workshop['y'])
			person['unhandled_reqs'] = [req]
			person['handled_reqs'] = []
			person['total_distance'] = 0
			print('Total Cost - ',min_dist*per_km + per_person + variable_cost*(1-frac))
			boys.insert_one(person)
			return person
			




f = FindPerson()

def algo():
	x = 1
	y = 1
	while x!=0 or y!=0:
		print('\n\nEnter X Y coordinates (0 0 to end) - ')
		str = input().split(' ')
		x = float(str[0])
		y = float(str[1])
		#print(x,y)
		if x==0 and y==0:
			return
		
		global total_count_reqs

		total_count_reqs += 1

		cc.adjust_clusters(x,y)
		reqdb.insert({'x':x,'y':y})
		print(f.GetPerson({'x':x,'y':y}))



if __name__=='__main__':
	from Compute_Cluster import Tree
	global total_count_reqs
	total_count_reqs = reqdb.find().count()
	global count
	count = boys.find().count()
	algo()

#print(list(reqdb.find()))

'''
print(f.GetPerson({'x':4,'y':4}))
print()
print(f.GetPerson({'x':3,'y':4}))
print()
print(f.GetPerson({'x':5,'y':4}))
print()
print(f.GetPerson({'x':-7,'y':7}))
print()
print(f.GetPerson({'x':-3,'y':4}))
print()
print(f.GetPerson({'x':-7,'y':-7}))
print()
#print(list(boys.find()))
print(f.GetPerson({'x':-6,'y':-4}))
print()
print(f.GetPerson({'x':2,'y':-4}))


'''