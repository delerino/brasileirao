def get_club_info(club_object):
    infos = [club_object.id, 
            club_object.screen_name,
            club_object.name,
            club_object.created_at,
            club_object.location,
            club_object.followers_count,
            club_object.friends_count,
            club_object.favourites_count,
            club_object.statuses_count,
            datetime.now()]
    return infos

def get_tweet_info(tweet_object):
    infos = [tweet_object.user.id,
            tweet_object.id, 
            tweet_object.created_at,
            get_status_text_len(tweet_object),
            get_status_count_by_entity(tweet_object, "hashtags"),
            get_status_count_by_entity(tweet_object, "symbols"),
            get_status_count_by_entity(tweet_object, "urls"),
            get_status_count_by_entity(tweet_object, "user_mentions"),
            get_status_count_by_extended_entity(tweet_object, "media"),
            tweet_object.retweet_count,
            tweet_object.favorite_count,
            datetime.now()]
    return infos

def get_status_count_by_entity(status,entity_name):
    try:
        lenght = len(status.entities[entity_name])
    except:
        lenght = 0
    return lenght

def get_status_count_by_extended_entity(status,entity_name):
    try:
        lenght = len(status.extended_entities[entity_name])
    except:
        lenght = 0
    return lenght

def get_status_text_len(tweet):
    return len(tweet.full_text)

def is_tweet_date_in_month(tweet_object, month):
    tweet_month = tweet_object.created_at.month
    return tweet_month == month

def read_all_clubs_from_file():
    for club_screen_name in open('clubs.txt', 'r'):
        yield club_screen_name
        
def get_club_object_by_all_screen_names():
    for club_screen_name in read_all_clubs_from_file():
        club_object = api.get_user(screen_name=club_screen_name)
        yield club_object
        
def get_all_tweets_by_club_and_month(club_screen_name, month):
    oldest_id = 0
    pegou_todos = False
    while (not pegou_todos):
        
        if(oldest_id == 0):
            tweets = api.user_timeline(screen_name=club_screen_name, 
                                   count=200,
                                   include_rts = False,
                                   # Necessary to keep full_text 
                                   # otherwise only the first 140 words are extracted
                                   tweet_mode = 'extended'
                                   )
        else:
            tweets = api.user_timeline(screen_name=club_screen_name, 
                               count=200,
                               include_rts = False,
                               max_id = oldest_id - 1,
                               # Necessary to keep full_text 
                               # otherwise only the first 140 words are extracted
                               tweet_mode = 'extended'
                               )
        #last_datem = datetime.strptime(tweets[-1].created_at, "%Y-%m-%d %H:%M:%S")
        if len(tweets) == 0:
            pegou_todos = True
        elif(is_tweet_date_in_month(tweets[-1], month)):
            pegou_todos = False
        else:
            pegou_todos = True
        yield tweets
        oldest_id = tweets[-1].id