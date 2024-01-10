import pytest
import os
import pandas as pd
from src.read_csv import get_logo_image_path, create_subfolder, process_csv_file
from src.validate import validate_csv

# テスト用の定数
DATA_DIRECTORY = 'data'  # テスト用のCSVファイルが格納されるディレクトリ
QR_CODE_DIRECTORY = 'qr_code'  # テスト用QRコードを保存するディレクトリ
IMG_DIRECTORY = 'img'  # テスト用の画像ファイルが格納されるディレクトリ

def test_get_logo_image_path():
  # imgフォルダからPNG画像ファイルのパスを取得する機能をテスト
  logo_path = get_logo_image_path(IMG_DIRECTORY)
  assert os.path.exists(logo_path) and logo_path.endswith('.png')

def test_create_subfolder():
  # サブフォルダを作成する機能をテスト
  subfolder_path = os.path.join(QR_CODE_DIRECTORY, 'test_subfolder')
  create_subfolder(subfolder_path)
  assert os.path.exists(subfolder_path)
  os.rmdir(subfolder_path)  # テスト後にサブフォルダを削除

def test_process_csv_file():
  # CSVファイルを処理してQRコードを生成するプロセスをテスト
  test_csv_path = os.path.join(DATA_DIRECTORY, 'test_data.csv')  # テスト用のCSVファイルパス
  logo_image_path = get_logo_image_path(IMG_DIRECTORY)
  process_csv_file(test_csv_path, QR_CODE_DIRECTORY, logo_image_path)

  # 生成されたQRコードファイルの存在を確認
  df = pd.read_csv(test_csv_path)
  subfolder_name = os.path.splitext(os.path.basename(test_csv_path))[0]  # CSVファイル名から拡張子を除いたもの
  for index, row in df.iterrows():
    qr_code_filename = os.path.join(QR_CODE_DIRECTORY, subfolder_name, row['ファイル名'])
    assert os.path.exists(qr_code_filename), f"QRコードファイル {qr_code_filename} が見つかりません"

def test_process_csv_file_not_exists():
  # CSVファイルが存在しない場合の挙動をテスト
  test_csv_path = 'nonexistent.csv'
  logo_image_path = get_logo_image_path(IMG_DIRECTORY)
  process_csv_file(test_csv_path, QR_CODE_DIRECTORY, logo_image_path)
  # 処理が完了したら、期待するエラーメッセージが出力されていることを確認（例：ログファイルの確認など）

def test_process_csv_file_empty():
  # CSVファイルが空の場合の挙動をテスト
  empty_csv_path = os.path.join(DATA_DIRECTORY, 'empty.csv')
  # 空のCSVファイルを作成
  with open(empty_csv_path, 'w') as f:
    pass
  logo_image_path = get_logo_image_path(IMG_DIRECTORY)
  process_csv_file(empty_csv_path, QR_CODE_DIRECTORY, logo_image_path)
  # 処理が完了したら、期待するエラーメッセージが出力されていることを確認（例：ログファイルの確認など）
  os.remove(empty_csv_path)

# バリデーションの詳細テスト
def test_invalid_csv_data():
  invalid_csv_path = os.path.join(DATA_DIRECTORY, 'invalid.csv')
  # 不正なデータを含むCSVファイルを作成
  with open(invalid_csv_path, 'w') as f:
    f.write('不正なデータ')
  errors = validate_csv(invalid_csv_path)
  assert len(errors) > 0  # エラーがあることを確認
  os.remove(invalid_csv_path)

# img フォルダにPNG画像が存在しない場合のテスト
def test_no_png_in_img_directory():
  # 一時的にimgフォルダを空にする
  saved_files = [f for f in os.listdir(IMG_DIRECTORY) if f.endswith('.png')]
  for f in saved_files:
    os.rename(os.path.join(IMG_DIRECTORY, f), os.path.join(IMG_DIRECTORY, f + '.bak'))
  with pytest.raises(Exception):
    get_logo_image_path(IMG_DIRECTORY)
  # 元に戻す
  for f in saved_files:
    os.rename(os.path.join(IMG_DIRECTORY, f + '.bak'), os.path.join(IMG_DIRECTORY, f))
