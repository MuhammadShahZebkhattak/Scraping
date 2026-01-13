import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc

uc.Chrome.__del__ = lambda self: None  # prevent WinError 6

PROFILE_URL = "https://www.instagram.com/natgeo/"
MAX_SCROLLS = 10       # how many times to scroll
SCROLL_PAUSE = 2       # seconds pause per scroll

# ---------------- Launch browser ----------------
driver = uc.Chrome(
    user_data_dir=r"C:\Users\khatt\AppData\Local\Google\Chrome\User Data\InstaBotProfile",
    use_subprocess=True
)

driver.get("https://www.instagram.com")
input("➡ Login manually once and press ENTER if required...")

# ---------------- Visit profile ----------------
driver.get(PROFILE_URL)
time.sleep(5)

# ---------------- Scroll dynamically ----------------
last_height = driver.execute_script("return document.body.scrollHeight")
for scroll in range(MAX_SCROLLS):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:  # reached bottom
        break
    last_height = new_height

# ---------------- Wait for posts ----------------
try:
    WebDriverWait(driver, 30).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "article img")) > 0
    )
except TimeoutException:
    print("No posts loaded. Check login or profile visibility.")
    driver.quit()
    exit()

# ---------------- Extract posts ----------------
posts_elements = driver.find_elements(By.CSS_SELECTOR, "article a")
results = []
seen = set()

for el in posts_elements:
    try:
        post_url = el.get_attribute("href")
        if "/p/" not in post_url or post_url in seen:
            continue
        seen.add(post_url)

        # image and caption
        try:
            img = el.find_element(By.TAG_NAME, "img")
            img_url = img.get_attribute("src")
            caption = img.get_attribute("alt")
        except NoSuchElementException:
            img_url = None
            caption = None

        # likes and comments
        try:
            likes = el.find_element(By.XPATH, ".//..//div[contains(@aria-label,'likes')]").text
        except:
            likes = "N/A"

        try:
            comments = el.find_element(By.XPATH, ".//..//ul").text
        except:
            comments = "N/A"

        results.append({
            "url": post_url,
            "image": img_url,
            "caption": caption,
            "likes": likes,
            "comments": comments
        })

    except Exception as e:
        continue

# ---------------- Show results ----------------
print("\n--- Extracted Posts ---\n")
if not results:
    print("No posts found. Check login or profile privacy settings.")
else:
    for p in results:
        print("Post URL :", p["url"])
        print("Image    :", p["image"])
        print("Caption  :", p["caption"])
        print("Likes    :", p["likes"])
        print("Comments :", p["comments"])
        print("-" * 80)

driver.quit()
