# 🎵 Apple Music Album Link Generator

A Python-based utility that reads an Excel spreadsheet containing artist and album names, queries the Apple Music website, and retrieves **album links only** (no singles). The script outputs results to both an `.xlsx` and `.txt` file. It includes built-in random delays to avoid being blocked by the server.

---

##  Features

-  Extracts **only Apple Music album links** (ignores singles/EPs)
-  Supports `.xlsx` input with artist & album details and can read all sheets
-  Outputs:
  - `updated_music_links.xlsx` with album links
-  Adds random delay (5–10 seconds) between requests to avoid API rate limits
-  Automatically skips failed lookups
-  Apple Music India region support (can be customized)

---

##  Example Input

Your input `.xlsx` file should have the following structure:

| Artist         | Album                             |
|----------------|------------------------------------|
| Charli XCX     | BRAT                               |
| Mabe Fratti    | Sentir Que No Sabes                |
| Beyoncé        | COWBOY CARTER                      |

---

##  Setup & Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/apple-music-link-generator.git
   cd apple-music-link-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Place your input file**
   - Save your Excel file as `input_music_data.xlsx` in the project root or update the filename in the script.

---

##  Usage

```bash
python get_album_links.py
```

After the script finishes, you’ll get:
- `updated_music_links.xlsx` – with artist, album, and Apple Music link
- `apple_music_links.txt` – plain list of Apple Music album URLs

---

##  Output Example

### Excel (`updated_music_links.xlsx`)
| Artist         | Album              | Apple Music Link                                              |
|----------------|--------------------|----------------------------------------------------------------|
| Mabe Fratti    | Sentir Que No Sabes | https://music.apple.com/in/album/sentir-que-no-sabes/1740787009 |
| Charli XCX     | BRAT               | https://music.apple.com/in/album/brat/1723251871             |


---

## Configuration

To customize:
- Input filename: change the `input_file` variable in the script
- Delay between requests: adjust the `time.sleep(random.randint(5, 10))` line
- Region: modify the Apple Music domain from `/in/` to your desired country code

---

## ❗ Notes

- Ensure your Excel input is clean: no empty rows and proper spelling
- Script avoids singles, but accuracy depends on Apple Music’s search structure
- Not affiliated with Apple Inc. or Apple Music

---

##  Requirements

- Python 3.7+
- [pandas](https://pandas.pydata.org/)
- [requests](https://docs.python-requests.org/)
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/)

Install them via:
```bash
pip install -r requirements.txt
```

---

## 🧑‍💻 Author

**J221B**

> Feel free to fork, open issues, or contribute to improve the project!

---

## 📄 License

This project is open-source and available under the MIT License.
