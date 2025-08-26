// 全局变量
let currentTab = 'activation';
let activationInProgress = false;

// DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 应用初始化
function initializeApp() {
    setupTabSwitching();
    loadSettings();
    checkSystemStatus();
    setupThemeToggle();
    
    // 添加页面加载动画
    animateOnLoad();
}

// 标签页切换功能
function setupTabSwitching() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.dataset.tab;
            switchTab(targetTab);
        });
    });
}

function switchTab(tabName) {
    // 更新导航按钮状态
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // 更新内容区域
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    currentTab = tabName;
    
    // 根据标签页执行特定操作
    if (tabName === 'status') {
        updateStatusPage();
    }
}

// 模态框操作
function openActivationDialog() {
    const modal = document.getElementById('activation-modal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function openKMSDialog() {
    // 这里可以添加KMS配置对话框
    showNotification('KMS配置功能开发中...', 'info');
}

function closeModal() {
    const modal = document.getElementById('activation-modal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
    
    // 重置激活进度
    resetActivationProgress();
}

// 激活流程
async function startActivation() {
    if (activationInProgress) return;
    
    activationInProgress = true;
    const activateBtn = document.getElementById('activate-btn');
    const progressSection = document.getElementById('progress-section');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    
    // 禁用按钮并显示进度
    activateBtn.disabled = true;
    activateBtn.textContent = '激活中...';
    progressSection.style.display = 'block';
    
    try {
        // 模拟激活过程
        const steps = [
            { progress: 10, text: '正在验证产品密钥...' },
            { progress: 30, text: '正在连接KMS服务器...' },
            { progress: 60, text: '正在激活Windows...' },
            { progress: 90, text: '正在验证激活状态...' },
            { progress: 100, text: '激活成功！' }
        ];
        
        for (const step of steps) {
            await delay(1000);
            progressFill.style.width = step.progress + '%';
            progressText.textContent = step.text;
        }
        
        // 激活完成
        await delay(500);
        showNotification('Windows已成功激活！', 'success');
        closeModal();
        
        // 更新状态页面
        updateStatusPage();
        
    } catch (error) {
        showNotification('激活失败：' + error.message, 'error');
    } finally {
        activationInProgress = false;
        activateBtn.disabled = false;
        activateBtn.textContent = '开始激活';
    }
}

function resetActivationProgress() {
    const progressSection = document.getElementById('progress-section');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    
    progressSection.style.display = 'none';
    progressFill.style.width = '0%';
    progressText.textContent = '准备激活...';
}

// 状态检查
async function checkActivationStatus() {
    showNotification('正在检查激活状态...', 'info');
    
    try {
        // 模拟API调用
        await delay(1500);
        
        // 模拟获取状态数据
        const statusData = {
            productId: '00331-10000-00001-AA123',
            licenseStatus: '已激活',
            expiryDate: '永久有效',
            isActivated: true
        };
        
        updateStatusDisplay(statusData);
        showNotification('状态检查完成', 'success');
        
    } catch (error) {
        showNotification('状态检查失败：' + error.message, 'error');
    }
}

function updateStatusDisplay(data) {
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    const productId = document.getElementById('product-id');
    const licenseStatus = document.getElementById('license-status');
    const expiryDate = document.getElementById('expiry-date');
    
    statusDot.className = data.isActivated ? 'status-dot activated' : 'status-dot';
    statusText.textContent = data.isActivated ? '已激活' : '未激活';
    productId.textContent = data.productId;
    licenseStatus.textContent = data.licenseStatus;
    expiryDate.textContent = data.expiryDate;
}

// 设置页面功能
function loadSettings() {
    // 从localStorage加载设置
    const settings = JSON.parse(localStorage.getItem('activateWinSettings') || '{}');
    
    // 应用设置
    document.getElementById('theme-select').value = settings.theme || 'auto';
    document.getElementById('animations-toggle').checked = settings.animations !== false;
    document.getElementById('kms-server').value = settings.kmsServer || '';
    document.getElementById('kms-port').value = settings.kmsPort || '1688';
    
    // 应用主题
    applyTheme(settings.theme || 'auto');
}

function saveSettings() {
    const settings = {
        theme: document.getElementById('theme-select').value,
        animations: document.getElementById('animations-toggle').checked,
        kmsServer: document.getElementById('kms-server').value,
        kmsPort: document.getElementById('kms-port').value
    };
    
    localStorage.setItem('activateWinSettings', JSON.stringify(settings));
    applyTheme(settings.theme);
    showNotification('设置已保存', 'success');
}

function setupThemeToggle() {
    const themeSelect = document.getElementById('theme-select');
    const animationsToggle = document.getElementById('animations-toggle');
    
    themeSelect.addEventListener('change', saveSettings);
    animationsToggle.addEventListener('change', saveSettings);
    
    // KMS设置自动保存
    document.getElementById('kms-server').addEventListener('blur', saveSettings);
    document.getElementById('kms-port').addEventListener('blur', saveSettings);
}

function applyTheme(theme) {
    const root = document.documentElement;
    
    if (theme === 'dark') {
        root.style.setProperty('--bg-primary', 'rgba(15, 23, 42, 0.9)');
        root.style.setProperty('--bg-secondary', 'rgba(30, 41, 59, 0.7)');
    } else if (theme === 'light') {
        root.style.setProperty('--bg-primary', 'rgba(248, 250, 252, 0.9)');
        root.style.setProperty('--bg-secondary', 'rgba(241, 245, 249, 0.7)');
        root.style.setProperty('--text-primary', '#1e293b');
        root.style.setProperty('--text-secondary', '#475569');
    } else {
        // 自动模式 - 根据系统偏好
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            applyTheme('dark');
        } else {
            applyTheme('light');
        }
    }
}

// 系统状态检查
async function checkSystemStatus() {
    try {
        // 这里可以添加实际的系统检查逻辑
        const systemInfo = await getSystemInfo();
        console.log('系统信息:', systemInfo);
    } catch (error) {
        console.error('获取系统信息失败:', error);
    }
}

async function getSystemInfo() {
    // 模拟获取系统信息
    await delay(500);
    return {
        os: 'Windows 10 Pro',
        version: '22H2',
        build: '19045.3693',
        architecture: 'x64'
    };
}

// 更新状态页面
async function updateStatusPage() {
    if (currentTab !== 'status') return;
    
    try {
        const statusData = await fetchActivationStatus();
        updateStatusDisplay(statusData);
    } catch (error) {
        console.error('更新状态失败:', error);
    }
}

async function fetchActivationStatus() {
    // 模拟获取激活状态
    await delay(800);
    
    // 随机生成状态数据用于演示
    const isActivated = Math.random() > 0.3;
    
    return {
        productId: '00331-10000-0000' + Math.floor(Math.random() * 10000).toString().padStart(5, '0') + '-AA' + Math.floor(Math.random() * 1000).toString().padStart(3, '0'),
        licenseStatus: isActivated ? '已激活' : '未激活',
        expiryDate: isActivated ? '永久有效' : '需要激活',
        isActivated: isActivated
    };
}

// 通知系统
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
    `;
    
    // 添加到页面
    document.body.appendChild(notification);
    
    // 显示动画
    setTimeout(() => notification.classList.add('show'), 100);
    
    // 自动移除
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// 页面加载动画
function animateOnLoad() {
    const elements = document.querySelectorAll('.glass-card, .glass-header, .glass-main');
    
    elements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// 工具函数
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// 键盘快捷键
document.addEventListener('keydown', function(e) {
    // ESC关闭模态框
    if (e.key === 'Escape') {
        closeModal();
    }
    
    // Ctrl/Cmd + 数字键切换标签页
    if (e.ctrlKey || e.metaKey) {
        const keyMap = {
            '1': 'activation',
            '2': 'status',
            '3': 'settings'
        };
        
        if (keyMap[e.key]) {
            e.preventDefault();
            switchTab(keyMap[e.key]);
        }
    }
});

// 窗口大小变化时重新计算布局
window.addEventListener('resize', function() {
    // 这里可以添加响应式布局调整逻辑
});

// 系统主题变化监听
if (window.matchMedia) {
    const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
    darkModeQuery.addEventListener('change', function() {
        const currentTheme = document.getElementById('theme-select').value;
        if (currentTheme === 'auto') {
            applyTheme('auto');
        }
    });
}

// 添加通知样式
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        z-index: 1001;
        max-width: 400px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        background: linear-gradient(135deg, #4ade80, #22c55e);
    }
    
    .notification-error {
        background: linear-gradient(135deg, #ef4444, #dc2626);
    }
    
    .notification-warning {
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
    }
    
    .notification-info {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
    }
`;
document.head.appendChild(notificationStyles);