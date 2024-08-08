
# successfull for cnbc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Initialize the Firefox WebDriver
driver = webdriver.Firefox()

# List to store the collected data
data = []

try:
    wait_time = 10
    wait = 3
    # Open the website
    driver.get("https://www.cnbc.com/search/?query=news&qsearchterm=news")
    time.sleep(wait_time)

    # Scroll down and collect data
    last_height = driver.execute_script("return document.body.scrollHeight")

    count = 0

    while count < 11:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait)  # Wait for new content to load

        # Check new height and break if no new content
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        count += 1

    # Retrieve and print the content
    content = driver.find_element(By.CLASS_NAME, 'SearchResults-searchResultsContainer')
    headlines = content.find_elements(By.CLASS_NAME, "resultlink")

    links = set()  # Use a set to avoid duplicates

    for head in headlines:
        link = head.get_attribute('href')
        if link and link.startswith("https://www.cnbc.com/") and not any(
                keyword in link for keyword in ["video", "audio", "podcast"]):
            links.add(link)

    unique_links = list(links)
    print(len(unique_links))

    for link in unique_links:
        driver.get(link)  # Navigate to each link
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))  # Wait for the h1 tag to be present

        try:
            title = driver.find_element(By.TAG_NAME, "h1").text

            try:
                date_publish = driver.find_element(By.TAG_NAME, "time").text
            except:
                date_publish = "Date not found"

            try:
                writer = driver.find_element(By.CLASS_NAME, "Author-authorName").text
            except:
                writer = "Author not found"

            try:
                content = driver.find_element(By.CLASS_NAME, "group").text
            except:
                content = "Content not found"

            try:
                category = driver.find_element(By.CLASS_NAME, "ArticleHeader-eyebrow").text
            except:
                category = "Category not found"

            # Print the data (optional)
            print(f"title: {title}")
            print(f"date_publish: {date_publish}")
            print(f"writer: {writer}")
            print(f"content: {content}")
            print(f"category: {category}")

            # Store the data in a dictionary and append to the list
            data.append({
                "title": title,
                "date_publish": date_publish,
                "writer": writer,
                "content": content,
                "category": category,
                "link": link
            })

        except Exception as e:
            print(f"Error fetching details from {link}: {e}")

finally:
    # Close the browser
    driver.quit()

    # Write the data to an Excel file
    df = pd.DataFrame(data)
    df.to_excel("cnbc_news_data.xlsx", index=False)

    print("Data has been written to news_data.xlsx")
