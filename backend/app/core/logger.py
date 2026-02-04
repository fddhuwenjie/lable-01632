"""
结构化日志模块
"""
import logging
import sys
from datetime import datetime
from typing import Any
import json


class JsonFormatter(logging.Formatter):
    """JSON格式日志"""
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # 添加额外字段
        if hasattr(record, "extra_data"):
            log_data["data"] = record.extra_data
            
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_data, ensure_ascii=False)


class ColorFormatter(logging.Formatter):
    """彩色控制台日志"""
    COLORS = {
        "DEBUG": "\033[36m",    # 青色
        "INFO": "\033[32m",     # 绿色
        "WARNING": "\033[33m",  # 黄色
        "ERROR": "\033[31m",    # 红色
        "CRITICAL": "\033[35m", # 紫色
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"{color}[{timestamp}] {record.levelname:8}{self.RESET} | {record.module}:{record.funcName}:{record.lineno} - {record.getMessage()}"
        
        if hasattr(record, "extra_data"):
            message += f" | {record.extra_data}"
            
        if record.exc_info:
            message += f"\n{self.formatException(record.exc_info)}"
            
        return message


def setup_logger(name: str = "app", level: str = "INFO", json_format: bool = False) -> logging.Logger:
    """配置日志器"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # 清除已有处理器
    logger.handlers.clear()
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    if json_format:
        console_handler.setFormatter(JsonFormatter())
    else:
        console_handler.setFormatter(ColorFormatter())
    
    logger.addHandler(console_handler)
    logger.propagate = False
    
    return logger


# 全局日志实例
logger = setup_logger("blog")


def log_info(message: str, **kwargs: Any) -> None:
    """记录信息日志"""
    record = logger.makeRecord(
        logger.name, logging.INFO, "", 0, message, (), None
    )
    if kwargs:
        record.extra_data = kwargs
    logger.handle(record)


def log_error(message: str, exc: Exception = None, **kwargs: Any) -> None:
    """记录错误日志"""
    logger.error(message, exc_info=exc, extra={"extra_data": kwargs} if kwargs else None)


def log_warning(message: str, **kwargs: Any) -> None:
    """记录警告日志"""
    record = logger.makeRecord(
        logger.name, logging.WARNING, "", 0, message, (), None
    )
    if kwargs:
        record.extra_data = kwargs
    logger.handle(record)


def log_debug(message: str, **kwargs: Any) -> None:
    """记录调试日志"""
    record = logger.makeRecord(
        logger.name, logging.DEBUG, "", 0, message, (), None
    )
    if kwargs:
        record.extra_data = kwargs
    logger.handle(record)
