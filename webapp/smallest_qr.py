"""Backward-compatible wrapper module.

Prefer importing from services.qr_service but keep these for existing imports.
"""
from services.qr_service import (
    generate_qr_min_version as smallest_qr,  # returns (bytes, version)
    generate_qr_manual as manual_qr,         # returns bytes
    decode_qr as decode,
)


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

