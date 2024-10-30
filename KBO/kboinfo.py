import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
url = "https://www.koreabaseball.com/Schedule/Schedule.aspx"
# HTML 읽기
response = requests.get(url)
driver = webdriver.Chrome()

driver.get(url)

year_select = Select(driver.find_element(By.ID, 'ddlYear'))
month_select = Select(driver.find_element(By.ID, 'ddlMonth'))
series_select = Select(driver.find_element(By.ID, 'ddlSeries'))
year_select.select_by_value('2024')
month_select.select_by_value('04')
series_select.select_by_value("0,9,6")

time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="boxList"]/ul/li[8]/a').click()
time.sleep(2)
year_select.select_by_value('2023')
time.sleep(2)
games = driver.find_elements(By.XPATH, '//*[@id="tblScheduleList"]/tbody')

days, farteams, farteam_points, hometeam_points, hometeams, ballparks = [], [], [], [], [], []

idx = 1
while True:
    try:
        if driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[9]').text != '-':
            idx += 1
            continue
            
        day = driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[1]').text
        farteam = driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[3]/span[1]').text
        farteam_point = driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[3]/em/span[1]').text
        hometeam_point = driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[3]/em/span[3]').text
        hometeam = driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[3]/span[2]').text
        ballpark = driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[8]').text
        
        days.append(day)
        ballparks.append(ballpark)
        farteams.append(farteam)
        farteam_points.append(farteam_point)
        hometeam_points.append(hometeam_point)
        hometeams.append(hometeam)
        print(day, ballpark, farteam, farteam_point, hometeam_point, hometeam)
        idx += 1
    except Exception as e:
        print(f"Error processing item {idx}: {e}")
        break  # 더 이상 항목이 없을 경우 종료

df = pd.DataFrame({
    'Date': days,
    '구장': ballparks,
    '원정팀': farteams,
    '원정팀점수': farteam_points,
    '홈팀점수': hometeam_points,
    '홈팀': hometeams
})

df.to_csv("롯데_2023_04기록.csv", index=False, encoding='utf-8-sig')
print(df)
driver.quit()
