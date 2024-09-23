import pytest
import os
from config.setting import PROGRAM_SETTINGS
import qrcode


def test_logo_path():
    # `IMG_DIRECTORY` 内の画像ファイルのリストを取得
    logo_files = [
        f
        for f in os.listdir(PROGRAM_SETTINGS["DIRECTORY"]["IMG"])
        if os.path.isfile(os.path.join(PROGRAM_SETTINGS["DIRECTORY"]["IMG"], f))
    ]

    # 予想されるロゴファイルパスを設定（画像ファイルが存在する場合は最初のものを選択）
    expected_logo_path = (
        os.path.join(PROGRAM_SETTINGS["DIRECTORY"]["IMG"],
                     logo_files[0]) if logo_files else None
    )

    # `setting.py` に設定されたロゴファイルパスが予想されるパスと一致するかを確認
    assert PROGRAM_SETTINGS["LOGO_PATH"] == expected_logo_path
