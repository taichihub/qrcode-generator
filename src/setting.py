import qrcode
import os

DATA_DIRECTORY = "data"  # CSVファイルが格納されているディレクトリのパス
QR_CODE_DIRECTORY = "qr_code"  # 生成したQRコードを格納するディレクトリのパス
IMG_DIRECTORY = "img"  # ロゴ画像が格納されているディレクトリのパス
QR_CODE_FILES_PER_DIR = 1000  # デフォルトで1000件ごとにディレクトリを分割

if os.path.exists(IMG_DIRECTORY):
    logo_files = [
        f
        for f in os.listdir(IMG_DIRECTORY)
        if os.path.isfile(os.path.join(IMG_DIRECTORY, f))
    ]
else:
    logo_files = []
LOGO_PATH = (
    os.path.join(IMG_DIRECTORY, logo_files[0]) if logo_files else None
)  # img フォルダ内の最初の画像ファイルを検出して設定

# ーーーーーーーーーーQRコード生成のための設定定数ーーーーーーーーーー

# QRコードのバージョン
# QRコードのバージョンについて：https://www.qrcode.com/about/version.html
QR_VERSION = 1

# 25%のエラー訂正能力を持つレベル(Qレベル)
# エラー訂正レベルについて：https://www.mediaseek.co.jp/barcode/10908/#:~:text=QR%E3%82%B3%E3%83%BC%E3%83%89%E3%81%AB%E3%81%AF%E8%AA%A4%E3%82%8A,L%E3%81%A8%E3%81%AA%E3%81%A3%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99%E3%80%82
ERROR_CORRECTION_LEVEL = qrcode.constants.ERROR_CORRECT_Q

# ボックスサイズ(QRコードの大きさ)
BOX_SIZE = 10

# 境界線のサイズ(周りの白色)
BORDER_SIZE = 4

# QRコードの色（デフォルトは黒色, 黒：#000000）
QR_COLOR = "#000000"

# QRコードの背景色（デフォルトは白色, 白：#FFFFFF）
QR_BACKGROUND_COLOR = "#FFFFFF"

# True：背景透明化有効, False：背景透明化無効 (背景透過する場合はimgフォルダに透過済の画像を入れておく)
QR_BACKGROUND_TRANSPARENT = False
