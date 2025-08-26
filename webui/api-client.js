/**
 * API客户端
 * 与后端服务通信
 */

class ApiClient {
    constructor(baseUrl = 'http://localhost:5000') {
        this.baseUrl = baseUrl;
        this.timeout = 30000; // 30秒超时
    }

    /**
     * 发送HTTP请求
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        };

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), this.timeout);
            
            const response = await fetch(url, {
                ...config,
                signal: controller.signal,
            });
            
            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('请求超时');
            }
            throw error;
        }
    }

    /**
     * GET请求
     */
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    /**
     * POST请求
     */
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    /**
     * 获取系统激活状态
     */
    async getActivationStatus() {
        return this.get('/api/status');
    }

    /**
     * 自动激活Windows
     */
    async activateWindows(windowsVersion = null, kmsServer = null) {
        const data = {};
        if (windowsVersion) data.windows_version = windowsVersion;
        if (kmsServer) data.kms_server = kmsServer;
        
        return this.post('/api/activate', data);
    }

    /**
     * 测试KMS服务器
     */
    async testKMSServer(kmsServer, port = 1688) {
        return this.post('/api/kms/test', {
            kms_server: kmsServer,
            port: port,
        });
    }

    /**
     * 获取KMS服务器列表
     */
    async getKMSServers() {
        return this.get('/api/kms/servers');
    }

    /**
     * 获取GVLK密钥列表
     */
    async getGVLKKeys() {
        return this.get('/api/keys');
    }

    /**
     * 获取激活历史
     */
    async getActivationHistory() {
        return this.get('/api/history');
    }

    /**
     * 获取系统信息
     */
    async getSystemInfo() {
        return this.get('/api/system/info');
    }

    /**
     * 手动激活步骤
     */
    async manualActivation(action, data = {}) {
        return this.post('/api/activation/manual', {
            action: action,
            ...data,
        });
    }

    /**
     * 检查服务连接
     */
    async checkConnection() {
        try {
            await this.get('/');
            return true;
        } catch {
            return false;
        }
    }
}

// 创建全局API客户端实例
const apiClient = new ApiClient();

/**
 * 更新前端以使用新的API客户端
 */

// 重写原有的激活功能
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
        // 获取系统信息
        progressFill.style.width = '10%';
        progressText.textContent = '正在获取系统信息...';
        
        const systemInfo = await apiClient.getSystemInfo();
        if (!systemInfo.success) {
            throw new Error('无法获取系统信息');
        }
        
        // 开始激活
        progressFill.style.width = '30%';
        progressText.textContent = '正在激活Windows...';
        
        const activateResult = await apiClient.activateWindows();
        
        if (activateResult.success) {
            progressFill.style.width = '100%';
            progressText.textContent = '激活成功！';
            
            await delay(1000);
            showNotification('Windows已成功激活！', 'success');
            closeModal();
            
            // 更新状态页面
            updateStatusPage();
        } else {
            throw new Error(activateResult.error || '激活失败');
        }
        
    } catch (error) {
        progressFill.style.width = '100%';
        progressFill.style.backgroundColor = '#ff4757';
        progressText.textContent = '激活失败';
        
        showNotification('激活失败：' + error.message, 'error');
    } finally {
        activationInProgress = false;
        activateBtn.disabled = false;
        activateBtn.textContent = '开始激活';
        
        setTimeout(() => {
            resetActivationProgress();
        }, 3000);
    }
}

// 重写状态检查功能
async function checkActivationStatus() {
    showNotification('正在检查激活状态...', 'info');
    
    try {
        const status = await apiClient.getActivationStatus();
        
        if (status.success) {
            const activationData = status.activation_status;
            const systemData = status.system_info;
            
            updateStatusDisplay({
                isActivated: activationData.is_activated,
                productId: activationData.product_id || '未知',
                licenseStatus: activationData.license_status || '未知',
                expiryDate: activationData.is_activated ? '永久有效' : '未激活',
                osName: systemData.system_info?.os_name || 'Windows',
                osVersion: systemData.system_info?.os_version || '未知'
            });
            
            showNotification('状态检查完成', 'success');
        } else {
            throw new Error(status.error || '无法获取状态');
        }
        
    } catch (error) {
        showNotification('状态检查失败：' + error.message, 'error');
    }
}

// 重写状态页面更新
async function updateStatusPage() {
    try {
        const status = await apiClient.getActivationStatus();
        
        if (status.success) {
            const activationData = status.activation_status;
            const systemData = status.system_info;
            
            // 更新系统名称
            const osNameElement = document.querySelector('#status-tab h3');
            if (osNameElement) {
                osNameElement.textContent = systemData.system_info?.os_name || 'Windows';
            }
            
            updateStatusDisplay({
                isActivated: activationData.is_activated,
                productId: activationData.product_id || '未知',
                licenseStatus: activationData.license_status || '未知',
                expiryDate: activationData.is_activated ? '永久有效' : '未激活'
            });
        }
    } catch (error) {
        console.error('更新状态页面失败:', error);
    }
}

// 添加KMS服务器测试功能
async function testKMSServer() {
    const kmsServer = document.getElementById('kms-server').value;
    const kmsPort = document.getElementById('kms-port').value;
    
    if (!kmsServer) {
        showNotification('请输入KMS服务器地址', 'warning');
        return;
    }
    
    showNotification('正在测试KMS服务器...', 'info');
    
    try {
        const result = await apiClient.testKMSServer(kmsServer, parseInt(kmsPort) || 1688);
        
        if (result.success) {
            showNotification('KMS服务器连接成功', 'success');
        } else {
            showNotification('KMS服务器连接失败：' + result.message, 'error');
        }
        
    } catch (error) {
        showNotification('测试失败：' + error.message, 'error');
    }
}

// 在设置页面添加KMS测试按钮
document.addEventListener('DOMContentLoaded', function() {
    // 添加KMS测试按钮
    const settingsSection = document.querySelector('#settings-tab .settings-grid');
    if (settingsSection) {
        const testButton = document.createElement('button');
        testButton.className = 'btn-secondary';
        testButton.innerHTML = '<i class="fas fa-network-wired"></i> 测试KMS服务器';
        testButton.onclick = testKMSServer;
        
        const settingsCard = settingsSection.querySelector('.glass-card');
        if (settingsCard) {
            settingsCard.appendChild(testButton);
        }
    }
    
    // 加载KMS服务器列表
    loadKMSServers();
});

// 加载KMS服务器列表
async function loadKMSServers() {
    try {
        const result = await apiClient.getKMSServers();
        if (result.success) {
            // 可以在这里填充KMS服务器下拉列表
            console.log('可用的KMS服务器:', result.servers);
        }
    } catch (error) {
        console.error('加载KMS服务器列表失败:', error);
    }
}