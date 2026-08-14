import logging
import sys

def setup_logger() -> logging.Logger:
    """Cấu hình và khởi tạo Logger tiêu chuẩn cho ứng dụng."""
    logger = logging.getLogger("whatsapp_bot")
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Ghi log ra console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Định dạng log (Format) bao gồm: Time - Logger Name - Level - Message
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        
    return logger

logger = setup_logger()
