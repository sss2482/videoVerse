from __future__ import print_function
import pymongo
import pprint
from operator import itemgetter
from collections import Counter
conn = pymongo.MongoClient('mongodb://localhost')
import sys
sys.path.insert(0, '/home/sunil/Documents/assignment/gui/youtube/databaseCreate')
import handler
import helper
import didyoumean

# conn.admin.authenticate('admin','vodka')
db = conn.yt
coll = db.yt_videos
sorted_output=[]
def search(context,user):
	#print context
	global sorted_output
	del sorted_output[:]
	query = context['message']
	search_input=map(str,context['message'].split())
	print(search_input)
	# print search_input
	final_output=[]
	for word in search_input:
		print(word)
		result=coll.find({'$or':[{'videoInfo.snippet.tags':{'$regex':word,'$options':'i'}},
			{'videoInfo.snippet.title':{'$regex':word,'$options':'i'}},
			{'videoInfo.snippet.channelTitle':{'$regex':word,'$options':'i'}},
			{'videoInfo.snippet.localized.description':{'$regex':word,'$options':'i'}},
			{'videoInfo.snippet.localized.title':{'$regex':word,'$options':'i'}},
			{'videoInfo.snippet.description':{'$regex':word,'$options':'i'}},
			{'videoInfo.snippet.categoryId':{'$regex':word,'$options':'i'}}
			]})
		# result = coll.find({})
		
		for obj in result:
			print(obj)
			if obj not in final_output:
				final_output.append(obj)
	# print final_output
	count=0

	if helper.is_user_query_exists(query, user):
		rank_scores = helper.user_query_rank_scorings(query, user, final_output)
	elif helper.is_query_exits(query):
		rank_scores = helper.query_rank_scorings(query, final_output)
	else:
		rank_scores= [[[obj],[0]] for obj in final_output]
	
	# print(final_output)
	similarity = {}
	viewcounts = {}
	for obj in final_output:
		viewCount=0
		if user.is_authenticated:
			video_id=obj['videoInfo']['id']
			viewCount=helper.viewcount(video_id,user)
		else:
			viewCount=obj['videoInfo']['statistics']['viewCount']
			
		# viewCount=obj['videoInfo']['id']
		unparsed_string=''
		count_occurence=0
		if 'tags' in obj['videoInfo']['snippet']:
			for tag in obj['videoInfo']['snippet']['tags']:
				unparsed_string+=tag.lower()
				unparsed_string+=" "
		if 'title' in obj['videoInfo']['snippet']:
			unparsed_string+=obj['videoInfo']['snippet']['title'].lower().strip('\n')
			unparsed_string+=" "
		if 'channelTitle' in obj['videoInfo']['snippet']:
			unparsed_string+=obj['videoInfo']['snippet']['channelTitle'].lower().strip('\n')
			unparsed_string+=" "
		if 'description' in obj['videoInfo']['snippet']:
			unparsed_string+=obj['videoInfo']['snippet']['description'].lower().strip('\n')
			unparsed_string+=" "
		if 'categoryId' in obj['videoInfo']['snippet']:
			unparsed_string+=obj['videoInfo']['snippet']['categoryId'].lower().strip('\n')
			unparsed_string+=" "
		frequency=Counter(unparsed_string.split())
		
		
		for word in search_input:
			count_occurence+=frequency[word.lower()]
		
		# search_query = 
		# similarity[obj] = (count_occurence/len(unparsed_string.split()))*20
		# viewcounts[obj] = viewCount
		for rank_obj in rank_scores:
			if rank_obj[0][0]==obj:
				score = viewCount+rank_obj[1][0]*20+(count_occurence/len(unparsed_string.split()))*20
				sorted_output.append([[obj],[score]])
				break

	
		# sorted_output.append([[obj],[count_occurence]])
	
	# video_ids = [obj['']]
	
	# sorted_output = [k for k, v in sorted(score.items(), key=lambda item: item[1])]
	sorted_output = sorted(sorted_output,key=itemgetter(1))
	sorted_output.reverse()
	return sorted_output

json_data=[]
def searchIndividual(videoId):
	global json_data
	del json_data[:]
	
	result=coll.find({'videoInfo.id':videoId})
	return result

def increase_view_count(video_id):
	output=coll.find({'videoInfo.id':video_id})
	for result in output:
		initial_count=result['videoInfo']['statistics']['viewCount']+1
		filter_criteria = {'videoInfo.id': video_id}
		update_operation = {'$set': {'videoInfo.statistics.viewCount': initial_count}}

		# result = collection.update_one(filter_criteria, update_operation)
		coll.update_one({'videoInfo.id':video_id},{'$set':{'videoInfo.statistics.viewCount':initial_count}})
		# print initial_count
		return initial_count
