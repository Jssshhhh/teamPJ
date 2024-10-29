import folium
import matplotlib.colors as mcolors

# 각 구장별 위치 데이터
stadium_locations = {
    '광주 기아 챔피언스필드': [35.1694249627668, 126.888805470329],
    '대구 삼성 라이온즈 파크': [35.8411289243023, 128.6812363722680],
    '잠실야구장': [37.5162500127349, 127.079283389854],
    '수원 kt 위즈 파크': [37.2978428909635, 127.011348102567],
    '문학랜더스필드': [37.4350819826381, 126.690759830613],
    '사직야구장': [35.19403166, 129.06151836],
    '대전 이글스파크': [36.3173370007388, 127.428013823451],
    '마산, 창원 NC파크': [35.2219848625101, 128.579580117268],
    '고척스카이돔': [37.4982125677913, 126.867088741096],
}

# 기아의 각 구장별 승률 데이터
kia_win_rates = {
    '광주 기아 챔피언스필드': 0.46,  # 46%
    '대구 삼성 라이온즈 파크': 0.45,    # 45%
    '잠실야구장': 0.39,               # 39.375%
    '수원 kt 위즈 파크': 0.49,   # 49.58%
    '문학랜더스필드': 0.52,                 # 52.5%
    '사직야구장': 0.46,                # 46.25%
    '대전 이글스파크': 0.45,     # 45%
    '마산, 창원 NC파크': 0.41,                # 41.25%
    '고척스카이돔': 0.40,                  # 40%
}

# 승률 범위 설정 및 색상 결정
def get_color(win_rate):
    if win_rate < 0.47:
        return "red"  # 낮은 승률
    elif 0.47 <= win_rate <= 0.52:
        return "green"  # 중간 승률
    else:
        return "blue"  # 높은 승률

# 지도 생성 (기아 홈 구장 기준)
m = folium.Map(location=[35.19403166, 129.06151836], zoom_start=7)

# 기아의 각 구장별 승률을 지도에 표시
for stadium, location in stadium_locations.items():
    win_rate = kia_win_rates.get(stadium, 0)  # 기본값을 0으로 설정
    color = get_color(win_rate)
    folium.CircleMarker(
        location=location,
        radius=10,  # 점의 크기
        color=color,  # 경계선 색상
        fill=True,
        fill_color=color,  # 승률에 따른 색상 적용
        fill_opacity=0.9,  # 적절한 불투명도 설정
        popup=f"{stadium} 승률: {win_rate * 100:.1f}%"
    ).add_to(m)

# 지도를 HTML로 저장
m.save("./data/kia_win_rates_gradient_stadiums5.html")