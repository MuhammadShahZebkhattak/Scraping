import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

# Prevent Windows handle crash
uc.Chrome.__del__ = lambda self: None

if __name__ == '__main__':
    # Enter Instagram profile URL here
    PROFILE_URL = input("Enter Instagram profile URL: ").strip()
    
    if not PROFILE_URL:
        PROFILE_URL = "https://www.instagram.com/natgeo/"
        print(f"Using default: {PROFILE_URL}")
    else:
        # Fix URL if needed
        if not PROFILE_URL.startswith(("http://", "https://")):
            if PROFILE_URL.startswith("instagram.com") or PROFILE_URL.startswith("www.instagram.com"):
                PROFILE_URL = "https://" + PROFILE_URL
            else:
                # Assume it's just a username
                PROFILE_URL = f"https://www.instagram.com/{PROFILE_URL.replace('@', '').replace('/', '')}/"
    
    # Launch browser
    print("Launching browser...")
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = uc.Chrome(options=options, use_subprocess=True)
    print("✅ Browser launched")
    
    # Visit profile
    print(f"Visiting {PROFILE_URL}...")
    driver.get(PROFILE_URL)
    time.sleep(8)  # Wait longer for page to load
    
    # Check if we're on login page
    current_url = driver.current_url
    if "login" in current_url.lower() or "accounts" in current_url.lower():
        print("⚠️  Instagram is asking to log in. The profile may be private or require authentication.")
        print(f"Current URL: {current_url}")
    
    # Scroll to load more posts
    print("Scrolling to load posts...")
    for i in range(15):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        print(f"  Scroll {i+1}/15...", end="\r")
    print()
    
    # Try multiple methods to find images
    print("Extracting images...")
    image_urls = []
    seen = set()
    
    # Method 1: Find post links and get images from them
    try:
        post_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/'], a[href*='/reel/']")
        print(f"Found {len(post_links)} post links")
        for link in post_links[:50]:  # Limit to first 50
            try:
                img = link.find_element(By.TAG_NAME, "img")
                src = img.get_attribute("src")
                if src and src not in seen:
                    image_urls.append(src)
                    seen.add(src)
            except:
                continue
    except:
        pass
    
    # Method 2: Find all images and filter
    try:
        all_images = driver.find_elements(By.TAG_NAME, "img")
        print(f"Found {len(all_images)} total images on page")
        for img in all_images:
            try:
                src = img.get_attribute("src")
                if src and src not in seen:
                    # Look for Instagram CDN images
                    if "scontent" in src or "cdninstagram" in src or "fbcdn" in src:
                        if any(x in src for x in [".jpg", ".jpeg", ".png", ".webp"]):
                            image_urls.append(src)
                            seen.add(src)
            except:
                continue
    except:
        pass
    
    # Method 3: Try article tags
    try:
        articles = driver.find_elements(By.CSS_SELECTOR, "article img")
        for img in articles:
            try:
                src = img.get_attribute("src")
                if src and src not in seen and ("scontent" in src or "cdninstagram" in src):
                    image_urls.append(src)
                    seen.add(src)
            except:
                continue
    except:
        pass
    
    # Display results
    print(f"\n✅ Found {len(image_urls)} images\n")
    if image_urls:
        for i, url in enumerate(image_urls, 1):
            print(f"{i}. {url}")
    else:
        print("⚠️  No images found. Instagram may require login or the profile may be private.")
        print("💡 Try logging into Instagram manually in the browser window that opened.")
    
    driver.quit()
    print("\n✅ Done!")
