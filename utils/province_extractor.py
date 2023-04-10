from pythainlp.tag import tag_provinces
from pythainlp.tokenize import word_tokenize

def extract_province(text):
    """
    Extracts the province from a given address string.
    """
    text_list = word_tokenize(text, engine='newmm')
    provinced_tag = tag_provinces(text_list)
    for word, tag in provinced_tag:
        if 'LOCATION' in tag:
            return word
    return None

def get_province(df):
    province_list = []
    for index,row in df.iterrows():
        text = row['news'] 
        result = extract_province(text)
        province_list.append(result)
    return province_list
   
      