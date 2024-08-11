from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

data = []


def scrap_bbc():
    try:
        wait = 3

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
                category = ""

            # Collect more links from the new page
            more_headlines = driver.find_elements(By.TAG_NAME, 'a')
            for more_head in more_headlines:
                more_link = more_head.get_attribute('href')
                if more_link and more_link.startswith("https://www.bbc.com/") and not any(
                        keyword in more_link for keyword in ["video", "audio", "podcast", "tv", "live"]):
                    additional_links[more_link] = category

        # Processing the additional links
        pause = 0
        for reference, category in additional_links.items():

            try:
                driver.get(reference)  # Navigate to each link
                WebDriverWait(driver, 4).until(EC.presence_of_element_located(
                    (By.TAG_NAME, "h1")))  # Wait for the h1 tag to be present

                pause = 1  # Pause duration between actions

                # Try to fetch the title
                try:
                    title = driver.find_element(By.TAG_NAME, "h1").text
                    time.sleep(pause)
                except:
                    title = ""

                # Try to fetch the published date
                try:
                    date_publish = driver.find_element(By.TAG_NAME, "time").text
                    if "hours ago" in date_publish.lower():
                        # Replace "few hours ago" with today's date
                        date_publish = date.today()
                    time.sleep(pause)
                except:
                    date_publish = date.today()

                # Try to fetch the author
                try:
                    writer = driver.find_element(By.CSS_SELECTOR, ".sc-8b3e1b0d-7.iDUqNj").text
                    time.sleep(pause)
                except:
                    writer = "BBC"

                # Try to fetch the content
                try:
                    content = driver.find_element(By.CSS_SELECTOR,
                                                  "div.sc-18fde0d6-0:nth-child(4)").text  # Collect all paragraphs' text
                    time.sleep(pause)
                except:
                    content = ""

                # Store the data in a dictionary and append to the list
                data.append({
                    "title": title,
                    "date_publish": date_publish,
                    "writer": writer,
                    "content": content,
                    "category": category
                })

            except Exception as e:
                print(f"Error fetching details from {reference}: {e}")
                continue

    finally:
        print("bbc scraping done")
        driver.quit()


def scrap_cnbc():
    try:
        wait_time = 20
        wait = 3
        # Open the website
        driver.get("https://www.cnbc.com/search/?query=news&qsearchterm=news")
        time.sleep(wait_time)

        # Scroll down and collect data
        last_height = driver.execute_script("return document.body.scrollHeight")

        count = 0

        while count < 20:
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
            WebDriverWait(driver, wait_time-3).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1")))  # Wait for the h1 tag to be present

            try:
                title = driver.find_element(By.TAG_NAME, "h1").text

                try:
                    date_publish = driver.find_element(By.TAG_NAME, "time").text
                except:
                    date_publish = date.today()

                try:
                    writer = driver.find_element(By.CLASS_NAME, "Author-authorName").text
                except:
                    writer = "CNBC"

                try:
                    content = driver.find_element(By.CLASS_NAME, "group").text
                except:
                    content = ""

                try:
                    category = driver.find_element(By.CLASS_NAME, "ArticleHeader-eyebrow").text
                except:
                    category = ""

                # Store the data in a dictionary and append to the list
                data.append({
                    "title": title,
                    "date_publish": date_publish,
                    "writer": writer,
                    "content": content,
                    "category": category
                })

            except Exception as e:
                print(f"Error fetching details from {link}: {e}")

    finally:
        print("cnbc scrapping done")
        driver.quit()


def scrap_cnn():
    try:

        driver.get("https://edition.cnn.com/")

        wait = 5
        corrected_links = set()
        additional_links = set()

        unique_links = set()  # Use a set to avoid duplicates

        # Retrieve and print the content

        bar = driver.find_element(By.TAG_NAME, 'nav')
        headlines = bar.find_elements(By.TAG_NAME, 'a')

        for head in headlines:
            link = head.get_attribute('href')
            if link:
                unique_links.add(link)

        for link in unique_links:
            if link.startswith("https://edition.cnn.com"):
                corrected_links.add(link)

        # extraction of links so that websites other than cnn can be removed
        # Navigate to each link and collect more links

        for link in corrected_links:
            try:
                driver.get(link)  # Navigate to each link
                time.sleep(4)  # Ensure the page loads completely

                # Collect more links from the new page
                headlines = driver.find_elements(By.TAG_NAME, 'a')

                for more_headlines in headlines:
                    more_link = more_headlines.get_attribute('href')
                    if more_link and more_link.startswith("https://edition.cnn.com") and not any(
                            keyword in more_link for keyword in ["video", "audio", "podcast"]):
                        additional_links.add(more_link)
            except Exception as e:
                print(f"Error accessing link {link}: {e}")
                continue

            # taking out content from each link

            for reference in additional_links:
                try:
                    driver.get(reference)  # Navigate to each link
                    WebDriverWait(driver, 6).until(
                        EC.presence_of_element_located((By.ID, "maincontent"))
                    )
                except Exception as e:
                    print(f"Error accessing link {link}: {e}")
                    continue

                pause = 0  # Pause duration between actions

                # Try to fetch the title
                try:
                    title = driver.find_element(By.ID, "maincontent").text
                    time.sleep(pause)
                except:
                    title = "Title"

                # Try to fetch the published date
                try:
                    date_publish = driver.find_element(By.CSS_SELECTOR, ".timestamp").text
                    time.sleep(pause)
                except:
                    date_publish = date.today()

                # Try to fetch the author
                try:
                    writer = driver.find_element(By.CLASS_NAME, "byline__names").text
                    time.sleep(pause)
                except:
                    writer = "CNN"

                # Try to fetch the content
                try:
                    content = driver.find_element(By.CLASS_NAME,
                                                  "article__content").text  # Collect all paragraphs' text
                    time.sleep(pause)
                except:
                    content = ""

                # Try to fetch the category
                try:
                    category = driver.find_element(By.CSS_SELECTOR,
                                                   "div.brand-logo:nth-child(3) > a:nth-child(2) > span:nth-child(1)").text
                    time.sleep(pause)
                except:
                    category = ""

                # Print the data

                # Store the data in a dictionary and append to the list
                data.append({
                    "title": title,
                    "date_publish": date_publish,
                    "writer": writer,
                    "content": content,
                    "category": category
                })

    finally:
        print("cnn scrapping done")
        driver.quit()



# after final part

if __name__ =='__main__':

    driver = webdriver.Firefox()

    try:

        # scrap_bbc()
        scrap_cnbc()
        scrap_cnn()

    except Exception as e:
        print(f"Error fetching details")

    finally:
        df = pd.DataFrame(data)
        df.to_excel("allnews_more_scrapping.xlsx", index=False)
        print("filing done")

