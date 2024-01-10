import qrcode
import os

IMG_DIRECTORY = "img" # ロゴ画像が入っているフォルダ

# QRコード生成のための設定定数

QR_VERSION = 1 # QRコードのバージョン
ERROR_CORRECTION_LEVEL = qrcode.constants.ERROR_CORRECT_Q  # 25%のエラー訂正能力を持つレベル
# エラー訂正レベルの記事はる
BOX_SIZE = 10 # ボックスサイズ
BORDER_SIZE = 4 # 境界線のサイズ
QR_COLOR = "#000000" # QRコードの色（デフォルトは黒色, 黒：#000000）
QR_BACKGROUND_COLOR = "#FFFFFF" # QRコードの背景色（デフォルトは白色, 白：#FFFFFF）
QR_BACKGROUND_TRANSPARENT = False # True：背景透明化有効, False：背景透明化無効
logo_files = [f for f in os.listdir(IMG_DIRECTORY) if os.path.isfile(os.path.join(IMG_DIRECTORY, f))]
LOGO_PATH = os.path.join(IMG_DIRECTORY, logo_files[0]) if logo_files else None # img フォルダ内の最初の画像ファイルを検出して設定
