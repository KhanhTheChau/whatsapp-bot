import itertools
from typing import Dict, List
import google.generativeai as genai
from app.config import Config
from app.core.logger import logger

class GeminiService:
    """Service xử lý tương tác với Google Gemini API."""
    
    SYSTEM_PROMPT = """Bạn là Myka, một trợ lý ảo AI cực kỳ thông minh, thân thiện và duyên dáng trên WhatsApp. 
Quy tắc trả lời của bạn:
1. Luôn xưng hô là "Myka" và gọi người dùng là "bạn" (hoặc xưng hô linh hoạt, lịch sự theo cách họ gọi).
2. Trả lời tự nhiên, mượt mà, mang cảm giác như một người bạn đang nhắn tin chứ không phải một cỗ máy khô khan.
3. Câu trả lời nên ngắn gọn, súc tích, dễ đọc, phù hợp với định dạng tin nhắn điện thoại. Thêm emoji một cách tinh tế.
4. Luôn sẵn sàng giúp đỡ với thái độ vui vẻ, tích cực và hiểu chuyện."""

    def __init__(self):
        self.config_cycler = itertools.cycle(Config.GEMINI_CONFIGS) if Config.GEMINI_CONFIGS else None
        # Dictionary lưu phiên chat in-memory: { "số_điện_thoại": [history_messages] }
        self.user_sessions: Dict[str, List] = {}

    def get_response(self, prompt: str, sender_phone: str, sender_name: str = "Bạn") -> str:
        """
        Gửi tin nhắn đến Gemini và nhận phản hồi.
        """
        if not self.config_cycler:
            logger.error("Chưa cấu hình GEMINI_API_KEY hợp lệ.")
            return "Xin lỗi, hiện tại Myka đang bảo trì kết nối hệ thống. Vui lòng quay lại sau nhé!"

        config = next(self.config_cycler)
        
        try:
            genai.configure(api_key=config["api_key"])
            model = genai.GenerativeModel(
                model_name=config["model_name"],
                system_instruction=self.SYSTEM_PROMPT
            )
            
            if sender_phone not in self.user_sessions:
                self.user_sessions[sender_phone] = []
                
            # Chỉ lấy 4 tin nhắn gần nhất để giữ context
            recent_history = self.user_sessions[sender_phone][-4:]
                
            chat = model.start_chat(history=recent_history)
            
            logger.info(f"[GEMINI] Dùng model {config['model_name']} để trả lời {sender_name} ({sender_phone}).")
            
            # Gắn tên người dùng vào tin nhắn
            enhanced_prompt = f"[{sender_name} đang nói]: {prompt}"
            response = chat.send_message(enhanced_prompt)
            
            # Cập nhật lịch sử session
            self.user_sessions[sender_phone] = chat.history[-4:]
            
            return response.text
            
        except Exception as e:
            logger.error(f"[GEMINI] Lỗi khi gọi API: {e}", exc_info=True)
            return "Xin lỗi, hiện tại Myka đang gặp chút sự cố khi suy nghĩ. Thử lại sau giúp Myka nha!"
