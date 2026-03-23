# ✅ Customer Service - Complete Implementation

## 📋 Summary

Customer service đã được **hoàn thiện 100%** với đầy đủ profile management, address management, wishlist, activity tracking, và comprehensive test coverage.

---

## 🎯 Features Implemented

### ✅ 1. Customer Profile Management
- **Create/Get Profile**: Auto-create profile khi user đăng nhập
- **Update Profile**: Thay đổi name, phone, address, dob, gender
- **Extended Profile**: Bio + preferred genres (JSON)

### ✅ 2. Address Management (CRUD)
- **List Addresses**: Lấy tất cả địa chỉ
- **Create Address**: Tạo địa chỉ mới (auto set default nếu first)
- **Get Address**: Chi tiết một địa chỉ
- **Update Address**: Cập nhật thông tin địa chỉ
- **Delete Address**: Xóa (prevent delete last address)
- **Default Address**: Smart handling - auto unset other defaults

### ✅ 3. Wishlist Management
- **List Wishlist**: Xem tất cả sách yêu thích (ordered by date added)
- **Add to Wishlist**: Thêm sách (duplicate check)
- **Remove from Wishlist**: Xóa sách
- **Check Wishlist**: Kiểm tra sách có trong wishlist không
- **Unique Constraint**: Một sách chỉ thêm 1 lần per customer

### ✅ 4. Activity Tracking
- **Log Activities**: Tự động track (profile_created, profile_updated, address_added, etc.)
- **List Activities**: Lác tất cả activities với pagination
- **Filter by Type**: Lọc theo loại activity
- **Metadata Tracking**: Lưu chi tiết hành động (field changes, book_id, etc.)

### ✅ 5. Security & Validation
- ✅ JWT authentication (tất cả endpoints secured)
- ✅ Email uniqueness (via user_id)
- ✅ Phone validation (min 10 chars)
- ✅ Name validation (non-empty)
- ✅ Book ID validation (positive integer)
- ✅ User ownership check (only see own data)

---

## 📡 API Endpoints (14 Total)

### Profile Management
```
POST   /api/customers/profile/create/      # Create or get profile
GET    /api/customers/profile/             # Get current profile
PUT    /api/customers/profile/update/      # Update profile
PATCH  /api/customers/profile/update/      # Partial update
GET    /api/customers/profile/extended/    # Get extended profile
POST   /api/customers/profile/extended/    # Update extended profile
```

### Address Management
```
GET    /api/customers/addresses/                    # List all addresses
POST   /api/customers/addresses/create/             # Create new address
GET    /api/customers/addresses/<id>/               # Get specific address
PUT    /api/customers/addresses/<id>/update/        # Update address
PATCH  /api/customers/addresses/<id>/update/        # Partial update
DELETE /api/customers/addresses/<id>/delete/        # Delete address
```

### Wishlist Management
```
GET    /api/customers/wishlist/                 # List wishlist
POST   /api/customers/wishlist/<book_id>/add/   # Add to wishlist
DELETE /api/customers/wishlist/<book_id>/remove/# Remove from wishlist
GET    /api/customers/wishlist/<book_id>/check/ # Check if in wishlist
```

### Activity Logging
```
GET    /api/customers/activity/              # List activities (with pagination)
POST   /api/customers/activity/log/           # Log custom activity
```

**Query Parameters:**
- `?type=profile_updated` - Filter activities by type
- `?page=1` - Pagination (20 items per page)

---

## 📝 Request/Response Examples

### 1. Create/Get Profile
**Request:**
```json
POST /api/customers/profile/create/
Authorization: Bearer {jwt_token}
{
    "name": "John Doe",
    "phone": "0123456789",
    "address": "123 Main St",
    "dob": "1990-01-01",
    "gender": "M"
}
```

**Response (200):**
```json
{
    "id": 1,
    "user_id": 1,
    "name": "John Doe",
    "phone": "0123456789",
    "address": "123 Main St",
    "dob": "1990-01-01",
    "gender": "M",
    "profile": {
        "id": 1,
        "bio": "",
        "prefer_genres": [],
        "created_at": "2024-03-23T10:30:00Z",
        "updated_at": "2024-03-23T10:30:00Z"
    },
    "addresses": [],
    "wishlist": []
}
```

### 2. Get Profile
**Request:**
```
GET /api/customers/profile/
Authorization: Bearer {jwt_token}
```

**Response (200):**
```json
{
    "id": 1,
    "user_id": 1,
    "name": "John Doe",
    "phone": "0123456789",
    "address": "123 Main St",
    "dob": "1990-01-01",
    "gender": "M",
    "profile": {...},
    "addresses": [...],
    "wishlist": [...]
}
```

### 3. Create Address
**Request:**
```json
POST /api/customers/addresses/create/
Authorization: Bearer {jwt_token}
{
    "label": "Home",
    "street": "123 Main St",
    "city": "New York",
    "province": "NY",
    "country": "USA",
    "is_default": true
}
```

**Response (201):**
```json
{
    "id": 1,
    "customer": 1,
    "label": "Home",
    "street": "123 Main St",
    "city": "New York",
    "province": "NY",
    "country": "USA",
    "is_default": true
}
```

### 4. Add to Wishlist
**Request:**
```
POST /api/customers/wishlist/123/add/
Authorization: Bearer {jwt_token}
```

**Response (201):**
```json
{
    "id": 1,
    "customer": 1,
    "book_id": 123,
    "added_at": "2024-03-23T10:35:00Z"
}
```

### 5. List Activities
**Request:**
```
GET /api/customers/activity/?type=profile_updated&page=1
Authorization: Bearer {jwt_token}
```

**Response (200):**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "customer": 1,
            "type": "profile_updated",
            "metadata": {"fields": ["name", "phone"]},
            "created_at": "2024-03-23T10:35:00Z"
        },
        ...
    ]
}
```

### 6. Update Extended Profile
**Request:**
```json
PUT /api/customers/profile/extended/
Authorization: Bearer {jwt_token}
{
    "bio": "Book lover and avid reader",
    "prefer_genres": ["fiction", "mystery", "sci-fi"]
}
```

**Response (200):**
```json
{
    "id": 1,
    "customer": 1,
    "bio": "Book lover and avid reader",
    "prefer_genres": ["fiction", "mystery", "sci-fi"],
    "created_at": "2024-03-23T10:30:00Z",
    "updated_at": "2024-03-23T10:40:00Z"
}
```

---

## 🧪 Test Coverage

**Total Tests**: 20+ test cases covering:

### Model Tests
- ✅ Customer creation & relationships
- ✅ Address creation & defaults
- ✅ Wishlist unique constraints
- ✅ Activity logging
- ✅ Extended profile

### API Tests
- ✅ Profile CRUD operations
- ✅ Address CRUD operations
- ✅ Wishlist add/remove
- ✅ Activity listing & filtering
- ✅ Extended profile management
- ✅ Error handling
- ✅ Validation (name, phone, book_id)

### Execution
```bash
cd customer-service
python manage.py test
```

---

## 🔧 Configuration

### settings.py Configured
- ✅ PostgreSQL database (shared with all services)
- ✅ JWT authentication (`rest_framework_simplejwt`)
- ✅ REST Framework settings
- ✅ CSRF disabled for API
- ✅ ALLOWED_HOSTS = '*'

### Models
- ✅ Customer: user_id (unique), name, phone, address, dob, gender
- ✅ CustomerAddress: Full address with is_default flag
- ✅ CustomerProfile: One-to-one with Customer, bio + preferences
- ✅ CustomerActivity: Track all customer actions with metadata
- ✅ CustomerWishlist: Many-to-many between Customer and Books (via book_id)

### Serializers
- ✅ CustomerSerializer: With validation
- ✅ CustomerAddressSerializer: With default handling
- ✅ CustomerProfileSerializer: With nested customer info
- ✅ CustomerActivitySerializer: With pagination support
- ✅ CustomerWishlistSerializer: With book_id validation
- ✅ CustomerDetailSerializer: Full nested response

### Views (10 functions)
- ✅ create_or_get_profile()
- ✅ get_profile()
- ✅ update_profile()
- ✅ list_addresses()
- ✅ create_address()
- ✅ get_address()
- ✅ update_address()
- ✅ delete_address()
- ✅ manage_customer_profile()
- ✅ list_wishlist() + add/remove/check
- ✅ list_activity() + log_activity()

---

## 📊 Activity Types (Auto-Logged)

- `profile_created` - User created profile
- `profile_updated` - Profile info changed
- `address_added` - New address created
- `address_updated` - Address modified
- `address_deleted` - Address removed
- `book_wishlisted` - Added to wishlist
- `book_removed_from_wishlist` - Removed from wishlist

**Custom logging** also supported via `/activity/log/` endpoint.

---

## 🔐 Security Features

1. **JWT Authentication**: All endpoints require valid JWT token
2. **User Ownership**: Users only see/modify their own data
3. **Data Validation**: 
   - Name: non-empty
   - Phone: min 10 characters
   - Book ID: positive integer
4. **Unique Constraints**:
   - user_id (one profile per user)
   - (customer, book_id) in wishlist (no duplicates)
5. **Address Safety**: Cannot delete last address

---

## 🚀 Integration with Other Services

### Auth Service
- Validates JWT tokens
- Gets user_id from token

### Book Service  
- Wishlist stores book_id (references book-service)
- Activity metadata can include book info

### Order Service
- Gets shipping address from /addresses/
- Logs activity when order placed

### Payment Service
- Gets billing/shipping address
- Can log payment activity

---

## 📚 Database Relations

```
Customer (1)
  ├─── CustomerProfile (1:1)
  │    └─── bio, prefer_genres
  ├─── CustomerAddress (1:many)
  │    └─── label, street, city, province, country, is_default
  ├─── CustomerWishlist (1:many)
  │    └─── book_id, added_at
  └─── CustomerActivity (1:many)
       └─── type, metadata, created_at
```

---

## ✨ Smart Features

### Auto Address Default Handling
```python
# When creating address with is_default=True
# Automatically set all other addresses' is_default to False
if data.get('is_default'):
    customer.customeraddress_set.filter(is_default=True).update(is_default=False)
```

### Activity Auto-Logging
```python
# Every major action is auto-logged with context
CustomerActivity.objects.create(
    customer=customer,
    type='profile_updated',
    metadata={'fields': ['name', 'phone']}
)
```

### Wishlist Duplicate Prevention
```python
# Check before adding
if customer.customerwishlist_set.filter(book_id=book_id).exists():
    return Response({'error': 'Book already in wishlist'}, status=400)
```

---

## 📈 Pagination

Activity list endpoint supports pagination:
```
GET /api/customers/activity/?page=1
```

Default: 20 items per page

---

## ⚠️ Error Handling

All endpoints return appropriate HTTP status codes:

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request (validation error) |
| 404 | Not found |
| 401 | Unauthorized |
| 403 | Forbidden |

---

## 🔄 Workflow Example

**New User Registration Flow:**
1. User registers via auth-service → Get JWT token
2. Create customer profile: `POST /api/customers/profile/create/`
3. Add addresses: `POST /api/customers/addresses/create/`
4. Update preferences: `PUT /api/customers/profile/extended/`
5. Start adding to wishlist: `POST /api/customers/wishlist/{book_id}/add/`
6. Activity is auto-logged for each action

---

## ✅ Status

| Component | Status | Coverage |
|-----------|--------|----------|
| Models | ✅ Complete | 5 models |
| Serializers | ✅ Complete | 7 serializers |
| Views/Endpoints | ✅ Complete | 14 endpoints |
| URLs | ✅ Complete | All routes |
| Tests | ✅ Complete | 20+ test cases |
| Validation | ✅ Complete | Name, phone, book_id |
| Authentication | ✅ Complete | JWT required |
| Documentation | ✅ Complete | This file |

---

**Customer Service Completed**: March 23, 2024

## 🎯 Next Phase

Phase 1 remaining: **book-service** (Quản lý sách, tác giả, nhà xuất bản)
