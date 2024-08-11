from datetime import date

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Initialize the web driver
driver = webdriver.Firefox()

data = []

try:
    wait = 6

    # Open the website
    driver.get("https://www.bbc.com")

    unique_links = set()  # Use a set to avoid duplicates

    # Collect initial links
    time.sleep(wait)
    bar = driver.find_element(By.TAG_NAME, 'nav')
    headlines = bar.find_elements(By.TAG_NAME, 'a')

    for head in headlines:
        link = head.get_attribute('href')
        if link and "live" not in link and "video" not in link:
            unique_links.add(link)

    print(unique_links)
    print(len(unique_links))

    additional_links = {}  # Dictionary to store links and their categories

    for link in unique_links:
        driver.get(link)  # Navigate to each link
        time.sleep(wait)  # Ensure the page loads completely

        # Extract the category from the h1 tag
        try:
            category = driver.find_element(By.TAG_NAME, 'h1').text
        except:
            category = "Category not found"

        # Collect more links from the new page
        more_headlines = driver.find_elements(By.TAG_NAME, 'a')
        for more_head in more_headlines:
            more_link = more_head.get_attribute('href')
            if more_link and more_link.startswith("https://www.bbc.com/") and not any(
                    keyword in more_link for keyword in ["video", "audio", "podcast", "tv", "live"]):
                additional_links[more_link] = category
    print(additional_links)
    dt = pd.DataFrame(additional_links)
    dt.to_excel("additional_links.xlsx", index=False)
    # Processing the additional links

    for reference, category in additional_links.items():

        try:
            driver.get(reference)  # Navigate to each link
            WebDriverWait(driver, wait).until(EC.presence_of_element_located(
                (By.TAG_NAME, "h1")))  # Wait for the h1 tag to be present

            pause = 1  # Pause duration between actions

            # Try to fetch the title
            try:
                title = driver.find_element(By.TAG_NAME, "h1").text
                time.sleep(pause)
            except:
                title = "Title not found"

            # Try to fetch the published date
            try:
                date_publish = driver.find_element(By.TAG_NAME, "time").text
                if "hours ago" in date_publish.lower():
                    # Replace "few hours ago" with today's date
                    date_publish = date.today()
                time.sleep(pause)
            except:
                date_publish = "Date not found"

            # Try to fetch the author
            try:
                writer = driver.find_element(By.CSS_SELECTOR, ".sc-8b3e1b0d-7.iDUqNj").text
                time.sleep(pause)
            except:
                writer = "Author not found"

            # Try to fetch the content
            try:
                content = driver.find_element(By.CSS_SELECTOR, "div.sc-18fde0d6-0:nth-child(4)").text  # Collect all paragraphs' text
                time.sleep(pause)
            except:
                content = "Content not found"

            # Print the data
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
                "link": reference
            })

        except Exception as e:
            print(f"Error fetching details from {reference}: {e}")
            continue


finally:
    # Close the browser
    driver.quit()

    # Write the data to an Excel file
    df = pd.DataFrame(data)
    df.to_excel("news_data.xlsx", index=False)

    print("Data has been written to news_data.xlsx")
