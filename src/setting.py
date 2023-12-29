import qrcode

# QRコード生成のための設定定数
QR_VERSION = 1 # QRコードのバージョン
ERROR_CORRECTION_LEVEL = qrcode.constants.ERROR_CORRECT_L  # 7%のエラー訂正能力を持つレベル
BOX_SIZE = 10 # ボックスサイズ
BORDER_SIZE = 4 # 境界線のサイズ
