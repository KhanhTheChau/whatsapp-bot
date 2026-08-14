import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Cấu hình tập trung cho toàn bộ ứng dụng."""
    
    WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
    PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "myka_secret_123")
    
    GEMINI_CONFIGS = [
        {
            "api_key": os.getenv("GEMINI_API_KEY_1"),
            "model_name": "gemini-3.5-flash-lite"
        },
        {
            "api_key": os.getenv("GEMINI_API_KEY_2"),
            "model_name": "gemini-3.6-flash"
        }
    ]
    
    # Lọc bỏ các cấu hình chưa có API key
    GEMINI_CONFIGS = [cfg for cfg in GEMINI_CONFIGS if cfg["api_key"]]

    @classmethod
    def validate(cls):
        """Kiểm tra và xác thực các cấu hình bắt buộc trước khi chạy ứng dụng."""
        if not cls.WHATSAPP_TOKEN:
            raise ValueError("Cảnh báo: Thiếu cấu hình WHATSAPP_TOKEN trong file .env")
        if not cls.PHONE_NUMBER_ID:
            raise ValueError("Cảnh báo: Thiếu cấu hình PHONE_NUMBER_ID trong file .env")
        if not cls.GEMINI_CONFIGS:
            raise ValueError("Cảnh báo: Cần cấu hình ít nhất một GEMINI_API_KEY_x trong file .env")
