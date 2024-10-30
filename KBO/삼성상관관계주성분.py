import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA

# 한글 폰트 설정
import matplotlib.font_manager as fm
font_name = fm.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
plt.rc('font', family=font_name)

# 데이터 불러오기
file_path = '삼성_결합_기록.csv'
data = pd.read_csv(file_path)

# 1. 타겟 변수 (승률)와 피처(나머지 숫자형 변수들) 설정
X = data.drop(columns=['연도', '승률'])  # '승률'을 제외한 나머지를 피처로 사용
y = data['승률']  # 타겟 변수는 '승률'

# 숫자형 데이터만 사용하도록 제한
X_numeric = X.select_dtypes(include=[float, int])

# 2. 데이터 표준화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_numeric)


# 3. 주성분 분석(PCA) - 설명력이 높은 성분을 10개로 설정
pca = PCA(n_components=10)

# 4. 회귀분석 적용
regression = LinearRegression()

# 5. 결측값을 평균값으로 대체
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X_scaled)

# 6. PCA 적용
X_pca = pca.fit_transform(X_imputed)

# 7. 회귀분석을 위한 데이터 분할 (훈련/테스트)
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)

# 8. 회귀분석 적용
regression.fit(X_train, y_train)

# 9. 회귀분석 결과 (가중치 및 설명력 출력)
coefficients = regression.coef_
r_squared = regression.score(X_test, y_test)

print('가중치 : ',coefficients, 'R^2 : ', r_squared)  # 가중치와 R^2 값을 출력

# 5. 데이터를 훈련/테스트 세트로 분할
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)

# 6. 여러 모델을 사용해보기

# (1) Linear Regression
regression = LinearRegression()
regression.fit(X_train, y_train)
y_pred_lr = regression.predict(X_test)
print('Linear Regression R^2:', r2_score(y_test, y_pred_lr))

# (2) Random Forest Regressor
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
print('Random Forest R^2:', r2_score(y_test, y_pred_rf))

# (3) Gradient Boosting Regressor
gb_model = GradientBoostingRegressor(random_state=42)
gb_model.fit(X_train, y_train)
y_pred_gb = gb_model.predict(X_test)
print('Gradient Boosting R^2:', r2_score(y_test, y_pred_gb))

# (4) TensorFlow Neural Network (딥러닝 모델)
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))  # 출력은 1개 (회귀)
model.compile(optimizer='adam', loss='mse')

# 모델 학습
model.fit(X_train, y_train, epochs=100, verbose=0)

# 예측 및 평가
y_pred_nn = model.predict(X_test)
print('Neural Network R^2:', r2_score(y_test, y_pred_nn))

# 7. 최종 평가
print("Linear Regression MSE:", mean_squared_error(y_test, y_pred_lr))
print("Random Forest MSE:", mean_squared_error(y_test, y_pred_rf))
print("Gradient Boosting MSE:", mean_squared_error(y_test, y_pred_gb))
print("Neural Network MSE:", mean_squared_error(y_test, y_pred_nn))