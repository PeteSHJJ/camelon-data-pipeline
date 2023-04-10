import requests 
from utils.text_cleaner import clean 
from datetime import datetime
from utils.convert_datetime import split_thai_datetime_dailynews

class DailyNewsCrawler:
    BASE_URL = 'https://www.dailynews.co.th/wp-json/wp/v2/news'
    NEWS_LIMIT = 20
    Page = 1
    def __init__(self, limit=NEWS_LIMIT,page=Page):
        self.headers = {
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        self.limit = limit
        self.page = page


    def fetch_and_get_result(self):
        
        # print(response)
        try:
            if response['code'] == 'rest_post_invalid_page_number':
                return []
        except:
            pass
        news_result = []
        # print(f'[DailyNews] Loading DailyNews News Content Page: {page}')
        
        while True:
            params = {"per_page": 100, "news_group": 48, "page": int(self.page)}
            response = requests.get(self.BASE_URL, params=params, headers=self.headers).json()
            try:
                if response['code'] == 'rest_post_invalid_page_number':
                    print(f'[Dailynews] Finished Loading {len(news_result)} contents because there is no page {self.page}')
                    return news_result
            except:
                pass
            print(f'[DailyNews] Loading DailyNews News Content for Page: {self.page}')
            try:
                for data in response:
                    title = clean(data['title']['rendered'])
                    excerpt = clean(data['acf']['custom_excerpt'])
                    content = clean(data['content']['rendered'])
                    news_id = data['id']
                    source = 'Dailynews'
                    date = data['date'].replace("T", " ")
                    news = clean(title + " " + excerpt + " " + content)
                    date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                    year = date_obj.strftime('%Y')
                    if (int(year) <= 2021):
                        print(f'[Dailynews] Finished Loading {len(news_result)} contents because year is 2021')
                        return news_result
                    if (len(news_result) != self.limit):
                        print(f'[DailyNews] Loading DailyNews News Content {len(news_result) + 1} : {title}')
                        news_result.append([news_id, source, news, date])
                    else:
                        print(f'[Dailynews] Finished Loading {len(news_result)} contents')
                        return news_result
                self.page = int(self.page) + 1
                
            except Exception as e:
                print(e)
                return None
            
        
    # def fetch_and_get_result(self):
    #     news_result = []
    #     page = 1 
    #     while True:
    #         print(f'[DailyNews] Loading DailyNews News Content for Page: {page}')
    #         news_data = self.fetch_news_content(page)
    #         if not news_data:
    #             print(f'[Dailynews] Finished Loading {len(news_result)} contents because there is no more news')
    #             break
    #         news_result += news_data
    #         if len(news_result)  == self.limit:
    #             print(f'[Dailynews] Finished Loading {len(news_result)} contents')
    #             break
            
    #         page += 1 