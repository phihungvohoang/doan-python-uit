# Motel API - Hệ thống quản lý phòng trọ

Đồ án xây dựng Web API quản lý phòng trọ bằng Python Django REST Framework và SQLite.

## Công nghệ sử dụng

- Python
- Django
- Django REST Framework
- SQLite
- JWT Authentication
- drf-spectacular Swagger
- django-filter

## Chức năng chính

- Đăng nhập bằng JWT
- Quản lý khu trọ
- Quản lý phòng trọ
- Quản lý người thuê
- Quản lý hợp đồng thuê phòng
- Quản lý chỉ số điện nước
- Tạo hóa đơn tự động
- Thanh toán hóa đơn
- Kiểm thử API bằng Django TestCase

## Cấu trúc project

```txt
motel_api/
├── accounts/
├── properties/
├── rooms/
├── tenants/
├── contracts/
├── invoices/
├── reports/
├── motel_api/
├── manage.py
└── README.md

1. Clone project
git clone https://github.com/phihungvohoang/doan-python-uit.git
cd doan-python-uit
2. Tạo virtual environment
python -m venv venv
3. Kích hoạt môi trường ảo

Windows PowerShell:

.\venv\Scripts\Activate.ps1

Windows CMD:

venv\Scripts\activate
4. Cài thư viện
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-filter
pip install drf-spectacular

Hoặc nếu có file requirements.txt:

pip install -r requirements.txt
5. Chạy migrate
python manage.py makemigrations
python manage.py migrate
6. Tạo tài khoản admin
python manage.py createsuperuser
7. Chạy server
python manage.py runserver
Truy cập hệ thống

Swagger API:

http://127.0.0.1:8000/api/docs/

Admin Django:

http://127.0.0.1:8000/admin/
Xác thực JWT
Đăng nhập

Endpoint:

POST /api/auth/login/

Body:

{
  "username": "admin",
  "password": "your_password"
}

Response:

{
  "refresh": "refresh_token",
  "access": "access_token"
}

Khi gọi API cần đăng nhập, thêm header:

Authorization: Bearer access_token
API chính
Method	Endpoint	Chức năng
POST	/api/auth/login/	Đăng nhập
POST	/api/auth/refresh/	Làm mới token
GET	/api/properties/	Danh sách khu trọ
POST	/api/properties/	Tạo khu trọ
GET	/api/rooms/	Danh sách phòng
POST	/api/rooms/	Tạo phòng
GET	/api/tenants/	Danh sách người thuê
POST	/api/tenants/	Tạo người thuê
GET	/api/contracts/	Danh sách hợp đồng
POST	/api/contracts/	Tạo hợp đồng
PATCH	/api/contracts/{id}/terminate/	Kết thúc hợp đồng
GET	/api/utility-readings/	Danh sách điện nước
POST	/api/utility-readings/	Nhập điện nước
GET	/api/invoices/	Danh sách hóa đơn
POST	/api/invoices/generate/	Tạo hóa đơn tự động
PATCH	/api/invoices/{id}/mark-paid/	Thanh toán hóa đơn
Luồng demo
1. Tạo khu trọ
{
  "name": "Nhà trọ A",
  "address": "TP.HCM",
  "description": "Khu trọ sinh viên",
  "total_floors": 3
}
2. Tạo phòng
{
  "property": 1,
  "room_number": "P101",
  "area": 20,
  "price": 2500000,
  "max_people": 2,
  "status": "AVAILABLE"
}
3. Tạo người thuê
{
  "full_name": "Nguyễn Văn A",
  "phone": "0909000000",
  "identity_number": "123456789",
  "date_of_birth": "2000-01-01",
  "address": "TP.HCM"
}
4. Tạo hợp đồng
{
  "room": 1,
  "tenant": 1,
  "start_date": "2026-05-01",
  "end_date": "2027-05-01",
  "deposit": 2500000,
  "monthly_price": 2500000,
  "status": "ACTIVE"
}

Sau khi tạo hợp đồng, phòng sẽ tự chuyển từ:

AVAILABLE -> OCCUPIED
5. Nhập chỉ số điện nước
{
  "contract": 1,
  "month": 5,
  "year": 2026,
  "old_electric": 100,
  "new_electric": 150,
  "old_water": 20,
  "new_water": 25,
  "electric_price": 3500,
  "water_price": 15000
}
6. Tạo hóa đơn tự động
{
  "contract_id": 1,
  "month": 5,
  "year": 2026,
  "service_fee": 100000,
  "due_date": "2026-05-31"
}

Kết quả:

Tiền phòng: 2,500,000
Tiền điện: 50 x 3,500 = 175,000
Tiền nước: 5 x 15,000 = 75,000
Phí dịch vụ: 100,000
Tổng tiền: 2,850,000
7. Thanh toán hóa đơn
PATCH /api/invoices/1/mark-paid/
Chạy test

Chạy toàn bộ test:

python manage.py test

Chạy test riêng app hóa đơn:

python manage.py test invoices -v 2

Ví dụ kết quả test:

Found 7 test(s).
Creating test database for alias 'default'...
System check identified no issues.
.......
Ran 7 tests in 6.887s

OK
Kết quả kiểm thử hóa đơn

Ví dụ output khi test tạo hóa đơn:

===== KẾT QUẢ TEST TẠO HÓA ĐƠN =====
Status code: 200
Tên người thuê: Nguyễn Văn A
Số phòng: P101
Tiền phòng: 2500000.00
Tiền điện: 175000.00
Tiền nước: 75000.00
Phí dịch vụ: 100000.00
Tổng tiền: 2850000.00
====================================

Ví dụ output khi test thanh toán hóa đơn:

===== KẾT QUẢ TEST THANH TOÁN HÓA ĐƠN =====
Status code: 200
Dữ liệu trả về: {'message': 'Đã thanh toán hóa đơn.'}
Trạng thái hóa đơn sau thanh toán: PAID
==========================================
Tác giả

Sinh viên thực hiện: Võ Hoàng Phi Hùng, Trần Hoàng, Hà Minh Nhật
