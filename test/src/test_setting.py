import pytest
import os
from src import setting  # `setting.py` が src ディレクトリ内にあることを前提とする
import qrcode


def test_logo_path():
  # `IMG_DIRECTORY` 内の画像ファイルのリストを取得
  logo_files = [
      f
      for f in os.listdir(setting.IMG_DIRECTORY)
      if os.path.isfile(os.path.join(setting.IMG_DIRECTORY, f))
  ]

  # 予想されるロゴファイルパスを設定（画像ファイルが存在する場合は最初のものを選択）
  expected_logo_path = (
      os.path.join(setting.IMG_DIRECTORY,
                   logo_files[0]) if logo_files else None
  )

  # `setting.py` に設定されたロゴファイルパスが予想されるパスと一致するかを確認
  assert setting.LOGO_PATH == expected_logo_path
