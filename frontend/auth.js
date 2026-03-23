// API Base URL
const API_BASE = 'http://localhost:8001/api/auth';

// Utility functions
function showAlert(elementId, message, type = 'danger') {
    const alert = document.getElementById(elementId);
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.classList.remove('d-none');
    setTimeout(() => alert.classList.add('d-none'), 5000);
}

function hideAlert(elementId) {
    document.getElementById(elementId).classList.add('d-none');
}

function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.add('d-none');
    });
    // Show selected section
    document.getElementById(sectionId + 'Section').classList.remove('d-none');
}

function updateNav() {
    const token = localStorage.getItem('access_token');
    const profileLink = document.getElementById('profileLink');
    const logoutLink = document.getElementById('logoutLink');

    if (token) {
        profileLink.classList.remove('d-none');
        logoutLink.classList.remove('d-none');
        showSection('profile');
        loadProfile();
    } else {
        profileLink.classList.add('d-none');
        logoutLink.classList.add('d-none');
        showSection('register');
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    updateNav();
    showAlert('loginAlert', 'Đã đăng xuất thành công', 'success');
}

// API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    const config = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        config.body = JSON.stringify(data);
    }

    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, config);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || result.message || 'API Error');
        }

        return result;
    } catch (error) {
        throw error;
    }
}

// Register
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    hideAlert('registerAlert');

    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;

    try {
        const result = await apiCall('/register/', 'POST', {
            username,
            email,
            password
        });

        showAlert('registerAlert', 'Đăng ký thành công! Vui lòng đăng nhập.', 'success');
        document.getElementById('registerForm').reset();
        showSection('login');
    } catch (error) {
        showAlert('registerAlert', error.message);
    }
});

// Login
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    hideAlert('loginAlert');

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const result = await apiCall('/login/', 'POST', {
            email,
            password
        });

        localStorage.setItem('access_token', result.access);
        localStorage.setItem('refresh_token', result.refresh);

        showAlert('loginAlert', 'Đăng nhập thành công!', 'success');
        document.getElementById('loginForm').reset();
        updateNav();
    } catch (error) {
        showAlert('loginAlert', error.message);
    }
});

// Load Profile
async function loadProfile() {
    try {
        const result = await apiCall('/profile/');
        const profileDetails = document.getElementById('profileDetails');

        profileDetails.innerHTML = `
            <strong>ID:</strong> ${result.user.id}<br>
            <strong>Tên đăng nhập:</strong> ${result.user.username}<br>
            <strong>Email:</strong> ${result.user.email}<br>
            <strong>Trạng thái:</strong> ${result.user.is_active ? 'Hoạt động' : 'Không hoạt động'}<br>
            <strong>Vai trò:</strong> ${result.roles.join(', ')}<br>
            <strong>Ngày tạo:</strong> ${new Date(result.user.created_at).toLocaleDateString('vi-VN')}
        `;

        // Show password change option
        document.getElementById('passwordSection').classList.remove('d-none');
    } catch (error) {
        showAlert('profileAlert', 'Không thể tải thông tin profile: ' + error.message);
    }
}

// Password Change
document.getElementById('passwordForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    hideAlert('passwordAlert');

    const oldPassword = document.getElementById('oldPassword').value;
    const newPassword = document.getElementById('newPassword').value;

    try {
        const result = await apiCall('/password/change/', 'POST', {
            old_password: oldPassword,
            new_password: newPassword
        });

        showAlert('passwordAlert', 'Đổi mật khẩu thành công!', 'success');
        document.getElementById('passwordForm').reset();
    } catch (error) {
        showAlert('passwordAlert', error.message);
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateNav();
});