from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv

service = Service("path to chrome driver")
driver = webdriver.Chrome(service=service)

homepage_url = "https://www.geeksforgeeks.org/"

all_data = []

max_pages = 5

try:
    driver.get(homepage_url)

    search_bar = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "HomePageSearchContainer_homePageSearchContainer_container_input__1LS0r"))
    )
    search_bar.send_keys("interview questions")
    search_bar.send_keys(Keys.RETURN)

    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "SearchModalArticleCard_searchModalArticleCard_content_heading__hB4a_"))
    )

    article_links = []
    page_count = 0

    while page_count < max_pages:
        container = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "HomePageSearchModal_homePageSearchModalContainer_modal_container_content__drrYe"))
        )
        links = [a.get_attribute("href") for a in container.find_elements(By.TAG_NAME, "a")]
        article_links.extend(links)
        page_count += 1

    filtered_links = [link for link in article_links if "interview-questions" in link.lower()]

    for link in filtered_links:
        print(f"Fetching: {link}")
        driver.get(link)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "h3"))
            )
        except:
            continue

        questions = driver.find_elements(By.TAG_NAME, "h3")
        for i, question in enumerate(questions):
            question_text = question.text.strip()
            answer = ""

            sibling = question.find_element(By.XPATH, "following-sibling::*")
            while sibling:
                if sibling.tag_name == "h3":
                    break

                if sibling.tag_name in ["ul", "p"]:
                    answer += sibling.text.strip() + "\n"

                try:
                    sibling = sibling.find_element(By.XPATH, "following-sibling::*")
                except:
                    break

            all_data.append({"Question": question_text, "Answer": answer.strip()})

finally:
    driver.quit()

with open("interview_questions.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Question", "Answer"])
    writer.writeheader()
    for data in all_data:
        writer.writerow(data)