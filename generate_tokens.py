import os
from bs4 import BeautifulSoup
import pymorphy2
import nltk
import re

nltk.download('punkt')
nltk.download('stopwords')

folder_path = 'downloaded_pages'

morph = pymorphy2.MorphAnalyzer()

stop_words = set(nltk.corpus.stopwords.words('russian'))


def tokenize_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    tokens = nltk.word_tokenize(text)
    return tokens


def clean_tokens(tokens):
    cleaned_tokens = []
    pattern = re.compile(r'^[а-яА-ЯёЁ]{1,20}$')

    for token in tokens:
        if pattern.match(token) and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())

    return list(set(cleaned_tokens))


all_tokens = []
for file_name in os.listdir(folder_path):
    if file_name.endswith('.html'):
        with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as file:
            html_content = file.read()
            tokens = tokenize_html(html_content)
            cleaned_tokens = clean_tokens(tokens)
            all_tokens.extend(cleaned_tokens)

unique_tokens = list(set(all_tokens))

lemmas = {}
for token in unique_tokens:
    lemma = morph.parse(token)[0].normal_form
    if lemma in lemmas:
        lemmas[lemma].add(token)
    else:
        lemmas[lemma] = {token}

with open('tokens.txt', 'w', encoding='utf-8') as f:
    for token in unique_tokens:
        f.write(f"{token}\n")

with open('lemmas.txt', 'w', encoding='utf-8') as f:
    for lemma, tokens in lemmas.items():
        f.write(f"{' '.join([lemma] + list(tokens))}\n")
