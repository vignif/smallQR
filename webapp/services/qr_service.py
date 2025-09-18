"""QR generation & decoding logic isolated from Flask layer."""
from __future__ import annotations
import io
from typing import Optional, Tuple
import pyqrcode
from PIL import Image
from pyzbar.pyzbar import decode as zbar_decode


def generate_qr_min_version(data: str, error_level: str = "L") -> Tuple[bytes, int]:
    """Find the minimal QR version able to encode data.

    Iterates versions 1..40; raises ValueError if none fit.
    Returns raw PNG bytes and the version used.
    """
    if not isinstance(data, str):  # defensive
        raise TypeError("data must be a string")

    for version in range(1, 41):
        try:
            return _build_qr_bytes(data, error_level, version), version
        except ValueError:
            continue
    raise ValueError("Unable to encode data within version 1-40 constraints")


def generate_qr_manual(data: str, version: int, error_level: str = "L") -> bytes:
    if not (1 <= version <= 40):
        raise ValueError("version must be between 1 and 40")
    return _build_qr_bytes(data, error_level, version)


def _build_qr_bytes(data: str, error_level: str, version: int | None) -> bytes:
    qr = pyqrcode.create(data, error=error_level, version=version)
    buffer = io.BytesIO()
    # scale kept moderate to avoid huge memory use; front-end scales down naturally
    qr.png(buffer, scale=8)
    return buffer.getvalue()


def decode_qr(png_bytes: bytes) -> Optional[str]:
    try:
        img = Image.open(io.BytesIO(png_bytes))
        result = zbar_decode(img)
        if result:
            return result[0].data.decode("utf-8")
    except Exception:
        return None
    return None
