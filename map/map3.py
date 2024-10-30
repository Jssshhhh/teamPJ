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

# 이미지 마커 설정
images = {
   "잠실": './logoimages/combined_logo.jpg',
   "대구": './logoimages/samsung-lions.jpg',
   "사직": './logoimages/lotte-giants.jpg',
   "창원": './logoimages/nc-dinos.jpg',
   "광주": './logoimages/kia-tigers.jpg',
   "대전": './logoimages/hanwha-eagles.jpg',
   "수원": './logoimages/kt-wiz.jpg',
   "고척": './logoimages/kiwoom-heroes.jpg',
   "문학": './logoimages/ssg-landers.jpg'
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

# 맵의 기본 중심 좌표
map_center = [36.5, 127.5]

# 색상 리스트
colors = ["#800000", "#9B1C1C", "#B23939", "#C94D4D", "#DB6B6B", "#E89A9A", "#F3BDBD", "#F8D7D7", "#FCECEC"]

# 지도 생성 함수 정의
def create_map(team_data, image_key, filename):
    # 데이터프레임 병합
    merged = df.set_index('경기장').join(team_data.set_index('경기장'))
    merged.reset_index(inplace=True)
    merged = merged.sort_values(by='승률', ascending=False)

    # Folium 맵 생성
    m = folium.Map(location=map_center, zoom_start=8)

    # 각 경기장에 마커 추가
    for i, (index, row) in enumerate(merged.iterrows()):
        icon_color = colors[i % len(colors)]

        # 색상 마커 추가
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            popup=row['경기장'],
            color=icon_color,
            fill=True,
            fill_color=icon_color,
            fill_opacity=0.9,
            radius=15,
        ).add_to(m)

        # 특정 팀 경기장에 이미지 마커 덧씌우기
        if row['경기장'] == image_key:
            image_url = images.get(image_key)
            html = f'''
            <div style="width: 30px; height: 30px; background-image: url({image_url}); background-size: 100%; background-position: center; background-repeat: no-repeat; border-radius: 50%; transform: translate(-30%, -30%);"></div>
            '''
            icon = folium.DivIcon(html=html)
            
            # 이미지 마커 추가
            folium.Marker(
                location=[row['위도'], row['경도']],
                popup=row['경기장'],
                icon=icon
            ).add_to(m)

    # 지도 저장
    m.save(filename)

# 10개의 지도 생성 예시 (다른 팀 데이터를 사용)
create_map(LG_data, '잠실', 'kbo_team_distance_map_lg_twins.html')
create_map(KIA_data, '광주', 'kbo_team_distance_map_kia_tigers.html')
create_map(SAMSUNG_data, '대구', 'kbo_team_distance_map_samsung_lions.html')
create_map(DOSAN_data, '잠실', 'kbo_team_distance_map_doosan-bears.html')
create_map(HANWHA_data, '대전', 'kbo_team_distance_map_hanwha-eagles.html')
create_map(KIWOOM_data, '고척', 'kbo_team_distance_map_kiwoom-heroes.html')
create_map(KT_data, '수원', 'kbo_team_distance_map_kt-wiz.html')
create_map(LOTTE_data, '사직', 'kbo_team_distance_map_lotte-giants.html')
create_map(NC_data, '창원', 'kbo_team_distance_map_nc-dinos.html')
create_map(SSG_data, '문학', 'kbo_team_distance_map_ssg-landers.html')

# 추가적으로 필요한 데이터를 위 함수 호출로 생성
# 예시:
# create_map(Hanwha_data, '대전', 'kbo_team_distance_map_hanwha_eagles.html')
# create_map(KT_data, '수원', 'kbo_team_distance_map_kt_wiz.html')