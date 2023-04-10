from crawlers.thairath_crawler import ThairathCrawler
from crawlers.dailynews_crawler import DailyNewsCrawler
from crime_classification.crime_tagger import XLMRClassifier
from database.database_connector import connect_to_db, insert_data_into_table
from utils.province_extractor import get_province
import pandas as pd 

# Set up database connection
engine = connect_to_db()

# Crawl news articles
thairath_crawler = ThairathCrawler()
dailynews_crawler = DailyNewsCrawler()
news_result_thairath = thairath_crawler.fetch_and_get_result()
news_result_dailynews = dailynews_crawler.fetch_and_get_result()
merge_all_news = news_result_thairath + news_result_dailynews

# Classify crime tag from news articles
XLMR_path = "./XLMR_Model.h5"
XLMR_chosen_premodel = 'xlm-roberta-large'
classifier = XLMRClassifier(XLMR_path, XLMR_chosen_premodel)
probs = classifier.predict([news[2] for news in merge_all_news])

# Merge news articles and prediction results
df_news = pd.DataFrame(merge_all_news, columns=['news_id','source','news','date'])
df_predict = pd.DataFrame(probs, columns=['gambling', 'murder', 'sexual_abuse', 'theft/burglary', 'drug', 'battery/assault', 'accident', 'non-crime'])
merged_df = pd.concat([df_news, df_predict], axis=1)

# Get Province with PythaiNLP
province_list = get_province(merged_df)
merged_df['province'] = province_list


# Insert data into the database
insert_data_into_table(engine, merged_df)

# Print success message
print("Data pipeline executed successfully!")

# Export to csv 
merged_df.to_csv('test.csv', index=False)
