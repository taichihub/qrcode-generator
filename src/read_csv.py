import os
import pandas as pd
import logging
from src.validate import validate_csv
from src.generate_qr import generate_qr_code
from src.setting import DATA_DIRECTORY, QR_CODE_DIRECTORY, IMG_DIRECTORY

# Loggerの設定
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_logo_image_path(img_directory):
  # 指定されたディレクトリから最初に見つかったPNG画像のパスを返す。
  for file in os.listdir(img_directory):
    if file.lower().endswith(".png"):
      return os.path.join(img_directory, file)
  return None


def create_subfolder(path):
  # 指定されたパスにサブフォルダを作成する。
  # フォルダが既に存在する場合は何もしない。
  if not os.path.exists(path):
    os.makedirs(path)


def process_csv_file(file_path, qr_code_directory, logo_image_path):
  logger.info(f"右記のCSVファイルを元にQRコードの生成を開始します: {file_path}")
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

  for index, row in df.iterrows():
    qr_code_filename = os.path.join(subfolder_path, row["ファイル名"])
    logger.info(f"QRコード生成 :  {index + 1} / {len(df)}")
    generate_qr_code(row["URL"], qr_code_filename, logo_image_path)
  logger.info(f"右記のCSVファイルを元にQRコードの生成が完了しました: {file_path}")


def process_all_csv_files(data_directory, qr_code_directory, img_directory):
  try:
    logo_image_path = get_logo_image_path(img_directory)
    for filename in os.listdir(data_directory):
      if filename.endswith(".csv"):
        correct_file_path = os.path.join(data_directory, filename)
        process_csv_file(correct_file_path, qr_code_directory, logo_image_path)
  except Exception as e:
    logger.error("CSVファイルの読み込み中にエラーが発生しました:", exc_info=True)


if __name__ == "__main__":
  logger.info("実行開始")
  process_all_csv_files(DATA_DIRECTORY, QR_CODE_DIRECTORY, IMG_DIRECTORY)
  logger.info("実行終了")
