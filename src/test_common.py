import os
import pytest
from src.setting import IMG_DIRECTORY

# img フォルダ内の画像ファイルの一覧を取得
logo_files = [
    f
    for f in os.listdir(IMG_DIRECTORY)
    if os.path.isfile(os.path.join(IMG_DIRECTORY, f))
]

# 最初の画像ファイルをテスト用ロゴとして選択
TEST_LOGO_PATH = os.path.join(
    IMG_DIRECTORY, logo_files[0]) if logo_files else None

# TEST_LOGO_PATH が存在しない場合、関連するテストをスキップ
skip_if_no_logo = pytest.mark.skipif(
    not TEST_LOGO_PATH, reason="imgフォルダに画像ファイルが存在しません")
