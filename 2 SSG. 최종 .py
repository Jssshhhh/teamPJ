import folium
import pandas as pd

# 각 지역의 위도와 경도
locations = {
    "대구": (35.8411289243023, 128.6812363722680),
    "사직": (35.19403166, 129.06151836),
    "창원": (35.2219848625101, 128.579580117268),
    "광주": (35.1694249627668, 126.888805470329),
    "대전": (36.3173370007388, 127.428013823451),
    "수원": (37.2978428909635, 127.011348102567),
    "잠실": (37.5112525852452, 127.072863377526),
    "고척": (37.4982125677913, 126.867088741096),
    "문학": (37.4350819826381, 126.690759830613)
}

# 팀별 색상 설정
color_map = {
    "LG": ["", "", "", "", "", ""],
    "KIA": ["", "", "", "", "", ""],
    "SAMSUNG": ["", "", "", "", "", ""],
    "DOSAN": ["	#00008B", "	#000080", "	#0000CD", "#0000FF", "#4169E1", "#6495ED", "#1E90FF", "#00BFFF", "#00FFFF"],
    "HANWHA": ["#FF4500", "#FFA500", "#FF8C00", "#FF7F50", "#FFDAB9", "	#FFE4C4", "#FFE4C4", "#FFE4B5"],
    "KIWOOM":["#FF1493", "#C71585", "#800080", "#8B008B", "#4B0082", "#EE82EE", "#DA70D6", "#D8BFD8", "#E6E6FA"],
    "KT": ["#191919", "#353535", "#5D5D5D", "#8C8C8C", "#A6A6A6", "#BDBDBD", "#D5D5D5", "#EAEAEA", "#F6F6F6"],
    "LOTTE": ["", "", "", "", "", ""],
    "NC": ["", "", "", "", "", ""],
    "SSG": ["#FF0000", "#DC143C", "#B22222", "#800000", "#8B0000", "#A52A2A", "#A0522D", "#8B4513", "#CD5C5C"],

    # 다른 팀들에 대한 색상 추가
}

# 데이터프레임 생성
df = pd.DataFrame(
    [(key, value[0], value[1]) for key, value in locations.items()],
    columns=['경기장', '위도', '경도']
)

# 경기장 별 승률 데이터 로드
LG_data = pd.read_csv('./rate_data/Lg_data.csv', encoding='cp949')
KIA_data = pd.read_csv('./rate_data/KIA_data.csv', encoding='cp949')
SAMSUNG_data = pd.read_csv('./rate_data/SAMSUNG_data.csv', encoding='cp949')
DOSAN_data = pd.read_csv('./rate_data/DOSAN_data.csv', encoding='cp949')
HANWHA_data = pd.read_csv('./rate_data/HANWHA_data.csv', encoding='cp949')
KIWOOM_data = pd.read_csv('./rate_data/KIWOOM_data.csv', encoding='cp949')
KT_data = pd.read_csv('./rate_data/KT_data.csv', encoding='cp949')
LOTTE_data = pd.read_csv('./rate_data/LOTTE_data.csv', encoding='cp949')
NC_data = pd.read_csv('./rate_data/NC_data.csv', encoding='cp949')
SSG_data = pd.read_csv('./rate_data/SSG_data.csv', encoding='cp949')

# df와 csv 데이터 머지
merged = df.set_index('경기장').join(SSG_data.set_index('경기장'))

# 공백을 제거하기 위해 reset_index() 사용
merged.reset_index(inplace=True)

# 최종 결과 출력
merged = merged.sort_values(by='승률', ascending=False)

# Folium 맵 생성 (중심을 한국 중부로 설정)
map_center = [36.5, 127.5]
m = folium.Map(location=map_center, zoom_start=7)

# 각 지역 마커 추가 (아이콘 색상 구분)
for index, row in merged.iterrows():
    # 경기장 이름에 따라 팀 구분
    if "KT" in row['경기장']:
        colors = color_map["KT"]
    elif "두산" in row['경기장']:
        colors = color_map["두산"]
    elif "SSG" in row['경기장']:
        colors = color_map["SSG"]
    # 다른 팀들에 대한 조건 추가
    
    # 색상 배열에서 순서대로 색상 선택
    icon_color = colors[index % len(colors)]

    # 기본 아이콘 사용
    folium.CircleMarker(
        location=[row['위도'], row['경도']],
        popup=row['경기장'],
        color=icon_color,
        fill=True,
        fill_color=icon_color,
        fill_opacity=0.9,
        radius=10,
    ).add_to(m)

# 지도 저장
m.save("kbo_team_distance_SSGmap최종2_default_size_icons.html")