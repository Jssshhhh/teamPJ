import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.distance import geodesic
import matplotlib

# 폰트 설정
font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)

# CSV 파일 불러오기
file_path = 'C:/Mtest/개인연습/롯데_데이터.csv'
lotte_data = pd.read_csv(file_path)
locations = {
    "대구(삼성)": (35.8411289243023, 128.6812363722680),
    "부산(롯데)": (35.19403166, 129.06151836),
    "창원(NC)": (35.2219848625101, 128.579580117268),
    "광주(기아)": (35.1694249627668, 126.888805470329),
    "대전(한화)": (36.3173370007388, 127.428013823451),
    "수원(KT)": (37.2978428909635, 127.011348102567),
    "서울 잠실(LG, 두산)": (37.5112525852452, 127.072863377526),
    "서울 고척(키움)": (37.4980879456876, 126.867026290623)
}

lotte_home_location = locations.get("부산(롯데)")




def calculate_travel_distance_v3(games_df, team_name, team_home_location):
    """
    특정 팀의 경기 데이터를 기반으로 이동거리를 계산하며, 주어진 이동 규칙을 반영합니다.

    Args:
    - games_df (DataFrame): 경기 일정과 구장이 포함된 데이터
    - team_name (str): 이동 거리를 계산할 팀 이름
    - team_home_location (tuple): 팀의 홈 위치 좌표

    Returns:
    - total_distance (float): 총 이동 거리 (킬로미터 단위)
    """
    total_distance = 0.0
    last_location = team_home_location  # 팀의 홈 위치에서 시작
    first_game = True
    mid_season_break = False

    for index, row in games_df.iterrows():
        stadium = row['구장']
        home_team = row['홈팀']
        away_team = row['원정팀']
        date = row['Date']

        # 팀이 홈에서 경기하는지 아니면 원정인지 확인
        if team_name == away_team:
            current_location = locations.get(f"{stadium}({home_team})", None)  # 경기장 이름과 홈팀으로 위치 매핑
            
            if current_location:
                # 1. 각 경기 장소 간의 이동 거리 계산
                if last_location:
                    total_distance += geodesic(last_location, current_location).kilometers

                # 2. 시즌 개막 경기가 원정일 경우 홈에서 원정까지의 왕복 거리 추가
                if first_game:
                    total_distance += geodesic(team_home_location, current_location).kilometers
                    first_game = False

                # 3. 전반기 마지막 시리즈가 원정이며 후반기 첫 시리즈도 원정인 경우 홈으로 돌아오는 이동 거리 추가
                if mid_season_break:
                    # 전반기 마지막 경기 후 홈으로 이동하고, 후반기 첫 경기로 이동
                    total_distance += geodesic(last_location, team_home_location).kilometers
                    total_distance += geodesic(team_home_location, current_location).kilometers
                    mid_season_break = False

                last_location = current_location  # 마지막 위치 업데이트
        elif team_name == home_team:
            # 팀이 홈경기를 할 경우 마지막 위치를 홈구장으로 초기화
            last_location = team_home_location

        # 전반기 마지막 시리즈가 원정인지 감지하고, 플래그 설정
        if "07.09" in date:  # 시즌 중간을 나타내는 예시 날짜 (필요에 따라 조정 가능)
            mid_season_break = True

    return total_distance

total_distance_lotte_v3 = calculate_travel_distance_v3(lotte_data, '롯데', lotte_home_location)
print(total_distance_lotte_v3)


# 데이터 준비: 경기당 승률과 누적 이동 거리 계산
lotte_data['승률'] = (lotte_data['원정팀점수'] > lotte_data['홈팀점수']).cumsum() / (lotte_data.index + 1)
lotte_data['누적이동거리'] = lotte_data.apply(
    lambda row: calculate_travel_distance_v3(lotte_data.iloc[:row.name+1], '롯데', lotte_home_location), axis=1
)

# 산점도: 누적 이동 거리 vs 승률
plt.figure(figsize=(10, 6))
sns.scatterplot(data=lotte_data, x='누적이동거리', y='승률')
plt.title('누적 이동 거리와 승률')
plt.xlabel('누적 이동 거리 (km)')
plt.ylabel('승률')
plt.grid(True)
plt.show()

# 라인 플롯: 시간에 따른 누적 이동 거리와 승률
fig, ax1 = plt.subplots(figsize=(12, 6))

# 누적 이동 거리 그래프
ax1.set_xlabel('경기 인덱스')
ax1.set_ylabel('누적 이동 거리 (km)', color='tab:blue')
ax1.plot(lotte_data.index, lotte_data['누적이동거리'], color='tab:blue', label='누적 이동 거리')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# 보조 y축에 승률 표시
ax2 = ax1.twinx()
ax2.set_ylabel('승률', color='tab:green')
ax2.plot(lotte_data.index, lotte_data['승률'], color='tab:green', linestyle='--', label='승률')
ax2.tick_params(axis='y', labelcolor='tab:green')

fig.tight_layout()
plt.title('시간에 따른 누적 이동 거리와 승률')
plt.show()

# 경기당 이동 거리와 승률의 히트맵
plt.figure(figsize=(12, 6))
sns.heatmap(lotte_data[['누적이동거리', '승률']].T, cmap="YlGnBu", annot=True)
plt.title('경기당 누적 이동 거리와 승률 히트맵')
plt.show()
