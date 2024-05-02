import json
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

def generate_qr_code(data, file_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)

def read_qr_code(image):
    decoded_objects = decode(image)
    qr_contents = []
    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        qr_contents.append(json.loads(qr_data))
    return qr_contents
