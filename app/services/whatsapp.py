import requests
from typing import Optional
from app.config import Config
from app.core.logger import logger

class WhatsAppService:
    """Service xử lý các tác vụ liên quan đến WhatsApp API của Meta."""
    
    def __init__(self):
        self.token = Config.WHATSAPP_TOKEN
        self.phone_number_id = Config.PHONE_NUMBER_ID
        self.base_url = f"https://graph.facebook.com/v25.0/{self.phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def send_message(self, recipient_number: str, text_message: str) -> bool:
        """
        Gửi tin nhắn văn bản thông qua WhatsApp API.
        
        Args:
            recipient_number (str): Số điện thoại nhận tin (kèm mã quốc gia, VD: 849xxxxxxxx)
            text_message (str): Nội dung tin nhắn
            
        Returns:
            bool: True nếu thành công, False nếu thất bại.
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": "text",
            "text": {"body": text_message}
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=10)
            response.raise_for_status() 
            
            logger.info(f"Đã gửi tin nhắn thành công tới {recipient_number}. Status: {response.status_code}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Lỗi khi gửi tin nhắn tới {recipient_number}: {e}")
            if e.response is not None:
                logger.error(f"Phản hồi lỗi từ Meta: {e.response.text}")
            return False
