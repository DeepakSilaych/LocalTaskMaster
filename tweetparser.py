import re
import nltk
from nltk.corpus import stopwords
from transformers import pipeline
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
import tweepy
import datetime
from datetime import timedelta
from connections import tweetdata

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def tweetpipeline():
    BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAIfomwEAAAAAlBC3KnzchShxMhmQj8Ctg8J0jZw%3Dez8WeHlWy9AQ9rfw9apkFDD79Oe9nV9KWXNoq7T68kbTIIr93k'
    tweets = get_tweets(BEARER_TOKEN)
    time = datetime.datetime.now()
    for tweet in tweets:
        processed_tweet = process_tweet(tweet)
        if processed_tweet['locations']:
            for location, coords in processed_tweet['locations'].items():
                tweetdata({
                    'tweet': processed_tweet['text'],
                    'latitude': coords[0],
                    'longitude': coords[1],
                    'location': location,
                    'sentiment': processed_tweet['sentiment']['label'],
                    'timestamp': time,
                })
        else:
            tweetdata({
                'tweet': processed_tweet['text'],
                'latitude': 0,
                'longitude': 0,
                'location': '',
                'sentiment': processed_tweet['sentiment']['label'],
                'timestamp': time,
            })

def get_tweets(BEARER_TOKEN):
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    date = datetime.datetime.now() - timedelta(days=1, hours=5.51)
    start_time = date.strftime('%Y-%m-%dT00:00:00Z')
    today = datetime.datetime.now() - timedelta(hours=5.51)
    end_time = today.strftime('%Y-%m-%dT%H:%M:%SZ')

    queries = ['mumbairains -is:retweet', 'mumbairain -is:retweet', 'mumbaiflood -is:retweet']

    all_tweets = []
    for query in queries:
        tweets = client.search_recent_tweets(query=query, tweet_fields=['conversation_id','created_at','text'], start_time=start_time, end_time=end_time, max_results=30)
        if tweets.data:
            for tweet in tweets.data:
                all_tweets.append(tweet.text)

    return all_tweets

stations_western = [
    "Churchgate", "Marine Lines", "Grant Road", "Charni Road", "Mumbai Central", "Mahalaxmi", 
    "Lower Parel", "Elphinstone Road", "Dadar", "Matunga Road", "Mahim", "Bandra", "Khar Road",
    "Santacruz", "Vile Parle", "Andheri", "Jogeshwari", "Goregaon", "Malad", "Kandivali", 
    "Borivali", "Dahisar", "Mira Road", "Bhayandar", "Naigaon", "Vasai Road", "Nalasopara", "Virar"
]
stations_eastern = [
    "CST", "Masjid", "Sandhurst Road", "Byculla", "Chinchpokli", "Currey Road", "Parel", 
    "Dadar", "Matunga", "Sion", "Kurla", "Vidyavihar", "Ghatkopar", "Vikhroli", "Kanjurmarg", 
    "Bhandup", "Nahur", "Mulund", "Thane", "Kalwa", "Mumbra", "Diva", "Kopar", "Dombivli", "Thakurli", 
    "Kalyan", "Shahad", "Ambivli", "Titwala", "Khadavli", "Vasind", "Asangaon", "Atgaon", "Kasara"
]
stations_harbour = [
    "CST", "Masjid", "Sandhurst Road", "Dockyard Road", "Reay Road", "Cotton Green", "Sewri", "Wadala Road",
    "GTB Nagar", "Chunabhatti", "Kurla", "Tilak Nagar", "Chembur", "Govandi", "Mankhurd", "Vashi", 
    "Sanpada", "Juinagar", "Nerul", "Seawoods", "Belapur", "Kharghar", "Mansarovar", "Khandeshwar", "Panvel"
]
keyaddwords = [
    "Park", "Chowk", "Marg", "Bridge", "Tower", "Building", "Road", "Nagar", "Compound", "Cinema",
    "Talkies", "Link", "Market", "Street", "Colony", "Apartment", "School", "College", "Crossroad", 
    "Intersection", "Ground", "Drive", "Highway", "St", "Gully", "Rasta", "Station", "Udyan", "Signal", 
    "Mohalla", "Chawl", "Shop", "Bar", "Express", "Lake", "River", "Estate", "Rail", "Church", 
    "Masjid", "Temple", "Mandir", "Society", "Hotel", "Subway", "Flyover", "Underpass", "Pole", "Circle",
    "Gardens", "Lane", "Plaza", "Square", "Boulevard", "Avenue", "Court", "Terrace", "Heights", "Meadow", 
    "Terrace", "Garden", "Grove", "Meadow", "View", "Way", "Crescent", "Trail", "Place", "Parkway", 
    "Broadway", "Mall", "Esplanade", "Crescent", "Walk", "Driveway", "Turn", "Rise", "Path", "Close", 
    "Court", "Field", "Mount", "Court", "Glade", "Croft", "Mews", "Dell", "Valley"
]

all_keywords = stations_western + stations_eastern + stations_harbour + keyaddwords
pattern = re.compile(r"\b(?:{})\b".format("|".join(all_keywords)), re.IGNORECASE)

sentiment_pipeline = pipeline("sentiment-analysis")

def process_tweet(tweet):
    sentiment = sentiment_pipeline(tweet)[0]
    locations = extract_locations(tweet, pattern)
    if not locations:
        return {
            "text": tweet,
            "locations": None,
            "sentiment": sentiment
        }
    
    location_coords = {}
    for loc in locations:
        cleaned_location = ' '.join([word for word in loc.split() if word.lower() not in stop_words])
        coords = get_lat_long(cleaned_location)
        if coords:
            location_coords[loc] = coords

    return {
        "text": tweet,
        "locations": location_coords,
        "sentiment": sentiment
    }

def get_lat_long(location):
    geolocator = Nominatim(user_agent="twitter-location-extraction")
    try:
        location = geolocator.geocode(location)
        if location:
            # Check if the coordinates are within Mumbai's lat-long boundaries
            if 18.89 <= location.latitude <= 19.27 and 72.77 <= location.longitude <= 72.99:
                return location.latitude, location.longitude
    except GeopyError as e:
        print(f"Error getting coordinates for {location}: {e}")
    return None

def extract_locations(tweet, pattern):
    return pattern.findall(tweet)
