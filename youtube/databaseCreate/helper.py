from youtube.models import History, Search_click
from collections import Counter

def viewcount(video_id,user):
    user_history = History.objects.filter(user=user)
    for video in user_history:
        if video.video_id == video_id:
            return video.view_count
    return 0

def is_user_query_exists(query, user):
    searches = Search_click.objects.filter(user=user, search_query=query)
    if searches:
        return True
    else:
        return False

def is_query_exits(query):
    searches = Search_click.objects.filter(search_query = query)
    if searches:
        return True
    return False

def user_query_rank_scorings(query, user, objs):
    searches = Search_click.objects.filter(user=user, search_query = query)
    video_ids = [video.video_clicked for video in searches]
    video_count = Counter(video_ids)
    # obj_ids = [obj['videoInfo']['id'] for obj in objs]
    score = []
    for obj in objs:
        if obj['videoInfo']['id'] in video_ids:
            score.append([[obj],[video_count[obj['videoInfo']['id']]]])
        else:
            score.append([[obj],[0]])
    return score
    
def query_rank_scorings(query, objs):
    searches = Search_click.objects.filter(search_query = query)
    video_ids = [video.video_clicked for video in searches]
    video_count = Counter(video_ids)
    # obj_ids = [obj['videoInfo']['id'] for obj in objs]
    score = []
    for obj in objs:
        if obj['videoInfo']['id'] in video_ids:
            score.append([[obj],[video_count[obj['videoInfo']['id']]]])
        else:
            score.append([[obj],[0]])
    return score
    
    

    
        
# def query_rank(video_id, user):
