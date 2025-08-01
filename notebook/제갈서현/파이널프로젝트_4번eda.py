# -*- coding: utf-8 -*-
"""파이널프로젝트_4번EDA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11QanIChF977DWrQNq-CJ_0bshaMvQS3q
"""

# 기본
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 경고 뜨지 않게 설정
import warnings
warnings.filterwarnings('ignore')

# 그래프 설정
sns.set()

# 그래프 기본 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
# plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['figure.figsize'] = 12, 6
plt.rcParams['font.size'] = 14
plt.rcParams['axes.unicode_minus'] = False

# 결측치 시각화를 위한 라이브러리
import missingno

# 데이터 전처리 알고리즘
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

# 학습용과 검증용으로 나누는 함수
from sklearn.model_selection import train_test_split

# 교차 검증
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold

# 평가함수
# 분류용
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score

# 회귀용
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

# 모델의 최적의 하이퍼 파라미터를 찾기 위한 도구
from sklearn.model_selection import GridSearchCV

import gc

!pip install pyarrow  # 먼저 pyarrow 설치

from google.colab import files
uploaded = files.upload()



# 파일명 리스트 (업로드한 실제 파일명과 일치시켜야 함)
file_list = [
    '201807_train_청구정보.parquet',
    '201808_train_청구정보.parquet',
    '201809_train_청구정보.parquet',
    '201810_train_청구정보.parquet',
    '201811_train_청구정보.parquet',
    '201812_train_청구정보.parquet'
]

# 각 파일을 읽어서 하나의 데이터프레임으로 결합
df_all = pd.concat([pd.read_parquet(f) for f in file_list], ignore_index=True)

print("합친 후 데이터 크기:", df_all.shape)

# 예시: 제거하고 싶은 컬럼 리스트 (원하는 대로 수정)
cols_to_drop = ['대표결제방법코드', '청구서발송여부_R3M', '청구금액_R3M', '포인트_마일리지_환산_B0M']

# 삭제
df_all.drop(columns=cols_to_drop, inplace=True)

# 확인
print("삭제 후 컬럼 목록:", df_all.columns.tolist())

# df_all.info()
# df_all.describe()
# df_all.isnull().sum()
# ID 기준으로 고객별 평균, 합계, 표준편차 등 집계
df_grouped = df_all.groupby('ID').agg(['mean', 'sum', 'std']).reset_index()

# 다중 컬럼 정리
df_grouped.columns = ['_'.join(col).strip() if col[1] else col[0] for col in df_grouped.columns.values]

# 확인
df_grouped.head()

# # 이상치 확인
# def detect_outliers_iqr(df, column):
#     Q1 = df[column].quantile(0.25)
#     Q3 = df[column].quantile(0.75)
#     IQR = Q3 - Q1
#     lower_bound = Q1 - 1.5 * IQR
#     upper_bound = Q3 + 1.5 * IQR
#     outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
#     print(f"[{column}] 이상치 개수: {len(outliers)}")
#     return outliers[['ID', column]]

# # 분석 대상 컬럼 리스트
# target_columns = ['할인금액_R3M', '혜택수혜금액']

# # 이상치 탐지 결과 저장
# outlier_results = {}

# # 각 컬럼별 이상치 확인
# for col in target_columns:
#     outliers = detect_outliers_iqr(df_all, col)
#     outlier_results[col] = outliers

# import seaborn as sns
# import matplotlib.pyplot as plt

# plt.figure(figsize=(15, 8))
# for i, col in enumerate(target_columns):
#     plt.subplot(2, 3, i+1)
#     sns.boxplot(x=df_all[col])
#     plt.title(col)
# plt.tight_layout()
# plt.show()

df_all.shape
# df_all.columns.tolist()
# df_all.dtypes
# df_all.head()

df_all.to_csv('df_all.csv', index=False, encoding='cp949')

import os
os.listdir()

from google.colab import files
files.download('df_all.csv')

# 결측치 확인
df_all.isna().sum()

# 데이터 샘플 추출
# 1. (선택) 데이터 샘플링: df_all에서 500개 샘플 추출
df_all_sample = df_all.sample(n=500, random_state=42)  # 또는 head(n)

# 2. CSV 파일로 저장 (인코딩은 Excel 호환 위해 cp949 사용)
df_all_sample.to_csv('df_all_sample.csv', index=False, encoding='cp949')

# 3. 로컬로 다운로드
from google.colab import files
files.download('df_all_sample.csv')

# 1. 컬럼명 확인
print(df_all_sample.columns.tolist())

# 2. 데이터 미리보기
print(df_all_sample.head(3))

# 수치형 변수만 선택
num_df = df_all.select_dtypes(include='number')

# 상관계수
plt.figure(figsize=(14, 10))
sns.heatmap(num_df.corr(), annot=False, cmap='coolwarm')
plt.title("수치형 변수 간 상관관계 Heatmap")
plt.show()







# 수치형 데이터만 다중공선성(VIF)계산
numeric_cols = df.select_dtypes(include='number')
vif_result = calculate_vif(numeric_cols)
print(vif_result)







# read parquet
df1 = pd.read_parquet('201807_train_청구정보.parquet')
df1.head()

df2 = pd.read_parquet('201808_train_청구정보.parquet')
df3 = pd.read_parquet('201809_train_청구정보.parquet')
df4 = pd.read_parquet('201810_train_청구정보.parquet')
df5 = pd.read_parquet('201811_train_청구정보.parquet')
df6 = pd.read_parquet('201812_train_청구정보.parquet')

# print('201807_train_청구정보.parquet')
# df1.isnull().sum()

# print('201808_train_청구정보.parquet')
# df2.isnull().sum()

# print('201809_train_청구정보.parquet')
# df3.isnull().sum()

# print('201810_train_청구정보.parquet')
# df4.isnull().sum()

# print('201811_train_청구정보.parquet')
# df5.isnull().sum()

# print('201812_train_청구정보.parquet')
# df6.isnull().sum()

print('201807_train_청구정보.parquet')
df1.info()
# print('201808_train_청구정보.parquet')
# df2.info()
# print('201809_train_청구정보.parquet')
# df3.info()
# print('201810_train_청구정보.parquet')
# df4.info()
# print('201811_train_청구정보.parquet')
# df5.info()
# print('201812_train_청구정보.parquet')
# df6.info()

df1.columns.tolist()

# 컬럼 제거
df11 = df1.drop(columns=['대표결제방법코드', '청구서발송여부_R3M', '청구금액_R3M', '포인트_마일리지_환산_B0M'], inplace=False)
print(df11.shape)
print(df11.head())























# parquet 파일 열기
df1 = pd.read_parquet("201807_train_청구정보.parquet")

# csv로 저장
df1.to_csv("201807_train_청구정보.csv", index=False)

# parquet 파일 열고 csv로 저장
df2 = pd.read_parquet("201807_train_청구정보.parquet")
df2.to_csv("201807_train_청구정보.csv", index=False)

df3 = pd.read_parquet("201807_train_청구정보.parquet")
df3.to_csv("201807_train_청구정보.csv", index=False)

df4 = pd.read_parquet("201807_train_청구정보.parquet")
df4.to_csv("201807_train_청구정보.csv", index=False)

df5 = pd.read_parquet("201807_train_청구정보.parquet")
df5.to_csv("201807_train_청구정보.csv", index=False)

df6 = pd.read_parquet("201807_train_청구정보.parquet")
df6.to_csv("201807_train_청구정보.csv", index=False)

