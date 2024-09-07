import os
import pandas as pd
import logging
from src.validate import validate_csv
from src.generate_qr import generate_qr_code
from src.setting import DATA_DIRECTORY, QR_CODE_DIRECTORY, IMG_DIRECTORY, QR_CODE_FILES_PER_DIR
import argparse

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description='CSVファイルからQRコードを生成します。')
    parser.add_argument('-r', '--resume', type=int, default=1,
                        help='この行番号から処理を再開します (1-indexed)')
    parser.add_argument(
        '-n', '--number', action='store_true', help='ファイル名を番号に変更します')
    return parser.parse_args()


def get_logo_image_path(img_directory):
    if os.path.exists(img_directory):
        for file in os.listdir(img_directory):
            if file.lower().endswith(".png"):
                return os.path.join(img_directory, file)
    return None


def create_subfolder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"サブフォルダを作成しました: {path}")


def get_output_subfolder(base_folder, file_index):
    folder_number = (file_index // QR_CODE_FILES_PER_DIR +
                     1) * QR_CODE_FILES_PER_DIR
    subfolder = os.path.join(base_folder, str(folder_number))
    create_subfolder(subfolder)
    return subfolder


def process_csv_file(file_path, qr_code_directory, logo_image_path, start_row=1, chunk_size=1000, use_numbering=False):
    logger.info(
        f"{file_path}を元にQRコードの生成を開始します。開始行: {start_row}, チャンクサイズ: {chunk_size}")
    validation_errors = validate_csv(file_path)
    if validation_errors:
        for error in validation_errors:
            logger.error(error)
        return

    base_subfolder = os.path.join(
        qr_code_directory, os.path.splitext(os.path.basename(file_path))[0])
    create_subfolder(base_subfolder)

    row_counter = 0

    for chunk_index, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
        chunk_start = row_counter + 1
        chunk_end = row_counter + len(chunk)

        if chunk_end < start_row:
            row_counter = chunk_end
            continue

        logger.info(
            f"チャンク {chunk_index + 1} を処理中... 行: {chunk_start} 〜 {chunk_end}")

        for index, row in chunk.iterrows():
            row_counter += 1
            if row_counter < start_row:
                continue

            output_subfolder = get_output_subfolder(
                base_subfolder, row_counter)

            if use_numbering:
                qr_code_filename = os.path.join(
                    output_subfolder, f"{row_counter}.png")
            else:
                qr_code_filename = os.path.join(output_subfolder, row["ファイル名"])

            logger.info(
                f"QRコード生成中: 行番号 {row_counter}, ファイル名: {qr_code_filename}")
            generate_qr_code(row["URL"], qr_code_filename, logo_image_path)

    logger.info(f"{file_path}からQRコードの生成を完了しました。")


def process_all_csv_files(data_directory, qr_code_directory, img_directory, start_row=1, chunk_size=1000, use_numbering=False):
    try:
        logo_image_path = get_logo_image_path(img_directory)
        for filename in os.listdir(data_directory):
            if filename.endswith(".csv"):
                correct_file_path = os.path.join(data_directory, filename)
                process_csv_file(correct_file_path, qr_code_directory,
                                 logo_image_path, start_row, chunk_size, use_numbering)
                start_row = 1
    except Exception as e:
        logger.error("CSVファイルの読み込み中にエラーが発生しました:", exc_info=True)


if __name__ == "__main__":
    args = parse_args()
    logger.info("処理を開始します")
    process_all_csv_files(DATA_DIRECTORY, QR_CODE_DIRECTORY, IMG_DIRECTORY,
                          start_row=args.resume, chunk_size=1000, use_numbering=args.number)
    logger.info("処理が完了しました")
