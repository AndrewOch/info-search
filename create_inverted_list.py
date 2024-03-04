import os
from bs4 import BeautifulSoup

with open('tokens.txt', 'r', encoding='utf-8') as f:
    tokens = [line.strip() for line in f.readlines()]

token_pages = {token: [] for token in tokens}

for filename in os.listdir('downloaded_pages'):
    if filename.endswith('.html'):

        page_number = filename.split('.')[0]
        filepath = os.path.join('downloaded_pages', filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            text = soup.get_text().lower()

            for token in tokens:
                if token.lower() in text:
                    token_pages[token].append(page_number)

with open('inverted_index.txt', 'w', encoding='utf-8') as f:
    for token, pages in token_pages.items():
        f.write(f"{token} {' '.join(pages)}\n")

print("Inverted index file created successfully.")
