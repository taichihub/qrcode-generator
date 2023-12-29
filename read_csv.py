import os
import pandas as pd

data_directory = 'data'

try:
  filenames = os.listdir(data_directory)
  
  for filename in filenames:
    if filename.endswith('.csv'):
      correct_file_path = os.path.join(data_directory, filename)
      correct_df = pd.read_csv(correct_file_path)
      print("ーーーーーーーーーーーーーーーーーーー")
      for index, row in correct_df.iterrows():
        print(f"ファイル名：{row['ファイル名']}, URL:{row['URL']}")
      print("ーーーーーーーーーーーーーーーーーーー")
  completed_message = "CSVファイルの読み込みが完了し、ログを出力しました。"
except Exception as e:
  completed_message = f"CSVファイルの読み込み中にエラーが発生しました: {e}"

print(completed_message)
