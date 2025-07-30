import pandas as pd
import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def clean_query(artist, album):
    return quote_plus(f"{artist} {album}")

def extract_album_link(soup):
    results = soup.find_all('li', {'class': 'songs-list-row'})
    if results:
        return None  # Skip singles

    album_section = soup.find_all('a', {'class': 'we-lockup__title'})
    for link in album_section:
        href = link.get('href')
        if href and '/album/' in href:
            return "https://music.apple.com" + href
    return None

def search_album(artist, album):
    base_url = "https://music.apple.com/in/search"
    params = {"term": f"{artist} {album}"}
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        link = extract_album_link(soup)
        return link
    except Exception as e:
        print(f"[ERROR] Search failed for '{artist} - {album}': {e}")
        return None

def process_excel(input_file):
    df = pd.read_excel(input_file)
    df['Apple Music Link'] = None
    links_list = []

    for idx, row in df.iterrows():
        artist = str(row['Artist']).strip()
        album = str(row['Album']).strip()
        print(f"Searching: {artist} - {album}")

        link = search_album(artist, album)
        if link:
            df.at[idx, 'Apple Music Link'] = link
            links_list.append(link)
            print(f"✓ Found: {link}")
        else:
            print("✗ Not Found.")

        time.sleep(random.uniform(5, 10))  # Wait between 5 to 10 seconds

    output_excel = "apple_music_links_output.xlsx"
    output_txt = "apple_music_links.txt"
    
    df.to_excel(output_excel, index=False)
    print(f"\n✅ Excel saved to {output_excel}")

    with open(output_txt, "w") as f:
        for link in links_list:
            f.write(link + "\n")
    print(f"✅ TXT saved to {output_txt}")

if __name__ == "__main__":
    input_file = "your_input_file.xlsx"  # Replace with your Excel file
    process_excel(input_file)
