import os
import pandas as pd
import logging
from src.validate import validate_csv
from src.generate_qr import generate_qr_code
from src.setting import DATA_DIRECTORY, QR_CODE_DIRECTORY, IMG_DIRECTORY
import argparse

# Loggerの設定
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_args():
  # コマンドライン引数をパースする
  parser = argparse.ArgumentParser(description='CSVファイルからQRコードを生成します。')
  parser.add_argument('-r', '--resume', type=int, default=1, help='この行番号から処理を再開します (1-indexed)')
  return parser.parse_args()


def get_logo_image_path(img_directory):
  # 指定されたディレクトリから最初に見つかったPNG画像のパスを返す。
  if os.path.exists(img_directory):
    for file in os.listdir(img_directory):
      if file.lower().endswith(".png"):
        return os.path.join(img_directory, file)
  return None


def create_subfolder(path):
  # 指定されたパスにサブフォルダを作成する。
  # フォルダが既に存在する場合は何もしない。
  if not os.path.exists(path):
    os.makedirs(path)
    logger.info(f"サブフォルダを作成しました: {path}")


def process_csv_file(file_path, qr_code_directory, logo_image_path, start_row=1, chunk_size=1000):
  logger.info(f"{file_path}を元にQRコードの生成を開始します。開始行: {start_row}, チャンクサイズ: {chunk_size}")
  validation_errors = validate_csv(file_path)
  if validation_errors:
    for error in validation_errors:
      logger.error(error)
    return

  subfolder_path = os.path.join(
    qr_code_directory, os.path.splitext(os.path.basename(file_path))[0]
  )
  create_subfolder(subfolder_path)

  # 1-indexedから0-indexedに変換
  chunk_start_index = (start_row - 1) // chunk_size  # 開始行がどのチャンクに含まれるか計算
  row_counter = (start_row - 1)  # 実際の行番号の追跡

  for chunk_index, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
    if chunk_index < chunk_start_index:
      continue  # 開始行のチャンクまでスキップ

    chunk_start = chunk_index * chunk_size + 1
    chunk_end = chunk_start + len(chunk) - 1
    logger.info(f"チャンク {chunk_index + 1} を処理中... 行: {chunk_start} 〜 {chunk_end}")

    for index, row in chunk.iterrows():
      row_counter += 1
      if row_counter < start_row:
        continue

      qr_code_filename = os.path.join(subfolder_path, row["ファイル名"])
      logger.info(f"QRコード生成中: 行番号 {row_counter}, ファイル名: {qr_code_filename}")
      generate_qr_code(row["URL"], qr_code_filename, logo_image_path)

  logger.info(f"{file_path}からQRコードの生成を完了しました。")


def process_all_csv_files(data_directory, qr_code_directory, img_directory, start_row=1, chunk_size=1000):
  try:
    logo_image_path = get_logo_image_path(img_directory)
    for filename in os.listdir(data_directory):
      if filename.endswith(".csv"):
        correct_file_path = os.path.join(data_directory, filename)
        process_csv_file(correct_file_path, qr_code_directory, logo_image_path, start_row, chunk_size)
        start_row = 1  # 初回のファイル以後は1から開始する
  except Exception as e:
    logger.error("CSVファイルの読み込み中にエラーが発生しました:", exc_info=True)


if __name__ == "__main__":
  args = parse_args()
  logger.info("処理を開始します")
  process_all_csv_files(DATA_DIRECTORY, QR_CODE_DIRECTORY, IMG_DIRECTORY, args.resume)
  logger.info("処理が完了しました")
