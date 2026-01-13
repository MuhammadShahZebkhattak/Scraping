import requests
from bs4 import BeautifulSoup
import csv
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

page = 1

with open("all_quotes.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Quote", "Author"])

    while True:
        url = f"https://quotes.toscrape.com/page/{page}/"
        print("Scraping:", url)

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "lxml")

        quotes = soup.find_all("span", class_="text")
        authors = soup.find_all("small", class_="author")

        if len(quotes) == 0:
            break

        for q, a in zip(quotes, authors):
            writer.writerow([q.text.strip(), a.text.strip()])

        page += 1
        time.sleep(2)
print("All pages scraped successfully!")

#selenium

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import csv
# import time

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver.get("https://quotes.toscrape.com/js")

# with open("selenium_quotes.csv", "w", encoding= "utf-8", newline ="") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Quote", "Author"])
    
#     while True:
#         quotes_divs = driver.find_elements("class name","quote")

#         if len(quotes_divs)==0:
#             break

#         for div in quotes_divs:
#             text= div.find_element("class name", "text").text
#             author= div.find_element("class name", "author").text
#             writer.writerow([text, author])
#             print(f"{text} - {author}")

#         try: 
#             next_button =driver.find_element("css selector", "li.next > a")
#             next_button.click()
#             time.sleep(2)
#         except: 
#             break

# driver.quit()
# print("scraping completed! Check")        



