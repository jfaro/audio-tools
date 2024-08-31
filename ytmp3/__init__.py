import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

YTMP3_URL = "https://ytmp3s.nu/ux5Z/"

YOUTUBE_RESULTS_URL = "https://www.youtube.com/results?search_query="

def get_driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--window-size=800,600")
    return webdriver.Chrome(options=opts)


def get_youtube_url(name: str, artists: list[str]) -> str:
    # Search for video on youtube.
    artist_str = ' '.join(artists)
    search = f"{name} {artist_str} official audio"
    query = urllib.parse.quote_plus(search)
    url = f"{YOUTUBE_RESULTS_URL}{query}"
    
    print(f"Loading youtube search results from '{url}'")
    driver = get_driver()
    driver.get(url)
    
    print("Waiting for results list")
    path_elements = [
        'ytd-item-section-renderer',
        'div[@id="contents"]',
        'ytd-video-renderer',
        'div',
        'ytd-thumbnail',
        'a'
    ]
    path = f'//{"/".join(path_elements)}'
    item = None
    while True:
        try:
            item = driver.find_element(By.XPATH, path)
            print("Found thumbnail", item)
            return item.get_attribute("href")
        except:
            print("Fail to find item section...")
        time.sleep(1)


def download_song(name: str, youtube_url: str):
    driver = get_driver()
    driver.get(YTMP3_URL)
    assert "YTMP3" in driver.title
    
    # Search for youtube video.
    el = driver.find_element(By.ID, "url")
    el.clear()
    el.send_keys(youtube_url)
    el.send_keys(Keys.RETURN)
    
    # Wait and then close.
    download, duration = (None, 0)
    while True:
        try:
            download = driver.find_element(By.XPATH, '//a[text()="Download"]')
            break
        except:
            pass
        print(f"Waiting for download ('{name}' {duration * 5} seconds)...")
        duration += 1
        time.sleep(5)
    
    download.click()
    
    print(f"Downloading '{name}'")
    time.sleep(10)
    print(f"Download complete for '{name}'")
    driver.close()