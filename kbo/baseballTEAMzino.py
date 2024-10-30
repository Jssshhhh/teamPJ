import folium
import pandas as pd
import matplotlib.colors as mcolors

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

images = {
    "대구": "https://i.namu.wiki/i/nIFLDX1ihQwBVokkFpaaA5_j7lzBn7yxWQTgKnHtWi7T-_n7ZXho4bk25Wr4nln83jp_7UK5HPoj2Y-5C4izWNlmwwk_xuJw9sP8eFVsUo51G5tqHxO4j1d02FueZTsPO3djYZFBMAGVzHWMehVhvw.svg",
    "사직": "https://i.namu.wiki/i/qR3opgWyvcqT8O22XmKyMQAsFoaCMmtXH0El-iDBYhXB0RxfEQhbYUdV-TBudx1W3l_bUkK1KAZDFtt172W79c9C6Yc3YbVsklhHEf0_b1mHtqrwuNFXNJ67MsaYIvykptvBl6Nxerxc4mvHS-7z2Q.svg",
    "창원": "https://i.namu.wiki/i/zsmHt6UT62Ah-_Evr58aDNRFWNfRNKVXhQs35BYUxOPZ3t2MO2OQ_4pSZdYeD2xUSmfWXpUPFA5gJWu7z6GvHGcsz_S8jv9eXgUlwb0HffOi8uYeB-MjQXfVovhThSbjRVDlbSRmWfO70mpbPcFJpg.svg",
    "광주": "https://i.namu.wiki/i/wFayYt5GXe5x0OlMmalioj7G2c3DeLkLWJiRL2oP_PciuuQ4RiLQrYe2BRLhJ-Cn0ALLzidmj63vDpmMQBo0StbmOcjApJmiP3vRwBrjd0uLxI-Ku6K8LeWT9KP8yTIadM8JBxllf8ZSjrQWUu_Opw.svg",
    "대전": "https://i.namu.wiki/i/UO3cLQWbNsm-D4ZZ1QpKWsCyjIXvoRBRqF2C3pJz9COiYBQaHXVee1ppuO37g3SqHIiEmEccgPU1SAPxp9Nea-iXfKDFhUJvoFYhtdVFsC7oRjyDsREoCnocWz2ujxmerf_WjL64zrV9FTn69fy2QA.svg",
    "수원": "https://i.namu.wiki/i/-Op5HRrVtorB9yOdP7e2ZzNvBgE3WHZP0jSn3UZsUzg8z9kZBN2F0r4Nrck-m5aBK30vLEELz8xgsqqx57ddyQ.svg",
    "잠실": "https://s1.ihalla.com/upimages/gisaimg/202011/695532.jpg",
    "고척": "https://i.namu.wiki/i/-rzSl860TxcORH5L617NnG79AeRq7ZHfkF0JvLfaAh1CyTbIBL_doH024nfTMy6JNBeWRi0bcQzJbtCHKcVPQ4XraLMWAJZGkkAQtRpIuQcAyJIQhcq5kjJTpW_g1hDKUsT--pKIFn0gK8g7gd34vw.svg",
    "문학": "https://i.namu.wiki/i/cVYwBLxze1Oy3RGvNpSmeXxgKamX-46qthUbUrS_HVEtXD5wZnBoAi80WlwC-UAYTsZn6LPRyv5G9tjUwPxi6ji-AQSrI5vmY709IGhDNO5FoMiBYNSCHTEpvUXU7mrUrNUS4cD1bynYYQE-xDB6qA.svg"
}

# 데이터프레임 생성
df = pd.DataFrame(
    [(key, value[0], value[1]) for key, value in locations.items()],
    columns=['경기장', '위도', '경도']
)

# 경기장 별 승률 불러오기
LG_data = pd.read_csv('./away_data/Lotte_data.csv', encoding='cp949')

# df와 csv 데이터 머지
merged = df.set_index('경기장').join(LG_data.set_index('경기장'))
merged.reset_index(inplace=True)
merged = merged.sort_values(by='승률', ascending=False)

# Folium 맵 생성 (중심을 한국 중부로 설정)
map_center = [36.5, 127.5]
m = folium.Map(location=map_center, zoom_start=8)

# 더 세분화된 색상 구간 (빨강 -> 주황 -> 노랑 -> 연두 -> 초록)
def get_color(win_rate):
    if win_rate < 0.38:
        return '#FF0000'  # 진한 빨강
    elif 0.38 <= win_rate < 0.43:
        return '#FF4500'  # 주황
    elif 0.43 <= win_rate < 0.499:
        return '#FFA500'  # 노랑
    elif 0.499 <= win_rate < 0.518:
        return '#ADFF2F'  # 연두
    else:
        return '#008000'  # 진한 초록

# 승률에 따른 마커 추가
for i, (index, row) in enumerate(merged.iterrows()):
    color = get_color(row['승률'])
    
    folium.CircleMarker(
        location=[row['위도'], row['경도']],
        popup=row['경기장'],
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.9,
        radius=15,
    ).add_to(m)

# 강조할 팀 지정
highlight_team = "잠실"

# 이미지 마커 추가 (특정 팀 강조)
for loc_name, coords in locations.items():
    image_url = images[loc_name]
    
    # 강조할 팀은 반짝이는 마커로 설정
    if loc_name == highlight_team:
        html = f'''
        <div style="width: 60px; height: 60px; background-image: url({image_url}); 
        background-size: 50px 50px; background-position: center; 
        background-repeat: no-repeat; border-radius: 50%; border: 5px solid gold;
        animation: blink 1.5s infinite;"> <!-- 반짝이는 애니메이션 -->
        </div>
        <style>
        @keyframes blink {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
            100% {{ opacity: 1; }}
        }}
        </style>
        '''
    else:
        # 일반적인 마커 스타일
        html = f'''
        <div style="width: 40px; height: 40px; background-image: url({image_url}); 
        background-size: cover; border-radius: 50%; border: 2px solid white;">
        </div>
        '''
    
    icon = folium.DivIcon(html=html)
    
    folium.Marker(
        location=coords,
        popup=loc_name,
        icon=icon
    ).add_to(m)





# 지도 저장
m.save("./data/kbo_team_distance_map_TEAMzino.html")
