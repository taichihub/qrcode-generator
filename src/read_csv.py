import os
import pandas as pd
from validate import validate_csv
from generate_qr import generate_qr_code

data_directory = 'data' # CSVファイルを格納しているフォルダ
qr_code_directory = 'qr_code'  # QRコードを格納するフォルダ

try:
  filenames = os.listdir(data_directory)
  for filename in filenames:
    if filename.endswith('.csv'):
      correct_file_path = os.path.join(data_directory, filename)
      validation_errors = validate_csv(correct_file_path)
      if validation_errors:
        for error in validation_errors:
          print(error)
        continue  # バリデーションエラーがある場合は次のファイルへ
      correct_df = pd.read_csv(correct_file_path)
      subfolder_path = os.path.join(qr_code_directory, os.path.splitext(filename)[0]) # QRコードを保存するサブフォルダを作成
      if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
      for index, row in correct_df.iterrows():
        qr_code_filename = os.path.join(subfolder_path, row['ファイル名']) # QRコードをサブフォルダに保存
        generate_qr_code(row['URL'], qr_code_filename)
except Exception as e:
  print(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
