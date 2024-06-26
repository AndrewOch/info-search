import os
from collections import defaultdict

import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))


def load_index(folder_path):
    index = defaultdict(dict)
    for file_name in os.listdir(folder_path):
        doc_id = file_name.split('.')[0]
        with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as f:
            for line in f:
                token, idf, tf_idf = line.strip().split()
                index[token][doc_id] = (float(idf), float(tf_idf))
    return index


def query_to_vector(query, index):
    query_vector = defaultdict(float)
    for word in query.split():
        for doc_id, (idf, tf_idf) in index.get(word, {}).items():
            query_vector[doc_id] += idf
    return query_vector


def calculate_similarity(query_vector, index):
    similarity_scores = defaultdict(float)
    for token, docs in index.items():
        for doc_id, (idf, tf_idf) in docs.items():
            if doc_id in query_vector:
                similarity_scores[doc_id] += query_vector[doc_id] * tf_idf
    return similarity_scores


def vector_search(query):
    query_vector = query_to_vector(query, index)
    similarity_scores = calculate_similarity(query_vector, index)
    sorted_docs = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs


index = load_index('lemmas_tf_idf')
