#!/venv_py_flask/bin/env python3

import pyqrcode
import png
from PIL import Image
import io

def smallest_qr(link, error='L'):
  res = False
  im  = None
  i = 0
  while not res:
    try:
      assert type(link) == str, "Link must be a string"
      im = qr_from_link(link, version=i, error=error)
      print(f"Qr created with version: {i}")
      res = True
    except ValueError:
      i+=1
  return im, i


def manual_qr(link, version, error):
  try:
    assert type(link) == str, "Link must be a string"
    im = qr_from_link(link, version=version, error=error)
    err = None
  except ValueError as e:
    im = None
    err = e
  return im, err


def qr_from_link(link, version=None, error='L'):
  #inserting website name
  qr = pyqrcode.create(link, error=error, version=version)

  # Create a BytesIO object to store the binary representation in memory
  stream = io.BytesIO()

  # Save the QR code to the BytesIO object
  qr.png(stream, scale=100)  # You can choose a different scale if needed

  # Get the binary representation from the BytesIO object
  binary_qrcode = stream.getvalue()

  # Close the BytesIO stream
  stream.close()

  return binary_qrcode

def decode(img):
  from pyzbar.pyzbar import decode
  try:
    data = decode(Image.open(io.BytesIO(img)))
  except Exception as e:
    print(e)
    data = None
  
  return data[0].data.decode('utf-8') if data[0] else None


# #saving image
# # img = "qr-code.png"
# # url.png(img, scale=10)

# print(dir(url))
# print(url.data)
# print(url.encoding)
# print(url.xbm())  
# buffer = io.BytesIO()
# buffer.write(url.xbm())

# url.png(buffer)
# print("from src")
# print(buffer.read())
# #opening image
# # im=Image.open(img)

# #show
# return buffer

