"""
This module defines the `main()` coroutine for the Apify Actor, executed from the `__main__.py` file.

Feel free to modify this file to suit your specific needs.

To build Apify Actors, utilize the Apify SDK toolkit, read more at the official documentation:
https://docs.apify.com/sdk/python
"""

from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *

from apify import Actor
from time import sleep
from .quickstart import *


# To run this Actor locally, you need to have the Selenium Chromedriver installed.
# https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
# When running on the Apify platform, it is already included in the Actor's Docker image.


async def main() -> None:
    """
    The main coroutine is being executed using `asyncio.run()`, so do not attempt to make a normal function
    out of it, it will not work. Asynchronous execution is required for communication with Apify platform,
    and it also enhances performance in the field of web scraping significantly.
    """
    async with Actor:
        # Read the Actor input
        actor_input = await Actor.get_input() or {}
        start_urls = actor_input.get('start_urls', [{'url': 'https://apify.com'}])
        max_depth = actor_input.get('max_depth', 1)

        if not start_urls:
            Actor.log.info('No start URLs specified in actor input, exiting...')
            await Actor.exit()

        # Enqueue the starting URLs in the default request queue
        default_queue = await Actor.open_request_queue()
        for start_url in start_urls:
            url = start_url.get('url')
            Actor.log.info(f'Enqueuing {url} ...')
            await default_queue.add_request({'url': url, 'userData': {'depth': 0}})

        # Launch a new Selenium Chrome WebDriver
        Actor.log.info('Launching Chrome WebDriver...')
        chrome_options = ChromeOptions()
        if Actor.config.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        while(True):
            try:
                driver = webdriver.Chrome(options=chrome_options)
                parcel_num_book = "503"
                parcel_num_map = "51"
                parcel_num_item = "079"
                parcel_num_split = "A"

                driver.get('https://treasurer.maricopa.gov/Parcel/Summary.aspx')
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id=\"txtParcelNumBook\"]")))
                parcel_num_book_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumBook\"]")
                parcel_num_book_input.send_keys(parcel_num_book)
                parcel_num_map_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumMap\"]")
                parcel_num_map_input.send_keys(parcel_num_map)
                parcel_num_item_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumItem\"]")
                parcel_num_item_input.send_keys(parcel_num_item)
                parcel_num_split_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumSplit\"]")
                parcel_num_split_input.send_keys(parcel_num_split)

                search_button = driver.find_element(By.CSS_SELECTOR, "div[id=\"btnGo\"]")
                search_button.click()
                sleep(3)
                await quickstart_main()
                apn_list = await getAPNList()
                
                with open('index.txt', 'r') as file:
                    content = file.read()
                last_index = int(content)

                index = last_index
                while(len(apn_list) > index):
                    split_string = apn_list[index].split('-')
                    parcel_num_book = split_string[0]
                    parcel_num_map = split_string[1]
                    parcel_num_item = split_string[2]
                    try:
                        parcel_num_split = split_string[3]
                    except:
                        parcel_num_split = ""

                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id=\"txtParcelNumBook\"]")))
                    parcel_num_book_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumBook\"]")
                    parcel_num_book_input.send_keys(parcel_num_book)
                    parcel_num_map_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumMap\"]")
                    parcel_num_map_input.send_keys(parcel_num_map)
                    parcel_num_item_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumItem\"]")
                    parcel_num_item_input.send_keys(parcel_num_item)
                    parcel_num_split_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumSplit\"]")
                    parcel_num_split_input.send_keys(parcel_num_split)

                    search_button = driver.find_element(By.CSS_SELECTOR, "input[id=\"btnGo\"]")
                    search_button.click()
                    sleep(3)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id=\"cphMainContent_cphRightColumn_divViewAdditionalYears\"]")))
                    view_addtional_tax_years_button = driver.find_element(By.CSS_SELECTOR, "div[id=\"cphMainContent_cphRightColumn_divViewAdditionalYears\"]").find_element(By.TAG_NAME, "a")
                    view_addtional_tax_years_button.click()
                    sleep(3)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title=\"Click for a Tax Stub printout\"]")))
                    # tax_elements = driver.find_elements(By.CSS_SELECTOR, "a[title=\"Click for a Tax Stub printout\"]")
                    total_tax_due = driver.find_element(By.CSS_SELECTOR, "span[class=\"text-bold text-black \"]").text
                    tax_due_2023 = "0"
                    tax_due_2022 = "0"
                    tax_due_2021 = "0"
                    
                    tax_rows = driver.find_elements(By.CSS_SELECTOR, "tr[class=\"gridviewRow\"]")
                    for tax_row in tax_rows:
                        try:
                            if "2023" in tax_row.find_element(By.CSS_SELECTOR, "a[title=\"Click to view Tax Details\"]").text:
                                try:
                                    tax_due_2023 = tax_row.find_element(By.CSS_SELECTOR, "a[title=\"Click for a Tax Stub printout\"]").text
                                except:
                                    tax_due_2023 = tax_row.find_element(By.CSS_SELECTOR, "a[class=\"text-red\"]").text
                            if "2022" in tax_row.find_element(By.CSS_SELECTOR, "a[title=\"Click to view Tax Details\"]").text:
                                try:
                                    tax_due_2022 = tax_row.find_element(By.CSS_SELECTOR, "a[title=\"Click for a Tax Stub printout\"]").text
                                except:
                                    tax_due_2022 = tax_row.find_element(By.CSS_SELECTOR, "a[class=\"text-red\"]").text
                            if "2021" in tax_row.find_element(By.CSS_SELECTOR, "a[title=\"Click to view Tax Details\"]").text:
                                try:
                                    tax_due_2021 = tax_row.find_element(By.CSS_SELECTOR, "a[title=\"Click for a Tax Stub printout\"]").text
                                except:
                                    tax_due_2021 = tax_row.find_element(By.CSS_SELECTOR, "a[class=\"text-red\"]").text
                        except:
                            pass

                    data = []
                    data.append(tax_due_2023)
                    data.append(tax_due_2022)
                    data.append(tax_due_2021)
                    data.append(total_tax_due)
                    print(data)
                    for item in data:
                        if "See Redemption Statement" in item:
                            await Actor.push_data({'apn': apn_list[index], 'tax_due_2023': tax_due_2023, 'tax_due_2022': tax_due_2022, 'tax_due_2021': tax_due_2021, 'total_tax_due': total_tax_due})
                            break
                    index += 1
                    # with open('index.txt', 'w') as file:
                    #     file.write(str(index))
            except:
                try:
                    driver.quit()
                except:
                    pass

        
