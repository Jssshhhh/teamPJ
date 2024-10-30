import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.font_manager as fm
font_name = fm.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
plt.rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False 

df=pd.read_csv('상관관계_수정본2.csv', encoding='cp949')
print(df)



# data= df[~df['변수'].isin(['승리', '이닝'])]
# data

# cols=['승률_투수', '볼넷', '출루율', '승리']
# corr=df[cols].corr(method='person')
# corr
# corr.values
# Plot the remaining variables' correlations with '승률'
# plt.figure(figsize=(10, 6))
# sns.barplot(x='상관관계', y='변수', data=data)
# plt.title('Correlations with 승률 (excluding 승리 and 이닝)')
# plt.xlabel('Correlation')
# plt.ylabel('Variables')
# plt.tight_layout()
# plt.show()


#히트맵
# numeric_df=df.select_dtypes(include='number')
# correlation_matrix=numeric_df.corr()

# fig, ax = plt.subplots()
# im = ax.imshow(correlation_matrix, cmap='Greys', aspect='auto')
# ax.set_xticks(range(len(correlation_matrix.columns)))
# ax.set_yticks(range(len(correlation_matrix.index)))
# ax.set_xticklabels(correlation_matrix.columns)
# ax.set_yticklabels(correlation_matrix.index)
# plt.colorbar(im)
# plt.show()

# for x in range(len(df.columns)) :
#     for y in range(len(df.index)):
#         ax.text(y,x,df.iloc[y,x], ha='center', va='center', color='g')

# fig.tight_layout()
# plt.show()