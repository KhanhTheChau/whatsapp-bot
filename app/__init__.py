from flask import Flask
from app.config import Config
from app.core.logger import logger

def create_app() -> Flask:
    """Application Factory pattern: Khởi tạo và cấu hình ứng dụng Flask."""
    
    # Kiểm tra biến môi trường
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Lỗi khởi động: {e}")
        raise
        
    app = Flask(__name__)
    
    # Đăng ký Blueprints (Routes)
    from app.api.routes import webhook_bp
    app.register_blueprint(webhook_bp)
    
    logger.info("Khởi tạo ứng dụng Flask thành công.")
    
    return app
