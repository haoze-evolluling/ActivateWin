# NiceGUI KMS激活管理器

基于NiceGUI框架开发的现代化KMS激活管理工具。

## 特性

- **现代化界面**: 基于NiceGUI的响应式Web界面
- **多页面设计**: 主页、激活管理、设置页面
- **实时交互**: 异步操作，流畅的用户体验
- **主题支持**: 支持亮色/暗色主题切换
- **跨平台**: 基于Web技术，可在任何现代浏览器中运行

## 项目结构

```
nicegui_frontend/
├── main.py              # 应用入口点
├── pages/               # 页面模块
│   ├── __init__.py
│   ├── main_page.py     # 主页面
│   ├── activation_page.py # 激活管理页面
│   └── settings_page.py # 设置页面
├── utils/               # 工具模块
│   ├── __init__.py
│   └── theme_manager.py # 主题管理器
├── config/              # 配置文件目录
└── README.md           # 说明文档
```

## 快速开始

### 安装依赖

确保已安装Python 3.7或更高版本，然后运行：

```bash
pip install nicegui
```

或使用项目requirements.txt：

```bash
pip install -r requirements.txt
```

### 启动应用

#### 方法1：使用启动脚本
双击运行 `run_nicegui.bat` 文件

#### 方法2：命令行启动
```bash
cd nicegui_frontend
python main.py
```

#### 方法3：从项目根目录启动
```bash
python nicegui_frontend/main.py
```

## 访问应用

启动后，在浏览器中访问：
- http://localhost:8080

## 页面说明

### 主页
- 欢迎信息
- 功能特性展示
- 快速导航

### 激活管理
- Windows激活
- Office激活
- 实时状态显示
- 激活结果反馈

### 设置
- 外观设置（主题切换）
- 功能配置
- 系统信息显示
- 重置选项

## 开发说明

### 添加新页面

1. 在 `pages/` 目录创建新的页面文件
2. 在 `main.py` 中添加路由配置
3. 在导航菜单中添加对应链接

### 主题定制

修改 `utils/theme_manager.py` 中的主题配置，支持自定义颜色和样式。

### 扩展功能

新的功能可以添加到对应的页面模块中，保持代码结构清晰。

## 注意事项

- 确保系统已安装Python 3.7+
- 需要管理员权限执行激活操作
- 首次运行可能需要安装依赖包
- 建议在支持的浏览器中使用（Chrome、Firefox、Edge等）