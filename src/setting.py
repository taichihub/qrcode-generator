import qrcode

# QRコード生成のための設定定数
QR_VERSION = 1 # QRコードのバージョン
ERROR_CORRECTION_LEVEL = qrcode.constants.ERROR_CORRECT_L  # 7%のエラー訂正能力を持つレベル
BOX_SIZE = 10 # ボックスサイズ
BORDER_SIZE = 4 # 境界線のサイズ
QR_COLOR = "#000000" # QRコードの色（デフォルトは黒色, 黒：#000000）
QR_BACKGROUND_COLOR = "#FFFFFF" # QRコードの背景色（デフォルトは白色, 白：#FFFFFF）
QR_BACKGROUND_TRANSPARENT = True  # True：背景透明化有効, False：背景透明化無効
