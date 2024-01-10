import qrcode
from PIL import Image
from .setting import (
    QR_VERSION,
    ERROR_CORRECTION_LEVEL,
    BOX_SIZE,
    BORDER_SIZE,
    QR_COLOR,
    QR_BACKGROUND_COLOR,
    QR_BACKGROUND_TRANSPARENT,
    LOGO_PATH,
)


def has_alpha_channel(logo_path):
  try:
    with Image.open(logo_path) as img:
      return img.mode in ("RGBA", "LA")
  except IOError:
    return False


def create_qr_code(url):
  qr = qrcode.QRCode(
      version=QR_VERSION,
      error_correction=ERROR_CORRECTION_LEVEL,
      box_size=BOX_SIZE,
      border=BORDER_SIZE,
  )
  qr.add_data(url)
  qr.make(fit=True)
  return qr.make_image(fill_color=QR_COLOR, back_color=QR_BACKGROUND_COLOR)


def apply_transparency(img, logo_path):
  if QR_BACKGROUND_TRANSPARENT and has_alpha_channel(logo_path):
    img = img.convert("RGBA")
    new_pixels = [
        (pixel if pixel[:3] != (255, 255, 255) else (255, 255, 255, 0))
        for pixel in img.getdata()
    ]
    img.putdata(new_pixels)
  return img


def add_logo_to_qr_code(img, logo_path):
  if logo_path:
    logo = Image.open(logo_path).convert("RGBA")
    logo_size = int(min(img.size) * 0.25)
    logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)
    pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
    box = (pos[0], pos[1], pos[0] + logo_size, pos[1] + logo_size)
    blank = Image.new("RGBA", (logo_size, logo_size), (255, 255, 255, 0))
    img.paste(blank, box)
    mask = logo.split()[3]
    img.paste(logo, pos, mask=mask)
  return img


def generate_qr_code(url, filename, logo_path):
  img = create_qr_code(url)
  img = apply_transparency(img, logo_path)
  img = add_logo_to_qr_code(img, logo_path)
  img.save(filename)
