import pytest
import os
import pandas as pd
from src.read_csv import get_logo_image_path, create_subfolder, process_csv_file
from src.validate import validate_csv
from src.setting import DATA_DIRECTORY, QR_CODE_DIRECTORY, IMG_DIRECTORY
from src.test_common import skip_if_no_logo


def run_process_csv_file(csv_path, qr_code_directory, img_directory):
    if skip_if_no_logo:
        logo_image_path = get_logo_image_path(img_directory)
        process_csv_file(csv_path, qr_code_directory, logo_image_path)
    else:
        process_csv_file(csv_path, qr_code_directory, None)


@skip_if_no_logo
def test_get_logo_image_path():
    # imgフォルダからPNG画像ファイルのパスを取得する機能をテスト
    logo_path = get_logo_image_path(IMG_DIRECTORY)
    assert os.path.exists(logo_path) and logo_path.endswith(".png")


def test_create_subfolder():
    # サブフォルダを作成する機能をテスト
    subfolder_path = os.path.join(QR_CODE_DIRECTORY, "test_subfolder")
    create_subfolder(subfolder_path)
    assert os.path.exists(subfolder_path)
    os.rmdir(subfolder_path)  # テスト後にサブフォルダを削除


def test_process_csv_file():
    csv_files = [
        f
        for f in os.listdir(DATA_DIRECTORY)
        if f.lower().endswith(".csv") and os.path.isfile(os.path.join(DATA_DIRECTORY, f))
    ]
    if not csv_files:
        test_process_csv_file_empty()
    for csv_file in csv_files:
        test_csv_path = os.path.join(DATA_DIRECTORY, csv_file)
        run_process_csv_file(test_csv_path, QR_CODE_DIRECTORY, IMG_DIRECTORY)
        df = pd.read_csv(test_csv_path)
        subfolder_name = os.path.splitext(os.path.basename(test_csv_path))[0]
        use_numbering = False
        row_counter = 0

        for index, row in df.iterrows():
            row_counter += 1
            chunk_folder = ((row_counter // 1000) + 1) * 1000
            if use_numbering:
                qr_code_filename = os.path.join(
                    QR_CODE_DIRECTORY, subfolder_name, str(
                        chunk_folder), f"{row_counter}.png"
                )
            else:
                qr_code_filename = os.path.join(
                    QR_CODE_DIRECTORY, subfolder_name, str(
                        chunk_folder), row["ファイル名"]
                )
            assert os.path.exists(
                qr_code_filename
            ), f"QRコードファイル {qr_code_filename} が見つかりません"


def test_process_csv_file_empty():
    # CSVファイルが空の場合の挙動をテスト
    empty_csv_path = os.path.join(DATA_DIRECTORY, "empty.csv")
    # 空のCSVファイルを作成
    with open(empty_csv_path, "w") as f:
        pass
    run_process_csv_file(empty_csv_path, QR_CODE_DIRECTORY, IMG_DIRECTORY)
    # 処理が完了したら、期待するエラーメッセージが出力されていることを確認（例：ログファイルの確認など）
    os.remove(empty_csv_path)


# バリデーションの詳細テスト
def test_invalid_csv_data():
    invalid_csv_path = os.path.join(DATA_DIRECTORY, "invalid.csv")
    # 不正なデータを含むCSVファイルを作成
    with open(invalid_csv_path, "w") as f:
        f.write("不正なデータ")
    errors = validate_csv(invalid_csv_path)
    assert len(errors) > 0  # エラーがあることを確認
    os.remove(invalid_csv_path)


def test_no_png_in_img_directory():
    # 画像が見つからない場合に None が返ることを確認
    if not skip_if_no_logo:
        assert get_logo_image_path(IMG_DIRECTORY) is None
