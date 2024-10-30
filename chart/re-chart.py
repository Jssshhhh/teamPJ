import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
import matplotlib.font_manager as fm
font_name = fm.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
plt.rc('font', family=font_name)

# 데이터 불러오기
CC_data = pd.read_csv('상관관계_수정본2.csv', encoding='cp949')

# 20번째 컬럼까지 선택 (0~19번째 컬럼)
dataF = CC_data.iloc[:, :20].copy()

# 컬럼 페어를 생성 (0-1, 2-3, ..., 18-19)
column_pairs = [(i, i+1) for i in range(0, 20, 2)]
print(column_pairs)

# 그래프 그리기
for pair in column_pairs:
    x_col = dataF.columns[pair[0]]
    y_col = dataF.columns[pair[1]]

    # 결측값 처리: 결측값이 있는 행 제거
    dataF_sorted = dataF[[x_col, y_col]].dropna().sort_values(by=y_col)
    
    # 데이터 타입 확인
    print(f'{x_col} 타입: {dataF_sorted[x_col].dtype}, {y_col} 타입: {dataF_sorted[y_col].dtype}')
    
    # 1. 바 그래프 (상관관계 높은 변수들)
    plt.figure(figsize=(10, 6))
    plt.barh(dataF_sorted[x_col], dataF_sorted[y_col], color='green')
    plt.xlim(-1, 1)
    plt.tick_params(axis='y', which='both', left=False, labelleft=False)
    plt.xlabel(f'{y_col}')
    plt.ylabel(f'{x_col}')
    plt.title(f'{x_col}와 {y_col}의 bar그래프')
    plt.show()

    # 2. 산점도 (변수별 상관관계 시각화)
    green_palette = sns.color_palette("Greens", as_cmap=True)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=dataF_sorted, x=x_col, y=y_col, hue=y_col, palette=green_palette, s=100)
    plt.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
    plt.xticks(rotation=45)
    plt.ylim(-1,1)
    plt.xlabel(f'{x_col}')
    plt.ylabel(f'{y_col}')
    plt.title(f'{x_col}와 {y_col}의 산점도')
    plt.show()




'''# 3. 히트맵 (변수들의 상관관계 시각화)
# corr_matrix = dataF.corr()
plt.figure(figsize=(12, 10))
heatmap1 = sns.heatmap(data=dataF, 
            annot=False, 
            fmt='.2f', 
            cmap='coolwarm', 
            vmin=-1, 
            vmax=1, 
            linewidths=0.5, 
            annot_kws={"size": 10})
heatmap1.xaxis.tick_top()
heatmap1.set(
    xlabel = 'kt_변수',
    ylabel = 'kt_상관관계'
)
plt.title('승률과 상관관계 히트맵')
plt.show()'''
