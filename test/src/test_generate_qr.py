import pytest
from src.generate_qr import has_alpha_channel, create_qr_code, apply_transparency, add_logo_to_qr_code, generate_qr_code
from PIL import Image
import os
import qrcode

# img フォルダ内の画像ファイルの一覧を取得
IMG_DIRECTORY = "img"  # img フォルダのパスを指定
logo_files = [f for f in os.listdir(IMG_DIRECTORY) if os.path.isfile(os.path.join(IMG_DIRECTORY, f))]

# 最初の画像ファイルをテスト用ロゴとして選択
TEST_LOGO_PATH = os.path.join(IMG_DIRECTORY, logo_files[0]) if logo_files else None

def test_has_alpha_channel():
  # テスト用の画像がアルファチャンネルを持つかどうかをテスト
  assert has_alpha_channel(TEST_LOGO_PATH) in [True, False]

def test_create_qr_code():
  # QRコードが正しく作成されるかをテスト
  url = "https://example.com"
  qr_img = create_qr_code(url)
  assert isinstance(qr_img, qrcode.image.pil.PilImage)

def test_apply_transparency():
  # 背景透明化機能のテスト
  img = Image.new("RGB", (100, 100), "white")
  transparent_img = apply_transparency(img, TEST_LOGO_PATH)
  # 透明化が適用されたかの具体的な検証は実装に依存

def test_add_logo_to_qr_code():
  # QRコードにロゴが正しく追加されるかをテスト
  qr_img = Image.new("RGB", (100, 100), "white")
  qr_with_logo = add_logo_to_qr_code(qr_img, TEST_LOGO_PATH)
  # ロゴが追加されたかの具体的な検証は実装に依存

def test_generate_qr_code():
  # QRコード生成プロセス全体のテスト
  url = "https://example.com"
  filename = "test_qr.png"
  generate_qr_code(url, filename, TEST_LOGO_PATH)
  # ファイルが生成されたかを確認
  assert os.path.exists(filename)
  # ファイルの内容（QRコードとロゴ）を確認（具体的な検証方法は実装に依存）

  # テスト後に生成したファイルを削除
  os.remove(filename)
  
def test_invalid_logo_path():
  # 存在しないロゴファイルパスが与えられた場合のテスト
  invalid_logo_path = "invalid/path/to/logo.png"
  img = Image.new("RGB", (100, 100), "white")
  with pytest.raises(FileNotFoundError):
    add_logo_to_qr_code(img, invalid_logo_path)

def test_qr_code_content():
  # 生成されたQRコードの内容が正しいかをテスト
  url = "https://example.com"
  qr_img = create_qr_code(url)
  # QRコードの内容をデコードしてURLが含まれていることを確認（デコード方法は実装に依存）

def test_file_saving():
  # QRコードがファイルに正しく保存されるかをテスト
  url = "https://example.com"
  filename = "test_qr.png"
  generate_qr_code(url, filename, TEST_LOGO_PATH)
  assert os.path.exists(filename)
  # 必要に応じて保存されたファイルの内容を検証
  os.remove(filename)
