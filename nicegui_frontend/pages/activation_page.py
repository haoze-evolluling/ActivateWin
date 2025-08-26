"""
激活页面组件
提供Windows和Office激活功能
"""

from nicegui import ui
import asyncio
from typing import Optional
from pathlib import Path
import sys

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.kms_service import KMSService

class ActivationPage:
    """激活页面类"""
    
    def __init__(self):
        self.kms_service = KMSService()
        self.current_product = None
        self.activation_result = None
        
    def create_header(self):
        """创建页面头部"""
        with ui.header().classes('bg-primary text-white shadow-lg'):
            with ui.row().classes('w-full items-center justify-between'):
                ui.label('激活管理').classes('text-h4')
                
                with ui.row().classes('items-center'):
                    ui.button('返回主页', on_click=lambda: ui.navigate.to('/')).props('flat')
                    ui.button('设置', on_click=lambda: ui.navigate.to('/settings')).props('flat')
                    
    def create_product_selection(self):
        """创建产品选择区域"""
        with ui.card().classes('w-full q-pa-md'):
            ui.label('选择激活产品').classes('text-h6')
            
            with ui.row().classes('q-gutter-md q-mt-sm'):
                self.windows_btn = ui.button(
                    'Windows激活',
                    on_click=lambda: self.select_product('windows')
                ).props('color=primary')
                
                self.office_btn = ui.button(
                    'Office激活',
                    on_click=lambda: self.select_product('office')
                ).props('color=secondary')
                
    def create_activation_controls(self):
        """创建激活控制区域"""
        self.controls_card = ui.card().classes('w-full q-pa-md')
        
        with self.controls_card:
            ui.label('激活控制').classes('text-h6')
            
            # 状态显示
            self.status_label = ui.label('请选择要激活的产品').classes('text-subtitle1')
            
            # 进度条（初始隐藏）
            self.progress_bar = ui.linear_progress(value=0).classes('q-mt-md')
            self.progress_bar.visible = False
            
            # 结果显示区域
            self.result_area = ui.card().classes('w-full q-pa-md q-mt-md')
            self.result_area.visible = False
            
            # 操作按钮
            with ui.row().classes('q-gutter-md q-mt-md'):
                self.activate_btn = ui.button(
                    '开始激活',
                    on_click=self.start_activation
                ).props('color=positive')
                self.activate_btn.disable()
                
                self.refresh_btn = ui.button(
                    '刷新状态',
                    on_click=self.refresh_status
                ).props('color=info')
                
    async def select_product(self, product_type: str):
        """选择产品类型"""
        self.current_product = product_type
        
        # 更新按钮状态
        if product_type == 'windows':
            self.windows_btn.props('color=positive')
            self.office_btn.props('color=secondary')
            self.status_label.text = '已选择：Windows激活'
        else:
            self.windows_btn.props('color=primary')
            self.office_btn.props('color=positive')
            self.status_label.text = '已选择：Office激活'
            
        self.activate_btn.enable()
        
    async def start_activation(self):
        """开始激活流程"""
        if not self.current_product:
            ui.notify('请先选择产品类型', type='warning')
            return
            
        # 禁用按钮，显示进度
        self.activate_btn.set_enabled(False)
        self.progress_bar.visible = True
        self.progress_bar.value = 0
        self.result_area.visible = False
        
        try:
            # 模拟激活过程
            for i in range(1, 6):
                await asyncio.sleep(0.5)
                self.progress_bar.value = i * 20
                
            # 这里应该调用实际的KMS服务
            result = await self.perform_activation()
            
            # 显示结果
            self.show_activation_result(result)
            
        except Exception as e:
            ui.notify(f'激活失败：{str(e)}', type='negative')
            
        finally:
            self.activate_btn.set_enabled(True)
            self.progress_bar.visible = False
            
    async def perform_activation(self):
        """执行激活操作"""
        try:
            if self.current_product == 'windows':
                # 调用Windows激活
                return await self.kms_service.activate_windows()
            else:
                # 调用Office激活
                return await self.kms_service.activate_office()
        except Exception as e:
            return {'success': False, 'message': str(e)}
            
    def show_activation_result(self, result: dict):
        """显示激活结果"""
        with self.result_area:
            self.result_area.clear()
            
            if result.get('success', False):
                ui.label('激活成功！').classes('text-h6 text-positive')
                ui.label(result.get('message', '产品已成功激活')).classes('text-body1')
            else:
                ui.label('激活失败').classes('text-h6 text-negative')
                ui.label(result.get('message', '未知错误')).classes('text-body1')
                
        self.result_area.visible = True
        
    async def refresh_status(self):
        """刷新状态"""
        ui.notify('正在刷新状态...', type='info')
        # 这里可以添加实际的状态检查逻辑
        
def create_activation_page():
    """创建激活页面"""
    page = ActivationPage()
    
    # 设置页面背景
    ui.colors(primary='#1976D2', secondary='#424242', accent='#82B1FF')
    
    # 创建页面内容
    page.create_header()
    
    with ui.column().classes('q-pa-md q-gutter-md'):
        page.create_product_selection()
        page.create_activation_controls()