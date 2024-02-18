import requests
import os


def download_page(url, folder_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = url.split('/')[-1] + ".html"
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"Failed to download page {url}. Status code: {response.status_code}")
            return False
    except Exception as e:
        return False


def create_index_file(pages, folder_path):
    index_filepath = os.path.join(folder_path, 'index.txt')
    with open(index_filepath, 'w', encoding='utf-8') as f:
        for i, page in enumerate(pages):
            f.write(f"{i + 1}. {page}\n")


def get_links_from_file(filename):
    links = []
    with open(filename, 'r') as file:
        for line in file:
            links.append(line.strip())

    return links


urls = get_links_from_file('crawled_links.txt')

output_folder = "downloaded_pages"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

downloaded_pages = []
for url in urls:
    if download_page(url, output_folder):
        downloaded_pages.append(url)

create_index_file(downloaded_pages, output_folder)

print("Downloaded pages and index file created successfully.")
