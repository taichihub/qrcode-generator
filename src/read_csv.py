if __name__=='__main__':
  
  import os
  import pandas as pd
  from validate import validate_csv
  from generate_qr import generate_qr_code

  DATA_DIRECTORY = 'data' # CSVファイルを格納しているフォルダ
  QR_CODE_DIRECTORY = 'qr_code'  # QRコードを格納するフォルダ
  IMG_DIRECTORY = 'img'  # imgフォルダのパス

  # imgフォルダ内の最初の画像ファイルのパスを取得
  logo_image_path = None
  for file in os.listdir(IMG_DIRECTORY):
    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
      logo_image_path = os.path.join(IMG_DIRECTORY, file)
      break

  if logo_image_path is None:
    raise Exception("imgフォルダに画像ファイルが見つかりませんでした。")

  try:
    filenames = os.listdir(DATA_DIRECTORY)
    for filename in filenames:
      if filename.endswith('.csv'):
        correct_file_path = os.path.join(DATA_DIRECTORY, filename)
        validation_errors = validate_csv(correct_file_path)
        if validation_errors:
          for error in validation_errors:
            print(error)
          continue  # バリデーションエラーがある場合は次のファイルへ
        correct_df = pd.read_csv(correct_file_path)
        subfolder_path = os.path.join(QR_CODE_DIRECTORY, os.path.splitext(filename)[0]) # QRコードを保存するサブフォルダを作成
        if not os.path.exists(subfolder_path):
          os.makedirs(subfolder_path)
        for index, row in correct_df.iterrows():
          qr_code_filename = os.path.join(subfolder_path, row['ファイル名']) # QRコードをサブフォルダに保存
          generate_qr_code(row['URL'], qr_code_filename, logo_image_path)  # ここでロゴのパスを渡す
  except Exception as e:
    print(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
