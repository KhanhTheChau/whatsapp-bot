from flask import Blueprint, request, jsonify
from app.config import Config
from app.core.logger import logger
from app.services.whatsapp import WhatsAppService
from app.services.gemini import GeminiService

webhook_bp = Blueprint('webhook_bp', __name__)

# Khởi tạo các services
whatsapp_service = WhatsAppService()
gemini_service = GeminiService()

@webhook_bp.route('/webhook', methods=['GET'])
def verify_webhook():
    """1. Xác minh Webhook từ Meta."""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == Config.VERIFY_TOKEN:
        logger.info("Xác minh Webhook Meta thành công.")
        return challenge, 200
    
    logger.warning("Xác minh Webhook Meta thất bại.")
    return "Xác minh thất bại", 403

@webhook_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    """2. Nhận và xử lý tin nhắn từ người dùng."""
    data = request.json

    try:
        for entry in data.get('entry', []):
            for change in entry.get('changes', []):
                value = change.get('value', {})
                if 'messages' in value:
                    message_info = value['messages'][0]
                    sender_phone = message_info.get('from')
                    
                    if message_info.get('type') == 'text':
                        incoming_text = message_info['text']['body']
                        
                        sender_name = "Bạn"
                        if 'contacts' in value and len(value['contacts']) > 0:
                            sender_name = value['contacts'][0].get('profile', {}).get('name', 'Bạn')
                            
                        logger.info(f"Nhận tin từ {sender_name} ({sender_phone}): {incoming_text}")
                        
                        reply_text = gemini_service.get_response(incoming_text, sender_phone, sender_name)
                        whatsapp_service.send_message(sender_phone, reply_text)
                    else:
                        logger.info(f"Bỏ qua loại tin nhắn không phải text: {message_info.get('type')}")
                        
    except Exception as e:
        logger.error(f"Lỗi xử lý payload Webhook: {e}", exc_info=True)
        
    return jsonify({"status": "ok"}), 200
