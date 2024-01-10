import os
import pandas as pd
from .validate import validate_csv
from .generate_qr import generate_qr_code

DATA_DIRECTORY = "data"  # CSVファイルを格納しているフォルダ
QR_CODE_DIRECTORY = "qr_code"  # QRコードを格納するフォルダ
IMG_DIRECTORY = "img"  # imgフォルダのパス


def get_logo_image_path(img_directory):
  for file in os.listdir(img_directory):
    if file.lower().endswith(".png"):
      return os.path.join(img_directory, file)
  raise Exception("imgフォルダに画像ファイルが見つかりませんでした。")


def create_subfolder(path):
  if not os.path.exists(path):
    os.makedirs(path)


def process_csv_file(file_path, qr_code_directory, logo_image_path):
  validation_errors = validate_csv(file_path)
  if validation_errors:
    for error in validation_errors:
      print(error)
    return

  df = pd.read_csv(file_path)
  subfolder_path = os.path.join(
      qr_code_directory, os.path.splitext(os.path.basename(file_path))[0]
  )
  create_subfolder(subfolder_path)

  for index, row in df.iterrows():
    qr_code_filename = os.path.join(subfolder_path, row["ファイル名"])
    generate_qr_code(row["URL"], qr_code_filename, logo_image_path)


if __name__ == "__main__":
  try:
    logo_image_path = get_logo_image_path(IMG_DIRECTORY)
    for filename in os.listdir(DATA_DIRECTORY):
      if filename.endswith(".csv"):
        correct_file_path = os.path.join(DATA_DIRECTORY, filename)
        process_csv_file(correct_file_path, QR_CODE_DIRECTORY, logo_image_path)
  except Exception as e:
    print(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
