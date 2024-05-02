import json
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .utils import generate_qr_code, read_qr_code
import os 
import cv2
from PIL import Image
from datetime import datetime
from django.http import JsonResponse
from pyzbar.pyzbar import decode, ZBarSymbol
from django.http import StreamingHttpResponse

class QRView(TemplateView):
    template_name = 'myapp/qr.html'  # Chỉnh sửa tên template nếu cần

def generate_qr_view(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ request POST
        household_name = request.POST.get('household_name', '')
        phone_number = request.POST.get('phone_number', '')
        meter_code = request.POST.get('meter_code', '')
        current_number_water = request.POST.get('current_number_water', '')
        lastest_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Tạo dữ liệu JSON cho mã QR
        qr_data = {
            "household_name": household_name,
            "phone_number": phone_number,
            "meter_code": meter_code,
            "current_number_water": current_number_water,
            "lastest_updated": lastest_updated
        }

        # Chuyển đổi từ điển thành chuỗi JSON
        qr_json = json.dumps(qr_data)

        file_name = f"qr_{meter_code}.png"

        # Tạo đường dẫn đầy đủ cho tệp QR
        file_path = os.path.join(settings.BASE_DIR, 'static', 'images', file_name)

        # Tạo mã QR và lưu vào thư mục "static/images"
        generate_qr_code(qr_json, file_path)

        # Trả về đường dẫn tương đối của tệp QR để hiển thị trên giao diện
        qr_image_relative_path = os.path.join('images', file_name)
        return render(request, 'myapp/generate_qr_success.html', {'qr_image_relative_path': qr_image_relative_path, 'meter_code': meter_code})

    return render(request, 'myapp/generate_qr.html')


def read_qr_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        # Kiểm tra nếu là file hình ảnh
        if image_file.content_type.startswith('image'):
            # Mở hình ảnh và đọc mã QR
            image = Image.open(image_file)
            qr_contents = read_qr_code(image)
            
            # Trả về nội dung của mã QR dưới dạng JSON
            return JsonResponse(qr_contents, safe=False)

    return render(request, 'myapp/read_qr.html')

def generate_qr_data(request):
    # Khởi tạo webcam
    cap = cv2.VideoCapture("http://10.20.79.14:4747/video")

    decoder = ZBarSymbol.QRCODE 
    while True:
        # Đọc hình ảnh từ webcam
        ret, frame = cap.read()

        if ret:

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            qr_codes = decode(gray, symbols=[decoder])

            # Nếu có mã QR được đọc, gửi nó đến client
            if qr_codes:
                qr_contents = qr_codes[0].data.decode('utf-8')

                # Chuyển đổi chuỗi JSON thành một đối tượng Python
                qr_data = json.loads(qr_contents)

                return JsonResponse(qr_data)

def qr_streaming_view(request):
    # Trả về streaming response sử dụng generator function
    return StreamingHttpResponse(generate_qr_data())

def qr_display_view(request):
    return render(request, 'myapp/qr_display.html')