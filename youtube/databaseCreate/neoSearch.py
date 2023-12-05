from py2neo import Graph,Node, Relationship, cypher
# from py2neo import neo4j
# from neo4j.util import watch
# from neo4j.v1 import GraphDatabase, basic_auth
#import os
# import json
# import pprint , time, re
#search_input=raw_input()
# graph = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "vodka"))
# session=graph.session()
graph = Graph("bolt://localhost:7687/Project/data/", auth=("neo4j","neo4jbysss7"))
#global neo_output
neo_output=[]
def search_on_click(videoId):
	global neo_output
	del neo_output[:]
	id=videoId
	
	run_parameter="match(n:NewVideo)-[r]->(p:NewVideo) where n.id ='"+id+"' return p order by r.weight limit 20"
	#print run_parameter
	output=graph.run(run_parameter).data()
	print(type(output))
	# neo_output=output
	return output
	# print type(output)
	# for obj in output:
	# 	print (obj)
#search_on_click(123)
def related_videos(videoIds):
	global neo_output
	del neo_output[:]
	ids=videoIds
	if len(ids)==0:
		list_str = '[]'
	else:
		list_str = '['
		for id in ids:
			list_str=list_str+"'"+str(id)+"'"+','
		list_str=list_str[:-1]+']'	
	
	run_parameter="match(n:NewVideo)-[r]->(p:NewVideo) where n.id in "+list_str+" return p order by r.weight limit 100"
	#print run_parameter
	output=graph.run(run_parameter).data()
	print(type(output))
	# neo_output=output
	return output

current_video_info=[]
def search_current_detail(videoId):
	pass
	global current_video_info
	del current_video_info[:]
	run_parameter="match(n:NewVideo) where n.id ='"+videoId+"' return n"
	#print run_parameter
	current_video_info=graph.run(run_parameter).data()
	return current_video_info
#search_current_detail(search_input)