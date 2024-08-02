from bs4 import BeautifulSoup
import requests
import time
# request from a website
print("write a skill you are not familiar with : \n")
unfamiliar_skill = input('>')
print(f"filtering out {unfamiliar_skill}")


def find_jobs():

    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=').text

    soup = BeautifulSoup(html_text, 'lxml')

    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    for index, job in enumerate(jobs):
        posted = job.find('span', class_='sim-posted').span.text.replace(' ', '')
        if 'few' in posted:
            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ','')
            skill = job.find('span', class_='srp-skills').text.replace(' ','')
            more_info = job.header.h2.a['href']

            if unfamiliar_skill not in skill:
                with open(f'posts/{index}.txt', 'w') as f:
                    f.write(f"more info : {more_info}\n")
                    f.write(f"company name : {company_name.strip()}\n")
                    f.write(f"skill : {skill.strip()}\n")
                print(f"file saved {index} \n")

if __name__ =='__main__':
    while True:
        find_jobs()
        time_wait = 10 * 60  # seconds * seconds
        print(f"waiting : {time_wait}")
        time.sleep(time_wait)

