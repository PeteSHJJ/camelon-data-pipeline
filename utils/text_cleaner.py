import re 

def clean(text):
    # Removing html tag
    text_1 = re.sub('(<([^>]+)>)', '', text) 
    text_2 = re.sub(r'&[a-zA-Z]+;', '',text_1)
    # Removing multiple spaces with single space
    text_3 = re.sub(r'\s+', ' ',text_2, flags=re.I)
    words = text_2.split()
    new_text = ' '.join(words)
    return new_text
