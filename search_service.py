import string

import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))


def preprocess_query(query):
    query = query.translate(str.maketrans('', '', string.punctuation))
    query = ' '.join([word for word in query.split() if word.lower() not in stop_words])
    return query


def load_titles(titles_file_path):
    titles = {}
    with open(titles_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            doc_id, title = line.strip().split('. ', 1)
            titles[doc_id] = title
    return titles


def load_urls(index_file_path):
    urls = {}
    with open(index_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            doc_id, url = line.strip().split('. ', 1)
            urls[doc_id] = url
    return urls


titles = load_titles('titles.txt')
urls = load_urls('index.txt')
