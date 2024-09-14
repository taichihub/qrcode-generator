import qrcode
import os
from PIL import Image
from config.setting import PROGRAM_SETTINGS, QR_SETTINGS


def has_alpha_channel(logo_path):
    # 指定された画像がアルファチャンネル（透明度）を持っているかどうかを判断する。
    # アルファチャンネルを持つ場合はTrueを、持っていない場合はFalseを返す。
    if logo_path is None or not os.path.exists(logo_path):
        return True  # 画像が存在しない場合はTrueを返す
    try:
        with Image.open(logo_path) as img:
            return img.mode in PROGRAM_SETTINGS["COLORS"]["ALPHA_CHANNEL"]
    except IOError:
        return False


def create_qr_code(url):
    # 指定されたURLからQRコードを生成する。
    # QRコードの設定値（バージョン、エラー訂正レベル、ボックスサイズ、境界線サイズ）はsrc.settingモジュールから取得される。
    qr = qrcode.QRCode(
        version=QR_SETTINGS["VERSION"],
        error_correction=QR_SETTINGS["ERROR_CORRECTION_LEVEL"],
        box_size=QR_SETTINGS["BOX_SIZE"],
        border=QR_SETTINGS["BORDER_SIZE"],
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color=QR_SETTINGS["COLOR"], back_color=QR_SETTINGS["BACKGROUND_COLOR"])


def apply_transparency(img, logo_path):
    # QRコード画像に透明化処理を適用する。
    # QR_BACKGROUND_TRANSPARENTがTrueの場合のみ実行される。
    if QR_SETTINGS["BACKGROUND_TRANSPARENT"] and has_alpha_channel(logo_path):
        img = img.convert(PROGRAM_SETTINGS["MODES"]["RGBA"])
        new_pixels = [
            (pixel if pixel[:3] != PROGRAM_SETTINGS["COLORS"]["WHITE_RGB"] else PROGRAM_SETTINGS["COLORS"]["WHITE_RGBA_TRANSPARENT"])
            for pixel in img.getdata()
        ]
        img.putdata(new_pixels)
    return img


def add_logo_to_qr_code(img, logo_path):
    # QRコード画像にロゴを追加する。
    # ロゴのサイズと配置位置は画像サイズに基づいて計算される。
    if logo_path:
        logo = Image.open(logo_path).convert(PROGRAM_SETTINGS["MODES"]["RGBA"])
        logo_size = int(min(img.size) * 0.25)
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
        box = (pos[0], pos[1], pos[0] + logo_size, pos[1] + logo_size)
        blank = Image.new(PROGRAM_SETTINGS["MODES"]["RGBA"], (logo_size, logo_size),PROGRAM_SETTINGS ["COLORS"]["WHITE_RGBA_TRANSPARENT"])
        img.paste(blank, box)
        mask = logo.split()[3]
        img.paste(logo, pos, mask=mask)
    return img


def is_img_folder_empty(img_directory):
    if os.path.exists(img_directory):
        return not any(
            f.lower().endswith(PROGRAM_SETTINGS["EXTENSION"]["IMG"]) and os.path.isfile(os.path.join(img_directory, f))
            for f in os.listdir(img_directory)
        )
    else:
        return False


def generate_qr_code(url, filename, logo_path):
    # URLからQRコードを生成し、ファイルに保存する。
    # 透明化処理とロゴの追加も行われる。
    img = create_qr_code(url)
    img = apply_transparency(img, logo_path)
    if not is_img_folder_empty(PROGRAM_SETTINGS["DIRECTORY"]["IMG"]):
        img = add_logo_to_qr_code(img, logo_path)
    img.save(filename)
