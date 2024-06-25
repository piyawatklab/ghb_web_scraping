# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

# from seleniumbase import Driver
# import time
# from logging import ERROR

# import os
# import glob
# import shutil
# import sys

# import pandas as pd

from seleniumbase import Driver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import re
import time
import pandas as pd
from datetime import datetime

from tabulate import tabulate

data = []

def export_to_excel(data):

    df = pd.DataFrame(data)

    excel_filename = 'output_excel.xlsx'
    current_date = datetime.now()
    sheet_name = current_date.strftime('%Y-%m-%d')

    # เปิดไฟล์ Excel ที่มีอยู่แล้ว ถ้ามี และเขียนทับชีตที่ต้องการ
    with pd.ExcelWriter(excel_filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

def run():

    driver = Driver(uc=True)
    # driver = Driver(uc=True,headless=True)

    data = []

    try:
        url_main = 'https://www.ghbhomecenter.com/'
        sale_type_list = [
            'single_house-for-sale',
            'double_house-for-sale',
            ]
        county_list = [
            'Bangkok',
            # 'Nonthaburi',
            # 'SamutPrakan',
            ]

        for sale_type in sale_type_list:

            for county in county_list:

                page_no = 1
            
                while True:
                    # url = 'https://www.ghbhomecenter.com/single_house-for-sale?&pg=1'
                    url = url_main + sale_type + '/' + county + '?&pg=' + str(page_no)
                    driver.get(url)
                    time.sleep(2)

                    element_list = driver.find_elements(By.XPATH, ".//div[@class = 'card d-block']")
                    # if len(element_list) == 0 :
                    if len(element_list) == 0 or page_no >= 2 :
                        print('หยุดแล้ว หน้า :',str(page_no))
                        print('รวมเจอทั้งหมด :' , str(len(data)))
                        break

                    for element in element_list :
                        val = {}
                        val['county'] = county
                        val['sale_type'] = sale_type
                        val['link'] = element.find_element(By.XPATH, ".//a").get_attribute('href')
                        # val['img'] = element.find_element(By.XPATH, ".//img").get_attribute('src')
                        data.append(val)
                    
                    print('หน้า :',str(page_no))
                    print('เจอ :' , str(len(element_list)))
                    print('เจอทั้งหมด :' , str(len(data)))

                    # page_next_list = driver.find_element(By.XPATH, ".//ul[contains(@class, 'pagination')]")
                    # page_next = page_next_list.find_elements(By.XPATH, ".//li")
                    # print(page_next[-1].text)
                    # print(page_next[-1].text.isnumeric())
                    
                    page_no += 1
                    # if page_next[-1].text.isnumeric():
                    #     break
                    # else:
                    #     # if 
                    #     page_no += 1
                    #     continue

    except Exception as e:
        print('All : ' , str(len(data)))
        print(e)
    
    for index, item in enumerate(data, start=1):
        new_item = {'index': index}
        new_item.update(item)
        data[index - 1] = new_item
    
    # เขียนข้อมูลลง excel file 
    # export_to_excel(data)

    df = pd.DataFrame(data)

    excel_filename = 'output_excel.xlsx'
    sheet_name = 'list'

    # เปิดไฟล์ Excel ที่มีอยู่แล้ว ถ้ามี และเขียนทับชีตที่ต้องการ
    with pd.ExcelWriter(excel_filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    for item in data :
        url = item['link']
        driver.get(url)
        time.sleep(2)

        try:
            title_element = driver.find_element(By.XPATH, ".//div[contains(@class, 'col-md-8 col-xs-push-12')]")
            item['title'] = title_element.find_element(By.XPATH, ".//a").get_attribute('title')

            item['price'] = title_element.find_element(By.XPATH, ".//h3").text
            # numbers = re.findall(r'\d+', title_element.find_element(By.XPATH, ".//h3").text)
            # result = ''.join(numbers)
            # result_int = int(result)
            # item['price'] = result_int
            
            image_element = driver.find_element(By.XPATH, ".//div[contains(@class, 'img-fill')]")
            item['image_link'] = image_element.find_element(By.XPATH, ".//img").get_attribute('src')

            property_details = driver.find_element(By.XPATH, ".//div[contains(@class, 'property_details_box')]").text
            property_details = property_details.replace("\n", " \n")
            item['property_details'] = property_details

            row_property_details = driver.find_element(By.XPATH, ".//div[contains(@class, 'row-property-details')]").text
            row_property_details = row_property_details.replace("\n", " \n")
            item['row_property_details'] = row_property_details

            # property_info = driver.find_element(By.XPATH, ".//div[contains(@class, 'list-unstyled,property-info-action')]").text
            # property_info = property_info.replace("\n", " \n")
            # item['property_info'] = property_info

            print(item)

        except Exception as e:
            print(e)
            continue
    
    # # เขียนข้อมูลลง excel file 
    # df = pd.DataFrame(data)
    # df.to_excel('output_excel.xlsx', index=False)

    export_to_excel(data)

if __name__ == "__main__":

    run()
    
    