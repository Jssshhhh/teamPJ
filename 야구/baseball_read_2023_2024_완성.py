import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

url = "https://www.koreabaseball.com/Schedule/Schedule.aspx"
driver = webdriver.Chrome()
driver.get(url)


# 선택자 초기화
year_select = Select(driver.find_element(By.ID, 'ddlYear'))
month_select = Select(driver.find_element(By.ID, 'ddlMonth'))
series_select = Select(driver.find_element(By.ID, 'ddlSeries'))

year_select.select_by_value('2024')
month_select.select_by_value('04')
series_select.select_by_value("0,9,6")

driver.find_element(By.XPATH, '//*[@id="boxList"]/ul/li[8]/a').click()

# 데이터 저장을 위한 리스트 초기화
days, farteams, farteam_points, hometeam_points, hometeams, ballparks = [], [], [], [], [], []

# 시작 연도와 월 설정
year = 2023  # 시작 연도
month = 4    # 시작 월
end_year = 2024  # 종료 연도


def isExistXpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        return True
    except:
        return False



while True:
    # 종료 조건 확인
    if year > end_year:
        break

    # 연도와 월 설정

    year_select = Select(driver.find_element(By.ID, 'ddlYear'))
    month_select = Select(driver.find_element(By.ID, 'ddlMonth'))
    series_select = Select(driver.find_element(By.ID, 'ddlSeries'))

    year_select.select_by_value(str(year))
    month_select.select_by_value(f"{month:02d}")  # 월을 두 자리로 포맷팅
    series_select.select_by_value("0,9,6")


    idx = 1  # 데이터 인덱스 초기화



    while True:
        try:
            
            
           

            dayelement = driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[1]')
            rowspan = dayelement.get_attribute('rowspan')
            if driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[9]').text != '-':
                idx += 1
                continue
            if rowspan == '2':
                
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
                # 주의사항: rowspan==2 인경우 XPATH의 변동이 있음
                farteam = driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[2]/span[1]').text
                farteam_point = driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[2]/em/span[1]').text
                hometeam_point = driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[2]/em/span[3]').text
                hometeam = driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[2]/span[2]').text
                ballpark = driver.find_element(By.XPATH, f'//*[@id="tblScheduleList"]/tbody/tr[{idx}]/td[7]').text
                days.append(day)
                ballparks.append(ballpark)
                farteams.append(farteam)
                farteam_points.append(farteam_point)
                hometeam_points.append(hometeam_point)
                hometeams.append(hometeam)
                print(day, ballpark, farteam, farteam_point, hometeam_point, hometeam)
                idx += 1
            else:
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
            print(f"Error processing item {idx} on {year}-{month}: {e}")
            idx += 1 
            break
    # 다음 월로 이동
    month += 1
    # 10월 이후의 야구는 없으므로...
    if month > 10:
        #2024년 같은 경우 3월에 경기 있음
        month = 3
        year += 1

# 데이터프레임 생성 및 저장
df = pd.DataFrame({
    'Date': days,
    '구장': ballparks,
    '원정팀': farteams,
    '원정팀점수': farteam_points,
    '홈팀점수': hometeam_points,
    '홈팀': hometeams
})

df.to_csv("롯데_데이터.csv", index=False, encoding='utf-8-sig')
print(df)
driver.quit()
