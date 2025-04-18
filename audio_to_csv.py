# 음성 데이터를 OpenSMILE을 사용하여 CSV 파일로 변환
import opensmile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def extract_features(audio_path):
    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals,
    )
    features = smile.process_file(audio_path)
    # print(smile.feature_names)
    return features

def save_to_csv(row_list):
    # 기존 CSV의 열 순서를 가져옴
    columns = pd.read_csv("dataset.csv", nrows=1).columns.tolist()
    
    new_df = pd.DataFrame(row_list, columns=columns)
    # print(f"new_df확인 : {new_df}")
    new_df.to_csv("dataset.csv", mode='a', index=False, header=False)

data_path = r"C:\Users\wnthd\Downloads\emotion_set"

# data_path 경로에서 '5차년도.csv' 파일 읽기
df = pd.read_csv(os.path.join(data_path, "5차년도_2차.csv"), encoding='cp949')

count = 0
row_list = []
for index, row in df.iterrows():
    wav_id = str(row['wav_id'])
    situation = str(row['상황'])

    # data_path/situation 폴더에 접근
    folder_path = os.path.join(data_path, "5차년도_2차")
    audio_path = os.path.join(folder_path, wav_id + ".wav")
    
    # audio_path가 있는지 확인, 있다면 특징 추출
    if os.path.exists(audio_path):
        # 음성 파일에서 특징 추출
        features = extract_features(audio_path)
        features_values = features.values.flatten().tolist()
        new_row = [situation] + features_values
        row_list.append(new_row)
        # print("row_list 확인: ", row_list)
        
        # dataset = pd.read_csv("dataset.csv", encoding='cp949')

        count += 1
        print(f"{count}번째 음성 파일 처리 완료")
    else:
        print(f"File not found: {audio_path}")

print("======처리 완료======")

save_to_csv(row_list)
