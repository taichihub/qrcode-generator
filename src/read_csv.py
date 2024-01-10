import os
import pandas as pd
import logging
from src.validate import validate_csv
from src.generate_qr import generate_qr_code

# Loggerの設定
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 定数の定義
DATA_DIRECTORY = "data"  # CSVファイルが格納されているディレクトリのパス
QR_CODE_DIRECTORY = "qr_code"  # 生成したQRコードを格納するディレクトリのパス
IMG_DIRECTORY = "img"  # ロゴ画像が格納されているディレクトリのパス


def get_logo_image_path(img_directory):
  # 指定されたディレクトリから最初に見つかったPNG画像のパスを返す。
  # PNG画像が存在しない場合は例外を発生させる。
  for file in os.listdir(img_directory):
    if file.lower().endswith(".png"):
      return os.path.join(img_directory, file)
  logger.error("imgフォルダに画像ファイルが見つかりませんでした。")
  raise Exception("imgフォルダに画像ファイルが見つかりませんでした。")


def create_subfolder(path):
  # 指定されたパスにサブフォルダを作成する。
  # フォルダが既に存在する場合は何もしない。
  if not os.path.exists(path):
    os.makedirs(path)


def process_csv_file(file_path, qr_code_directory, logo_image_path):
  # 指定されたCSVファイルを読み込み、QRコードの生成と保存を行う。
  validation_errors = validate_csv(file_path)
  if validation_errors:
    for error in validation_errors:
      logger.error(error)
    return

  df = pd.read_csv(file_path)
  subfolder_path = os.path.join(
      qr_code_directory, os.path.splitext(os.path.basename(file_path))[0]
  )
  create_subfolder(subfolder_path)

  for _, row in df.iterrows():
    qr_code_filename = os.path.join(subfolder_path, row["ファイル名"])
    generate_qr_code(row["URL"], qr_code_filename, logo_image_path)


if __name__ == "__main__":
  #ここ関数化する
  # ログ出す：かいし終了何のファイル読んだか生成したファイルの名前とか
  try:
    logo_image_path = get_logo_image_path(IMG_DIRECTORY)
    for filename in os.listdir(DATA_DIRECTORY):
      if filename.endswith(".csv"):
        correct_file_path = os.path.join(DATA_DIRECTORY, filename)
        process_csv_file(correct_file_path, QR_CODE_DIRECTORY, logo_image_path)
  except Exception as e:
    logger.error("CSVファイルの読み込み中にエラーが発生しました:", exc_info=True)
