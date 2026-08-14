from app import create_app
from app.core.logger import logger

# Khởi tạo app
app = create_app()

if __name__ == '__main__':
    logger.info("Server WhatsApp Bot đang khởi động tại cổng 5000...")
    # Tắt debug mode để an toàn hơn cho môi trường doanh nghiệp
    app.run(host='0.0.0.0', port=5000, debug=False)