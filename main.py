import tweepy as tw
import sqlite3
from datetime import datetime

from myservice import *


class database():
    def __init__(self):
        self.con = sqlite3.connect("brasileirao.db")
        self.cur = self.con.cursor()
        self.create_clubs_table_()
        self.create_tweets_table_()

    def create_clubs_table_(self):
        sql = "CREATE TABLE IF NOT EXISTS clubs(internal_id INTEGER PRIMARY KEY AUTOINCREMENT, twitter_id, screen_name, name, created_at, location, followers_count, friends_count, favourites_count, statuses_count, last_verification)"
        self.cur.execute(sql)
        self.con.commit()

    def create_tweets_table_(self):
        sql = "CREATE TABLE IF NOT EXISTS tweets(internal_id INTEGER PRIMARY KEY AUTOINCREMENT, internal_club_id, tweet_id, created_at, text_lenght, hashtags_count, symbols_count, urls_count, user_mentions_count, media_count, retweet_count, favorite_count, verification_date)"
        self.cur.execute(sql)
        self.con.commit()

    def insert_or_update_club(self, club_info):
        club_internal_id = self.get_club_internal_id_by_twitter_id(club_info[0])
        if(club_internal_id is None):
            sql = """
            INSERT INTO clubs (twitter_id, screen_name, name, created_at, location, followers_count, friends_count, favourites_count, statuses_count, last_verification) 
            VALUES(?,?,?,?,?,?,?,?,?,?)"""
            self.cur.execute(sql, club_info)
            self.con.commit()
        else:
            sql = """
            UPDATE clubs 
            SET twitter_id = ?, 
            screen_name = ?, 
            name = ?, 
            created_at = ?, 
            location = ?, 
            followers_count = ?, 
            friends_count = ?, 
            favourites_count = ?, 
            statuses_count = ?, 
            last_verification = ?
            WHERE twitter_id = ?"""
            club_info.append(club_internal_id)
            self.cur.execute(sql, club_info)
            self.con.commit()

    def insert_or_update_tweet(self, tweet_info):
        tweet_info[0] = self.get_club_internal_id_by_twitter_id(tweet_info[0]) #screen_name to club_internal_id
        if(tweet_info[0] is not None):
            tweet_internal_id = self.get_tweet_internal_id_by_tweet_id(tweet_info[1])
            if(tweet_internal_id is None):
                sql = """
                INSERT INTO tweets (internal_club_id, tweet_id, created_at, text_lenght, hashtags_count, symbols_count, urls_count, user_mentions_count, media_count, retweet_count, favorite_count, verification_date) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"""
                self.cur.execute(sql, tweet_info)
                self.con.commit()
            else:
                sql = """
                UPDATE tweets
                SET internal_club_id = ?, 
                tweet_id = ?, 
                created_at = ?, 
                text_lenght = ?, 
                hashtags_count = ?,
                symbols_count = ?,
                urls_count = ?,
                user_mentions_count = ?, 
                media_count = ?, 
                retweet_count = ?, 
                favorite_count = ?, 
                verification_date = ?
                WHERE tweet_id = ?"""
                tweet_info.append(tweet_internal_id)
                self.cur.execute(sql, tweet_info)
                self.con.commit()
        else:
            raise Exception("Club internal id doesn't exists on database. Create one first.")
    
    def insert_all_clubs_in_db(self):
        for club_object in get_club_object_by_all_screen_names():
            print(f"Inserting club [{club_object.name}] in database...")
            self.insert_or_update_club(get_club_info(club_object))
            
    def insert_all_tweets_in_db_by_club_and_month(self, club_screen_name, month):
        for twohundred in get_all_tweets_by_club_and_month(club_screen_name = club_screen_name, month = month):
            for tweet_object in twohundred:
                if(is_tweet_date_in_month(tweet_object,month)):
                    self.insert_or_update_tweet(get_tweet_info(tweet_object))
                    
    def insert_all_tweets_by_month(self, month):
        all_clubs = self.get_all_clubs()
        for club in all_clubs:
            print(f"Starting tweets insertion of club = {club[0]}...")
            self.insert_all_tweets_in_db_by_club_and_month(club[0], month)
            
    def get_all_clubs(self):
        res = self.cur.execute("SELECT screen_name FROM clubs")
        retorno = res.fetchall()
        return retorno
                
    def get_club_internal_id_by_twitter_id(self, twitter_id):
        res = self.cur.execute("SELECT internal_id FROM clubs WHERE twitter_id = :id", {"id": twitter_id})
        retorno = res.fetchone()
        if(retorno is None):
            return retorno
        else:
            return retorno[0]

    def get_tweet_internal_id_by_tweet_id(self, tweet_id):
        res = self.cur.execute("SELECT internal_id FROM tweets WHERE tweet_id = :id", {"id": tweet_id})
        retorno = res.fetchone()
        if(retorno is None):
            return retorno
        else:
            return retorno[0]
    def create_weekday_column(self):
        sql = '''ALTER TABLE tweets
                ADD weekday_created_at'''
        self.cur.execute(sql)
        self.con.commit()
    
    def insert_weekday_values(self, internal_id, created_at):
        weekday = datetime.strptime(created_at[:-6], "%Y-%m-%d %H:%M:%S").weekday()
        sql = '''UPDATE tweets
                set weekday_created_at = ?
                WHERE internal_id = ?'''
        self.cur.execute(sql, (weekday, internal_id))
        self.con.commit()

if __name__ == "__main__":
    with open('tokens.txt', 'r') as tfile:
        consumer_key = tfile.readline().strip('\n')
        consumer_secret = tfile.readline().strip('\n')
        access_token = tfile.readline().strip('\n')
        access_token_secret = tfile.readline().strip('\n')
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tw.API(auth)

    MONTH = 8

    database = database() 
    database.insert_all_clubs_in_db()
    abrir_banco.insert_all_tweets_by_month(MONTH)