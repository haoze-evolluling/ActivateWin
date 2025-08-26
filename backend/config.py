#!/usr/bin/env python3
"""
配置文件
"""

import os

# 服务配置
class Config:
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'activate-win-secret-key-2024'
    
    # 服务端口
    PORT = int(os.environ.get('PORT', 5000))
    
    # 调试模式
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = 'activation.log'
    
    # KMS配置
    KMS_SERVERS = [
        "kms.bige0.com",
        "kms.03k.org", 
        "kms.wxlost.com",
        "kms.moeyuuko.top",
        "kms.loli.best",
        "kms.loli.beer",
        "kms.cgtsoft.com",
        "kms.sixyin.com",
        "kms.litbear.cn"
    ]
    
    KMS_PORT = 1688
    KMS_TIMEOUT = 5
    
    # 激活配置
    MAX_RETRIES = 3
    RETRY_DELAY = 2
    
    # 历史记录配置
    HISTORY_FILE = 'activation_history.json'
    MAX_HISTORY_ITEMS = 100
    
    # CORS配置
    CORS_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'INFO'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}