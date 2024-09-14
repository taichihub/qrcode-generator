import os
import pytest
from config.setting import PROGRAM_SETTINGS
from config.logging import LOG_MESSAGES, logger


# img フォルダ内の画像ファイルの一覧を取得
logo_files = [
    f
    for f in os.listdir(PROGRAM_SETTINGS["DIRECTORY"]["IMG"])
    if os.path.isfile(os.path.join(PROGRAM_SETTINGS["DIRECTORY"]["IMG"], f))
]


# 最初の画像ファイルをテスト用ロゴとして選択
test_logo_path = os.path.join(PROGRAM_SETTINGS["DIRECTORY"]["IMG"], logo_files[0]) if logo_files else None


# test_logo_path が存在しない場合、関連するテストをスキップ
skip_if_no_logo = pytest.mark.skipif(
    not test_logo_path, reason=LOG_MESSAGES["TEST_COMMON"]["SKIP_REASON"])
