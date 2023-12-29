import qrcode
from PIL import Image
from setting import QR_VERSION, ERROR_CORRECTION_LEVEL, BOX_SIZE, BORDER_SIZE

def generate_qr_code(url, filename):
  qr = qrcode.QRCode(
    version=QR_VERSION,
    error_correction=ERROR_CORRECTION_LEVEL,
    box_size=BOX_SIZE,
    border=BORDER_SIZE,
  )
  qr.add_data(url)
  qr.make(fit=True)
  img = qr.make_image(fill_color="black", back_color="white")
  img.save(filename)
