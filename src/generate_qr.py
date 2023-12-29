import qrcode
from PIL import Image
from setting import QR_VERSION, ERROR_CORRECTION_LEVEL, BOX_SIZE, BORDER_SIZE, QR_COLOR, QR_BACKGROUND_COLOR, QR_BACKGROUND_TRANSPARENT

def generate_qr_code(url, filename):
  qr = qrcode.QRCode(
    version=QR_VERSION,
    error_correction=ERROR_CORRECTION_LEVEL,
    box_size=BOX_SIZE,
    border=BORDER_SIZE,
  )
  qr.add_data(url)
  qr.make(fit=True)

  if QR_BACKGROUND_TRANSPARENT:
    img = qr.make_image(fill_color=QR_COLOR)
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
      if item[0] == 255 and item[1] == 255 and item[2] == 255:  # 白色の部分（背景）を透明に
        newData.append((255, 255, 255, 0))
      else:
        newData.append(item)
    img.putdata(newData)
  else:
    img = qr.make_image(fill_color=QR_COLOR, back_color=QR_BACKGROUND_COLOR)

  img.save(filename)
