import folium
import matplotlib.colors as mcolors
from geopy.distance import geodesic
import random


locations = {
    "대구(삼성)": (35.8411289243023, 128.6812363722680),
    "부산(롯데)": (35.19403166, 129.06151836),
    "창원(NC)": (35.2219848625101, 128.579580117268),
    "광주(기아)": (35.1694249627668, 126.888805470329),
    "대전(한화)": (36.3173370007388, 127.428013823451),
    "수원(KT)": (37.2978428909635, 127.011348102567),
    "서울 잠실(LG)": (37.53934562772943 , 127.214776054013),
    "서울 잠실(두산)" : (37.5162500127349, 127.079283389854) ,
    "서울 고척(키움)": (37.4982125677913, 126.867088741096),
    "인천(SSG)": (37.4350819826381, 126.690759830613)
}

# 롯데 자이언츠의 각 구장별 원정 승률 데이터 (예시)
lotte_away_win_rates = {
    'LG 트윈스': {'location': [37.53934562772943 , 127.214776054013], 'away_win_rate': 0.4},
    '두산 베어스' : {'location' : [37.5162500127349, 127.079283389854], 'away_win_rate' : 0.4} ,
    '키움 히어로즈': {'location': [37.4982125677913, 126.867088741096], 'away_win_rate': 0.4125},
    'SSG 랜더스': {'location': [37.4350819826381, 126.690759830613], 'away_win_rate': 0.375},
    'NC 다이노스': {'location': [35.2219848625101, 128.579580117268], 'away_win_rate': 0.425},
    '삼성 라이온즈': {'location': [35.8411289243023, 128.6812363722680], 'away_win_rate': 0.45},
    'KIA 타이거즈': {'location': [35.1694249627668, 126.888805470329], 'away_win_rate': 0.3875},
    '한화 이글스': {'location': [36.3173370007388, 127.428013823451], 'away_win_rate': 0.45},
    'KT 위즈': {'location': [37.2978428909635, 127.011348102567], 'away_win_rate': 0.4875},
    '롯데 홈' :{'location': [35.19403166, 129.06151836], 'away_win_rate': 0.4986},
}

images = {
    "대구(삼성)": "https://i.namu.wiki/i/nIFLDX1ihQwBVokkFpaaA5_j7lzBn7yxWQTgKnHtWi7T-_n7ZXho4bk25Wr4nln83jp_7UK5HPoj2Y-5C4izWNlmwwk_xuJw9sP8eFVsUo51G5tqHxO4j1d02FueZTsPO3djYZFBMAGVzHWMehVhvw.svg",
    "부산(롯데)": "https://i.namu.wiki/i/qR3opgWyvcqT8O22XmKyMQAsFoaCMmtXH0El-iDBYhXB0RxfEQhbYUdV-TBudx1W3l_bUkK1KAZDFtt172W79c9C6Yc3YbVsklhHEf0_b1mHtqrwuNFXNJ67MsaYIvykptvBl6Nxerxc4mvHS-7z2Q.svg",
    "창원(NC)": "https://i.namu.wiki/i/zsmHt6UT62Ah-_Evr58aDNRFWNfRNKVXhQs35BYUxOPZ3t2MO2OQ_4pSZdYeD2xUSmfWXpUPFA5gJWu7z6GvHGcsz_S8jv9eXgUlwb0HffOi8uYeB-MjQXfVovhThSbjRVDlbSRmWfO70mpbPcFJpg.svg",
    "광주(기아)": "https://i.namu.wiki/i/wFayYt5GXe5x0OlMmalioj7G2c3DeLkLWJiRL2oP_PciuuQ4RiLQrYe2BRLhJ-Cn0ALLzidmj63vDpmMQBo0StbmOcjApJmiP3vRwBrjd0uLxI-Ku6K8LeWT9KP8yTIadM8JBxllf8ZSjrQWUu_Opw.svg",
    "대전(한화)": "https://i.namu.wiki/i/UO3cLQWbNsm-D4ZZ1QpKWsCyjIXvoRBRqF2C3pJz9COiYBQaHXVee1ppuO37g3SqHIiEmEccgPU1SAPxp9Nea-iXfKDFhUJvoFYhtdVFsC7oRjyDsREoCnocWz2ujxmerf_WjL64zrV9FTn69fy2QA.svg",
    "수원(KT)": "https://i.namu.wiki/i/-Op5HRrVtorB9yOdP7e2ZzNvBgE3WHZP0jSn3UZsUzg8z9kZBN2F0r4Nrck-m5aBK30vLEELz8xgsqqx57ddyQ.svg",
    "서울 잠실(LG)": "https://i.namu.wiki/i/N0z9TehLEmQjCo-zLrr3hb88FHRIbgU_ngkEgkd7EKz8ngUhi-1GI_ngwGliBx4G3VzzckRDGKULwM6dLOggqUGV4RFrrqinNz2M2pLgM4FG50vAjZvw2AyhpkrDhq7fZO2khD1hfu0cBKZH50sIWA.svg",
    "서울 잠실(두산)" : "https://i.namu.wiki/i/cDVrQIU8Clo9QtpeOKmnA7uFs3z__ESk80rOtjtEYxjwYAEaoGs39iF1DYg3CVHhcBfq8L6BLUkY4SNzbyzDZOkdf92V3bJHP-_z6a0Q2yLWsaKSEZZi9XxjA0uM9L6c1FIT3aLVY0iSrFooZZqPug.svg" ,
    "서울 고척(키움)": "https://i.namu.wiki/i/-rzSl860TxcORH5L617NnG79AeRq7ZHfkF0JvLfaAh1CyTbIBL_doH024nfTMy6JNBeWRi0bcQzJbtCHKcVPQ4XraLMWAJZGkkAQtRpIuQcAyJIQhcq5kjJTpW_g1hDKUsT--pKIFn0gK8g7gd34vw.svg",
    "인천(SSG)": "https://i.namu.wiki/i/cVYwBLxze1Oy3RGvNpSmeXxgKamX-46qthUbUrS_HVEtXD5wZnBoAi80WlwC-UAYTsZn6LPRyv5G9tjUwPxi6ji-AQSrI5vmY709IGhDNO5FoMiBYNSCHTEpvUXU7mrUrNUS4cD1bynYYQE-xDB6qA.svg"
}

norm = mcolors.Normalize(vmin=0.37, vmax=0.5)
cmap = mcolors.LinearSegmentedColormap.from_list("winrate_gradient", ["red", "yellow", "green"])


def get_color_from_winrate(win_rate):
    # 0.4 ~ 0.6 범위 내에서 색상 계산
    return mcolors.to_hex(cmap(norm(win_rate)))


# 지도 생성 (롯데 자이언츠 홈 구장 기준)
m = folium.Map(location=[35.19403166, 129.06151836], zoom_start=7)

# 두산 베어스의 각 원정 경기 승률을 지도에 표시
for team, data in lotte_away_win_rates.items():
    color = get_color_from_winrate(data['away_win_rate'])
    folium.CircleMarker(
        location=data['location'],
        radius=15,  # 점의 크기
        color=color,  # 경계선 색상
        fill=True,
        fill_color=color,  # 승률에 따른 색상 적용
        fill_opacity=0.9,  # 적절한 불투명도 설정
        popup=f"{team} 원정 승률: {data['away_win_rate']*100:.1f}%"
    ).add_to(m)
    
for loc_name, coords in locations.items():
    image_url = images[loc_name]
    # HTML로 이미지를 추가하고 CSS로 둥글게 만들기
    html = f'''
    <div style="width: 40px; height: 40px; background-image: url({image_url}); background-size: cover; border-radius: 50%; border: 2px solid white;"></div>
    '''
    icon = folium.DivIcon(html=html)
    
    folium.Marker(
        location=coords,
        popup=loc_name,
        icon=icon
    ).add_to(m)
# 지도를 HTML로 저장
m.save("./data/lotte_away_win_rates_gradient_image.html")

