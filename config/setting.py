import qrcode
import os
import re

# ーーーーーーーーーーープログラム内の設定定数ーーーーーーーーーーー

PROGRAM_SETTINGS = {
    "DIRECTORY": {
        "INPUT": "data",
        "OUTPUT": "qr_code",
        "IMG": "img"
    },
    "EXTENSION": {
        "IMG": ".png",
        "INPUT_FILE": ".csv"
    },
    "COLORS": {
        "WHITE_RGB": (255, 255, 255),
        "WHITE_RGBA_TRANSPARENT": (255, 255, 255, 0)
    },
    "MODES": {
        "ALPHA_CHANNEL": ("RGBA", "LA"),
        "RGBA": "RGBA"
    },
    "CSV_HEADER": {
        "LINES": "行数",
        "FILE_NAME": "ファイル名",
        "FILE_URL": "URL"
    },
    "RESUME_OPTION": {
        "SHORT":"-r",
        "LONG":"--resume"
    },
    "NUMBER_OPTION": {
        "SHORT":"-n",
        "LONG":"--number"
    },
    "QR_CODE_FILES_PER_DIR": 1000,
    "START_ROW": 1,
    "LOG_FILE_PATH": 'config/log_messages.yml',
    "ENCODING": 'utf-8',
    "ACTION": 'store_true',
    "FILE_MODE": 'r',
    "LOGGING_FORMAT": '%(asctime)s - %(levelname)s - %(message)s',
    "LOGO_PATH": None,
    "URL_PATTERN": re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        # domain...
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # ...or ipv4
        r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # ...or ipv6
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
      ),
}

img_directory = PROGRAM_SETTINGS["DIRECTORY"]["IMG"]
if os.path.exists(img_directory):
    logo_files = [
        f for f in os.listdir(img_directory) if os.path.isfile(os.path.join(img_directory, f)) and f.lower().endswith(PROGRAM_SETTINGS["EXTENSION"]["IMG"])
    ]
    if logo_files:
        PROGRAM_SETTINGS["LOGO_PATH"] = os.path.join(img_directory, logo_files[0])

# ーーーーーーーーーーQRコード生成のための設定定数ーーーーーーーーーー

QR_SETTINGS = {
    # QRコードのバージョン
    # QRコードのバージョンについて：https://www.qrcode.com/about/version.html
    "VERSION": 1,
    # 25%のエラー訂正能力（Qレベル）
    # エラー訂正レベルについて：https://www.mediaseek.co.jp/barcode/10908/#:~:text=QR%E3%82%B3%E3%83%BC%E3%83%89%E3%81%AB%E3%81%AF%E8%AA%A4%E3%82%8A,L%E3%81%A8%E3%81%AA%E3%81%A3%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99%E3%80%82
    "ERROR_CORRECTION_LEVEL": qrcode.constants.ERROR_CORRECT_Q,
    # ボックスサイズ（QRコードの大きさ）
    "BOX_SIZE": 10,
    # 境界線のサイズ（周りの白色）
    "BORDER_SIZE": 4,
    # QRコードの色（デフォルトは黒色, 黒：#000000）
    "COLOR": "#000000",
    # QRコードの背景色（デフォルトは白色, 白：#FFFFFF）
    "BACKGROUND_COLOR": "#FFFFFF",
    # True：背景透明化有効, False：背景透明化無効
    "BACKGROUND_TRANSPARENT": False 
}
