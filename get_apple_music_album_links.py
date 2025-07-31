import pandas as pd
import requests
import urllib.parse
import time
import os
import random

def clean_query(text):
    return text.replace("’", "'").replace("–", "-").replace("&", "and").strip()

def slugify_name(name):
    safe = name.lower().replace(" ", "-")
    return urllib.parse.quote(safe, safe='-')

def get_apple_music_album_link(artist, album, country_codes=["IN", "US"], retries=2):
    base_url = "https://itunes.apple.com/search"
    query = f"{artist} {album}"
    query = clean_query(query)

    for country in country_codes:
        params = {
            "term": query,
            "entity": "album",
            "country": country,
            "limit": 5,  # fetch more results to filter better
        }
        for attempt in range(retries):
            try:
                response = requests.get(base_url, params=params, timeout=5)
                if response.status_code != 200 or not response.text.strip():
                    time.sleep(1)
                    continue

                data = response.json()
                results = data.get("results", [])
                for result in results:
                    if result.get("collectionType") != "Album":
                        continue  # Skip singles and other types

                    track_count = result.get("trackCount", 0)
                    if track_count <= 3:
                        continue  # Likely a single or EP

                    coll_id = result.get("collectionId")
                    coll_name = result.get("collectionName", "")
                    slug = slugify_name(coll_name)
                    return f"https://music.apple.com/{country.lower()}/album/{slug}/{coll_id}"
                break
            except Exception:
                time.sleep(1)
    return "Not Found"

def process_excel(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    sheets = pd.read_excel(file_path, sheet_name=None)

    for sheet_name, df in sheets.items():
        print(f"\n🔍 Processing sheet: {sheet_name}")
        if not {'Artist', 'Album'}.issubset(df.columns):
            print("❌ Sheet skipped — must contain 'Artist' and 'Album' columns.")
            continue

        links = []
        for idx, row in df.iterrows():
            artist = str(row['Artist'])
            album = str(row['Album'])
            link = get_apple_music_album_link(artist, album)
            links.append(link)
            print(f"[{idx+1}/{len(df)}] {artist} — {album} → {link}")

            sleep_time = random.uniform(3, 7)
            print(f"⏳ Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)

        df['Apple Music Link'] = links
        sheets[sheet_name] = df

    output_file = os.path.splitext(file_path)[0] + "_with_links.xlsx"
    with pd.ExcelWriter(output_file) as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"\n✅ Done. File saved as: {output_file}")

if __name__ == "__main__":
    path = input("Enter path to Excel file (.xlsx): ").strip()
    process_excel(path)
