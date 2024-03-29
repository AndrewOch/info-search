import os
from bs4 import BeautifulSoup

folder_path = 'downloaded_pages'

output_file = 'titles.txt'


def extract_titles(folder_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for file_name in os.listdir(folder_path):

            if file_name.endswith('.html'):
                file_name_without_extension = file_name[:-5]
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as html_file:
                    soup = BeautifulSoup(html_file, 'html.parser')
                    title_tag = soup.find('title')

                    title_text = title_tag.get_text(strip=True) if title_tag else 'No Title Found'

                    out_file.write(f"{file_name_without_extension}. {title_text}\n")


extract_titles(folder_path, output_file)
