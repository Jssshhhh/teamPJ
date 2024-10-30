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
# 데이터프레임 생성
df = pd.DataFrame(
    [(key, value[0], value[1]) for key, value in locations.items()],
    columns=['경기장', '위도', '경도']
)
print(df)
# 경기장 별 승률 불러오기
SSG_data = pd.read_csv('SSG_data.csv',encoding='euc-kr')
print(SSG_data)
# df와 csv 데이터 머지
merged = df.set_index('경기장').join(SSG_data.set_index('경기장'))
# 공백을 제거하기 위해 reset_index() 사용
merged.reset_index(inplace=True)
# 최종 결과 출력
merged = merged.sort_values(by='승률', ascending=False)
print(merged)
# Folium 맵 생성 (중심을 한국 중부로 설정)
map_center = [36.5, 127.5]
m = folium.Map(location=map_center, zoom_start=7)
# 마커 색상을 구분할 수 있게 지정
colors = ["#FF0000", "#DC143C", "#B22222", "#800000", "#8B0000", "#A52A2A", "#A0522D", "#8B4513", "	#CD5C5C"]
# 각 지역 마커 추가 (아이콘 색상 구분)
for i, (index, row) in enumerate(merged.iterrows()):
    icon_color = colors[i % len(colors)]
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