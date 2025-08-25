# KMS激活管理器 - 前后端分离架构

## 架构概述

本程序采用前后端分离架构，将用户界面(UI)与业务逻辑完全解耦：

### 架构组件

#### 前端层 (frontend/)
- **ui_manager.py**: 用户界面管理器，负责所有UI展示和交互
- 使用Tkinter实现图形界面
- 完全独立于业务逻辑

#### 后端层 (backend/)
- **kms_service.py**: KMS激活服务，处理所有业务逻辑
- 包含激活流程、服务器测试、系统信息获取等
- 提供API接口供前端调用

#### 数据模型层 (models/)
- **activation_data.py**: 数据模型定义
- 定义激活配置、服务器状态等数据结构
- 提供数据访问接口

#### 主程序 (main.py)
- 程序入口点
- 负责权限检查和程序启动

## 文件结构

```
ActivateWin/
├── main.py                 # 新的主程序入口
├── frontend/
│   └── ui_manager.py      # 用户界面管理器
├── backend/
│   └── kms_service.py     # KMS激活服务
├── models/
│   └── activation_data.py   # 数据模型
├── build_new.py            # 新的打包脚本
├── requirements.txt        # 依赖列表
├── icon.ico               # 程序图标
├── icon.png               # 程序图标(备用)
├── image.png              # 背景图片
├── kmsserver.md           # KMS服务器列表
└── kmskey.md              # 产品密钥列表
```

## 使用方法

### 1. 直接运行
```bash
python main.py
```

### 2. 使用打包版本
运行 `build_new.py` 生成可执行文件：
```bash
python build_new.py
```
生成的可执行文件位于 `dist/KMSActivator.exe`

### 3. 开发模式运行
```bash
# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

## 架构优势

### 1. 解耦设计
- **UI与业务逻辑分离**: 前端只负责展示，后端处理逻辑
- **易于维护**: 修改UI不影响业务逻辑，反之亦然
- **可测试性**: 各层可独立测试

### 2. 模块化
- **职责清晰**: 每层有明确的职责边界
- **代码复用**: 业务逻辑可在不同UI中复用
- **扩展性强**: 易于添加新功能

### 3. 技术栈灵活
- **UI可替换**: 可以轻松替换为PyQt、Web界面等
- **后端可扩展**: 可以添加更多激活服务
- **数据模型统一**: 保持数据一致性

## 开发指南

### 添加新功能

#### 添加新的Windows版本支持
编辑 `models/activation_data.py` 中的 `_load_windows_versions` 方法：

```python
def _load_windows_versions(self) -> Dict[str, Dict[str, str]]:
    return {
        "Windows 11": {
            # 现有版本...
        },
        "新Windows版本": {
            "专业版": "新密钥",
            "企业版": "新密钥"
        }
    }
```

#### 添加新的激活服务
在 `backend/kms_service.py` 中添加新方法：

```python
def new_activation_method(self, config: ActivationConfig) -> Tuple[bool, str]:
    # 实现新的激活逻辑
    return True, "激活成功"
```

#### 修改UI界面
编辑 `frontend/ui_manager.py` 中的相应方法，不影响业务逻辑。

### 测试各层

#### 测试数据模型
```python
from models.activation_data import ActivationData

data = ActivationData()
# data.get_all_windows_versions()
```

#### 测试后端服务
```python
from backend.kms_service import KMSService
from models.activation_data import ActivationConfig

service = KMSService()
config = ActivationConfig("Windows 11", "专业版", "密钥", "服务器")
success, message = service.execute_activation(config)
```

#### 测试UI组件
```python
from frontend.ui_manager import UIManager

ui = UIManager()
ui.run()
```

## 故障排除

### 常见问题

#### 1. 模块导入错误
确保项目根目录在Python路径中：
```python
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

#### 2. 权限问题
程序需要管理员权限运行，会自动尝试提升权限。

#### 3. 打包问题
使用 `build_new.py` 而不是旧的打包方法。

## 扩展计划

### 未来功能
- [ ] Web界面支持
- [ ] 命令行界面
- [ ] 批量激活支持
- [ ] 激活状态监控
- [ ] 日志系统
- [ ] 国际化支持

### 技术升级
- [ ] 异步操作支持
- [ ] 插件系统
- [ ] 配置持久化
- [ ] API文档

## 迁移指南

### 从旧版本迁移
1. 备份原有配置
2. 使用新的文件结构
3. 更新启动方式为 `main.py`
4. 测试所有功能正常

### 向后兼容
新的架构保持原有功能不变，用户操作习惯无需改变。