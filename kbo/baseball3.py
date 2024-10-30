import folium
from geopy.distance import geodesic
import random

# 각 지역의 위도와 경도
locations = {
    "대구(삼성)": (35.8411289243023, 128.6812363722680),
    "부산(롯데)": (35.19403166, 129.06151836),
    "창원(NC)": (35.2219848625101, 128.579580117268),
    "광주(기아)": (35.1694249627668, 126.888805470329),
    "대전(한화)": (36.3173370007388, 127.428013823451),
    "수원(KT)": (37.2978428909635, 127.011348102567),
    "서울 잠실(LG)": (37.5112525852452, 127.072863377526),
    "서울 잠실(두산)" : (37.5112525852452, 127.072863377526),
    "서울 고척(키움)": (37.4982125677913, 126.867088741096),
    "인천(SSG)": (37.4350819826381, 126.690759830613)
}

# Folium 맵 생성 (중심을 한국 중부로 설정)
map_center = [36.5, 127.5]
m = folium.Map(location=map_center, zoom_start=7)

# 각 지역 구장에 사진 아이콘 추가
images = {
    "대구(삼성)": "./image/samsung-lions.jpg",
    "부산(롯데)": "./image/lotte-giants.jpg",
    "창원(NC)": "./image/nc-dinos.jpg",
    "광주(기아)" : "./image/kia-tigers.jpg",
    "대전(한화)" : "./image/hanwha-eagles.jpg",
    "수원(KT)" : "./image/kt-wiz.jpg",
    "서울 잠실(LG)" : "./image/lg-twins.jpg",
    "서울 잠실(두산)" : "./image/doosan-bears.jpg",
    "서울 고척(키움)" : "./image/kiwoom-heroes.jpg",
    "인천(SSG)" : "./image/ssg-landers.jpg"
    
}

team_colors = {
    "대구(삼성)": "blue",
    "부산(롯데)": "red",
    "창원(NC)": "green",
    "광주(기아)": "purple",
    "대전(한화)": "orange",
    "수원(KT)": "darkred",
    "서울 잠실(LG)": "lightred",
    "서울 잠실(두산)" : "black" , 
    "서울 고척(키움)": "beige",
    "인천(SSG)": "darkblue"
}

# 각 지역 마커 추가 (사진 아이콘 사용)
for loc_name, coords in locations.items():
    icon = folium.CustomIcon(images[loc_name], icon_size=(40, 40))  # 아이콘 크기 설정
    folium.Marker(location=coords, popup=loc_name, icon=icon).add_to(m)

# 각 지역 간 거리 계산 및 지도에 선 표시 (선의 색상을 랜덤으로 변경)
for loc1, coord1 in locations.items():
    for loc2, coord2 in locations.items():
        if loc1 != loc2:
            # 거리 계산
            distance = geodesic(coord1, coord2).kilometers
            # 지도에 선 표시 (두 지점 연결, 랜덤한 색상 선택)
            folium.PolyLine(
                locations=[coord1, coord2],
                color=team_colors[loc1],  # 출발 팀 색상 사용
                weight=2,  # 선의 두께
                opacity=0.5  # 투명도 높임
            ).add_to(m)

            midpoint = [(coord1[0] + coord2[0]) / 2, (coord1[1] + coord2[1]) / 2]
            folium.Marker(
                location=midpoint,
                icon=folium.Icon(icon_size=(15, 15), icon_color='white', color="lightgray"),  # 작은 크기의 마커
                tooltip=f"{loc1} ↔ {loc2}: {distance:.2f} km"  # 마우스를 올리면 거리 정보 표시
            ).add_to(m)

            
# 지도 저장
m.save("./data/kbo_team_distance_map_with_images.html")
