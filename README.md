# ActivateWin - Windows激活工具

一个现代化的Windows激活工具，提供简洁的Web界面和强大的后端服务，支持KMS激活和状态管理。

## ✨ 功能特性

- **🎯 一键激活**: 自动检测系统版本并选择合适的KMS服务器
- **📊 状态监控**: 实时查看Windows激活状态
- **🌐 KMS管理**: 支持自定义KMS服务器和端口
- **📱 响应式设计**: 支持桌面和移动设备
- **🔒 安全可靠**: 本地运行，无需联网
- **📈 历史记录**: 记录激活历史

## 🚀 快速开始

### 一键安装

1. 以管理员身份运行 `install.bat`
2. 安装完成后，双击桌面快捷方式或运行 `start-all.bat`
3. 打开浏览器访问: http://localhost:8000

### 手动安装

#### 1. 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 2. 启动后端服务

```bash
cd backend
python run.py --host 0.0.0.0 --port 5000
```

#### 3. 启动前端服务

```bash
cd webui
python -m http.server 8000
```

## 📋 使用说明

### 自动激活

1. 打开 http://localhost:8000
2. 点击"开始激活"
3. 选择Windows版本（可选）
4. 等待激活完成

### 手动配置KMS

1. 切换到"设置"标签页
2. 输入KMS服务器地址和端口
3. 点击"测试KMS服务器"验证连接
4. 返回"激活"标签页进行激活

### 检查激活状态

1. 切换到"状态"标签页
2. 点击"检查状态"获取当前激活信息
3. 查看详细的产品ID、许可证状态等信息

## 🔧 系统要求

- **操作系统**: Windows 7/8/10/11 (需要管理员权限)
- **Python**: 3.7 或更高版本
- **网络**: 需要连接KMS服务器（可配置）

## 📁 项目结构

```
ActivateWin/
├── backend/                 # 后端服务
│   ├── app.py              # 主应用
│   ├── config.py           # 配置文件
│   ├── utils.py            # 工具模块
│   ├── run.py              # 启动脚本
│   └── requirements.txt    # Python依赖
├── webui/                  # 前端界面
│   ├── index.html          # 主页面
│   ├── styles.css          # 样式文件
│   ├── script.js           # 前端逻辑
│   └── api-client.js       # API客户端
├── doc/                    # 文档
├── pic/                    # 图标和图片
├── install.bat            # 安装脚本
├── start-all.bat          # 一键启动
└── README.md              # 说明文档
```

## 🔧 API接口

### 系统状态
- `GET /api/status` - 获取激活状态
- `GET /api/system/info` - 获取系统信息

### 激活功能
- `POST /api/activate` - 自动激活Windows
- `POST /api/activation/manual` - 手动激活步骤

### KMS管理
- `GET /api/kms/servers` - 获取KMS服务器列表
- `POST /api/kms/test` - 测试KMS服务器连接

### 数据管理
- `GET /api/keys` - 获取GVLK密钥列表
- `GET /api/history` - 获取激活历史

## ⚡ 高级配置

### 自定义KMS服务器

在`backend/config.py`中添加或修改KMS服务器列表：

```python
KMS_SERVERS = [
    "your-kms-server.com",
    "another-kms-server.com",
]
```

### 环境变量

- `PORT` - 服务端口（默认5000）
- `DEBUG` - 调试模式（true/false）
- `LOG_LEVEL` - 日志级别（DEBUG/INFO/WARNING/ERROR）

## 🛡️ 安全说明

- 本工具仅在本地运行，不会上传任何数据
- 所有激活操作使用官方KMS协议
- 建议仅从可信来源获取KMS服务器地址
- 使用前请确保了解KMS激活的法律风险

## 📊 支持的Windows版本

### Windows 11
- 专业版
- 专业工作站版
- 专业教育版
- 教育版
- 企业版
- 企业版 G
- 企业版 LTSC 2024

### Windows 10
- 专业版
- 专业工作站版
- 专业教育版
- 教育版
- 企业版
- 企业版 G
- 企业版 LTSC 2019
- 企业版 LTSB 2016

### Windows 7/8/8.1
- 专业版
- 企业版

## 🐛 故障排除

### 常见问题

1. **权限不足**
   - 以管理员身份运行程序

2. **KMS服务器连接失败**
   - 检查网络连接
   - 尝试其他KMS服务器
   - 检查防火墙设置

3. **激活失败**
   - 确认Windows版本支持
   - 检查系统时间是否正确
   - 查看日志文件 `activation.log`

4. **服务启动失败**
   - 检查端口是否被占用
   - 确认Python环境正常
   - 查看控制台错误信息

### 日志查看

激活日志保存在 `backend/activation.log`，包含详细的操作记录和错误信息。

## 📞 技术支持

如有问题，请查看日志文件或提交Issue。

## ⚖️ 免责声明

本工具仅供学习和测试使用，请确保在合法范围内使用。使用者需自行承担相关法律责任。

---

**注意**: 使用KMS激活可能违反微软许可协议，请确保在授权范围内使用本工具。