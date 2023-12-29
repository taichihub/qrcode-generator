import os
import pandas as pd
from validate import validate_csv 

data_directory = 'data'

try:
  filenames = os.listdir(data_directory)
  for filename in filenames:
    if filename.endswith('.csv'):
      correct_file_path = os.path.join(data_directory, filename)
      validation_errors = validate_csv(correct_file_path) # バリデーションチェック
      correct_df = pd.read_csv(correct_file_path)
      if validation_errors:
        for error in validation_errors:
          print(error)
      else:
        print("ーーーーーーーーーーーーーーーーーーー")
        for index, row in correct_df.iterrows():
          print(f"ファイル名：{row['ファイル名']}, URL:{row['URL']}")
        print("ーーーーーーーーーーーーーーーーーーー")
except Exception as e:
  print(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
