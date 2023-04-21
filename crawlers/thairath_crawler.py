import requests 
import time 
from datetime import datetime
import json

from utils.text_cleaner import clean 
from utils.convert_datetime import split_thai_datetime_thairath

class ThairathCrawler:
    BASE_URL = 'https://www.thairath.co.th'
    NEWS_LIMIT = 2500
    
    def __init__(self, limit=NEWS_LIMIT):
        self.limit = limit

    def fetch_news_data(self, timestamp, section='/news/crime'):
        """Fetches news data from Thairath API"""
        response = requests.get(f'{self.BASE_URL}/loadmore', params={"section": section, "ts": timestamp, "limit": 500}).json()
        min_timestamp = response['minTs']
        news_items = response['items']
        return min_timestamp, news_items
    
    def fetch_news_content(self, news_id):
        try:
            news_data = requests.get(f'{self.BASE_URL}/api-content/{news_id}').json()['items']
            news_id = f"THR_{news_id}"
            source = "Thairath"
            news = clean(news_data['title'] + " " + news_data['abstract'] + " " + news_data['content'])
            date = split_thai_datetime_thairath(news_data['publishTimeTh'])
            return news_id, source, news, date
        except: 
            return None 
    def fetch_and_get_result(self):
        news_result = []
        timestamp = int(time.time() * 1000)

        while len(news_result) < self.limit:
            print("[Thairath] Loading News Before", datetime.now())
            min_timestamp, news_items = self.fetch_news_data(timestamp)

            for item in news_items:
                print(f'[Thairath] Loading Thairath News Content {len(news_result) + 1} : {item["title"]}')
                id = item['id']
                news_content = self.fetch_news_content(id)
                if news_content and "2021" in str(news_content[3]):
                    print(f'[Thairath] Finished Loading {len(news_result)} contents because year is 2021')
                    return news_result
                news_result.append(news_content)       
                if len(news_result) == self.limit:
                    return news_result
            timestamp = min_timestamp
        print(f'[Thairath] Finished Loading {len(news_result)} contents')
        return news_result