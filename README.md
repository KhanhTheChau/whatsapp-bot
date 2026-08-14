# WhatsApp Bot (Enterprise Standard)

Dự án WhatsApp Bot tích hợp trí tuệ nhân tạo (Google Gemini) để tự động trả lời tin nhắn từ người dùng. Dự án đã được tái cấu trúc theo chuẩn doanh nghiệp với mô hình service-oriented, sẵn sàng để mở rộng và triển khai (deployment).

## 📁 Cấu trúc thư mục

```text
whatsapp-bot/
├── app/
│   ├── __init__.py          # Khởi tạo Flask app (Application Factory)
│   ├── config.py            # Quản lý cấu hình biến môi trường
│   ├── core/
│   │   └── logger.py        # Cấu hình Logging
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # Định tuyến Webhook
│   └── services/
│       ├── __init__.py
│       ├── gemini.py        # Tích hợp Google Gemini AI
│       └── whatsapp.py      # Tích hợp WhatsApp Cloud API
├── main.py                  # Entry point
├── .env                     # Biến môi trường (Không được push lên git)
├── .gitignore               # Cấu hình bỏ qua các file nhạy cảm
└── requirements.txt         # Các thư viện phụ thuộc
```

## 🚀 Cài đặt & Chạy dự án

**Bước 1:** Cài đặt và tạo môi trường ảo (khuyến nghị).
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
```

**Bước 2:** Cài đặt các thư viện phụ thuộc.
```bash
pip install -r requirements.txt
```

**Bước 3:** Cấu hình file `.env`.
Hãy tạo một file `.env` ở thư mục gốc và cung cấp các thông số bắt buộc sau:
```env
WHATSAPP_TOKEN="<token_tu_meta>"
PHONE_NUMBER_ID="<id_so_dien_thoai_meta>"
VERIFY_TOKEN="<chuoi_ky_tu_xac_minh_webhook>"

# Bạn có thể cung cấp nhiều key để xoay vòng
GEMINI_API_KEY_1="<api_key_gemini_thu_1>"
GEMINI_API_KEY_2="<api_key_gemini_thu_2>"
```

**Bước 4:** Khởi động server.
```bash
python main.py
```
Server sẽ khởi chạy tại `http://0.0.0.0:5000`.

---

## 🌍 Hướng dẫn Triển khai Webhook

Để Meta (WhatsApp) có thể gọi Webhook của bạn, ứng dụng phải có địa chỉ khả dụng trên Internet (Public URL) và phải dùng giao thức `https`.

### 1. Môi trường Local (Dùng Ngrok)
Nếu bạn đang chạy code trên máy tính cá nhân, hãy dùng **Ngrok** để tạo đường dẫn ra Internet:

1. Tải và cài đặt [ngrok](https://ngrok.com/).
2. Khởi chạy app (`python main.py`) ở port `5000`.
3. Mở một cửa sổ Terminal khác và chạy:
   ```bash
   ngrok http 5000
   ```
4. Copy đường dẫn `Forwarding` có chữ `https` mà ngrok cấp (VD: `https://abc-123.ngrok-free.app`).
5. Dán URL này cộng thêm đuôi `/webhook` (VD: `https://abc-123.ngrok-free.app/webhook`) vào phần cấu hình Webhook trên trang Meta for Developers.

### 2. Môi trường Production (VPS/Server)
Để bot luôn sẵn sàng 24/7, bạn cần đưa nó lên một máy chủ thực tế (như VPS Ubuntu của AWS, DigitalOcean...):

1. Clone dự án về server và cài đặt các thư viện `requirements.txt`.
2. Không dùng `python main.py` ở production. Thay vào đó, hãy cài và dùng **Gunicorn** làm WSGI server:
   ```bash
   pip install gunicorn
   gunicorn --workers 4 --bind 0.0.0.0:5000 main:app
   ```
3. Khuyên dùng **systemd** hoặc **pm2** để giữ Gunicorn luôn chạy ngầm (daemon).
4. Cài đặt **Nginx** làm Reverse Proxy để trỏ domain/IP của server vào port `5000` của app.
5. Tạo chứng chỉ SSL bảo mật (dùng Certbot/Let's Encrypt miễn phí). Cập nhật URL Webhook mới với Meta.

## 🛠️ Công nghệ sử dụng
- **Python / Flask:** Framework phát triển backend nhẹ nhàng, hiệu năng.
- **Requests:** HTTP Client để giao tiếp gửi tin nhắn qua WhatsApp Graph API.
- **Google Generative AI:** Bộ não thông minh Gemini để trả lời hội thoại.
- **Logging:** Tiêu chuẩn hóa việc ghi nhận hoạt động và lỗi của ứng dụng.
