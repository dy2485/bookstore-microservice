# Bookstore Auth Frontend

Frontend đơn giản để test Auth Service API.

## 🚀 Cách chạy

1. **Đảm bảo Auth Service đang chạy** (Docker Compose):
   ```bash
   docker-compose up -d
   ```

2. **Chạy Frontend Server**:
   ```bash
   cd frontend
   python3 -m http.server 8080
   ```

3. **Truy cập**: http://localhost:8080

## 📋 Tính năng

- ✅ **Đăng ký**: Tạo tài khoản mới
- ✅ **Đăng nhập**: Nhận JWT token
- ✅ **Profile**: Xem thông tin cá nhân
- ✅ **Đổi mật khẩu**: Thay đổi password
- ✅ **Đăng xuất**: Xóa token

## 🔧 API Endpoints

Frontend gọi các API sau từ Auth Service (port 8001):

- `POST /api/auth/register/` - Đăng ký
- `POST /api/auth/login/` - Đăng nhập
- `GET /api/auth/profile/` - Lấy profile
- `POST /api/auth/password/change/` - Đổi mật khẩu
- `POST /api/auth/logout/` - Đăng xuất

## 🛠️ Công nghệ

- **HTML5/CSS3**: Giao diện
- **Bootstrap 5**: Styling
- **Vanilla JavaScript**: API calls
- **LocalStorage**: Lưu token

## 📝 Lưu ý

- CORS: Đảm bảo Auth Service cho phép CORS từ localhost:8080
- Token: JWT token được lưu trong localStorage
- Security: Đây là demo, không dùng cho production