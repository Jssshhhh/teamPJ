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



    

# 필요한 데이터를 찾기 위해 롯데 관련 행 필터링




# 데이터 수집
# data = []
# for row in rows:
#     cells = row.find_all("td")
#     if len(cells) > 0:
#         # 날짜
#         Date = cells[0].get_text(strip=True)
        
        
        
#         # 경기 팀과 점수
#         game_info = cells[2]
#         teams = game_info.find_all("span")
        
#         # 원정팀과 홈팀
#         away_team = teams[0].get_
#         home_team = teams[4].get_text(strip=True)

#         # 우승 점수와 패배 점수 (승리 또는 패배 여부를 포함한 데이터)
#         scores = game_info.find_all("span", {"class": ["win", "lose", "same"]})
#         if len(scores) == 2:
#             win_score = scores[0].get_text(strip=True)
#             lose_score = scores[1].get_text(strip=True)
#         else:
#             win_score = "N/A"
#             lose_score = "N/A"

#         # 구장
#         stadium = cells[6].get_text(strip=True)

#         # 특이사항
#         remarks = cells[7].get_text(strip=True)

#         # 수집한 데이터를 리스트에 추가
#         data.append([Date, away_team, home_team, win_score, lose_score, stadium, remarks])




# # DataFrame 생성
# columns = ["날짜", "팀", "상대팀", "구장", "결과", "승패", "기타"]
# df = pd.DataFrame(data, columns=columns)

# # CSV 파일로 저장
# df.to_csv("lotte_games.csv", index=False, encoding='utf-8-sig')
# print("롯데 경기 기록이 CSV 파일로 저장되었습니다.")
