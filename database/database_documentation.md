# VTH Money - Database Documentation

## Tổng quan

Database của VTH Money được thiết kế để quản lý giao dịch tài chính, thông tin người dùng, và các hoạt động thanh toán. Hệ thống sử dụng PostgreSQL với các tính năng như UUID, ENUM types, và timestamps với timezone.

## Các kiểu dữ liệu tùy chỉnh (ENUM Types)

### user_status

- `active`: Đang hoạt động
- `inactive`: Không hoạt động
- `blocked`: Bị khóa
- `pending`: Đang chờ xử lý

### gender

- `male`: Nam
- `female`: Nữ
- `other`: Khác

### transaction_status

- `pending`: Đang chờ xử lý
- `completed`: Đã hoàn thành
- `failed`: Thất bại
- `cancelled`: Đã hủy

### kyc_status

- `unverified`: Chưa xác thực
- `pending`: Đang chờ xác thực
- `verified`: Đã xác thực
- `rejected`: Bị từ chối

## Chi tiết các bảng

### 1. users

Lưu trữ thông tin người dùng của hệ thống.

| Cột           | Kiểu dữ liệu | Mô tả                           |
| ------------- | ------------ | ------------------------------- |
| id            | UUID         | Khóa chính, tự động sinh        |
| phone_number  | VARCHAR(15)  | Số điện thoại, unique, bắt buộc |
| email         | VARCHAR(255) | Email, unique, có thể null      |
| full_name     | VARCHAR(255) | Họ tên đầy đủ, bắt buộc         |
| date_of_birth | DATE         | Ngày sinh                       |
| gender        | gender       | Giới tính (enum)                |
| status        | user_status  | Trạng thái tài khoản            |
| password_hash | VARCHAR(255) | Mật khẩu đã được hash           |
| created_at    | TIMESTAMP    | Thời điểm tạo                   |
| updated_at    | TIMESTAMP    | Thời điểm cập nhật cuối         |

### 2. wallets

Quản lý ví điện tử của người dùng.

| Cột        | Kiểu dữ liệu  | Mô tả                        |
| ---------- | ------------- | ---------------------------- |
| id         | UUID          | Khóa chính, tự động sinh     |
| user_id    | UUID          | Khóa ngoại tới bảng users    |
| balance    | DECIMAL(19,4) | Số dư hiện tại               |
| currency   | VARCHAR(3)    | Loại tiền tệ (mặc định: VND) |
| status     | user_status   | Trạng thái ví                |
| created_at | TIMESTAMP     | Thời điểm tạo                |
| updated_at | TIMESTAMP     | Thời điểm cập nhật cuối      |

### 3. transaction_types

Định nghĩa các loại giao dịch trong hệ thống.

| Cột         | Kiểu dữ liệu | Mô tả                     |
| ----------- | ------------ | ------------------------- |
| id          | SERIAL       | Khóa chính, tự tăng       |
| code        | VARCHAR(50)  | Mã loại giao dịch, unique |
| name        | VARCHAR(100) | Tên loại giao dịch        |
| description | TEXT         | Mô tả chi tiết            |
| created_at  | TIMESTAMP    | Thời điểm tạo             |

### 4. payment_methods

Quản lý các phương thức thanh toán.

| Cột         | Kiểu dữ liệu | Mô tả                   |
| ----------- | ------------ | ----------------------- |
| id          | SERIAL       | Khóa chính, tự tăng     |
| code        | VARCHAR(50)  | Mã phương thức, unique  |
| name        | VARCHAR(100) | Tên phương thức         |
| description | TEXT         | Mô tả chi tiết          |
| status      | user_status  | Trạng thái              |
| created_at  | TIMESTAMP    | Thời điểm tạo           |
| updated_at  | TIMESTAMP    | Thời điểm cập nhật cuối |

### 5. beneficiaries

Danh sách người thụ hưởng (người nhận tiền).

| Cột                      | Kiểu dữ liệu | Mô tả                            |
| ------------------------ | ------------ | -------------------------------- |
| id                       | UUID         | Khóa chính, tự động sinh         |
| user_id                  | UUID         | Khóa ngoại tới người dùng sở hữu |
| beneficiary_name         | VARCHAR(255) | Tên người thụ hưởng              |
| beneficiary_phone        | VARCHAR(15)  | Số điện thoại                    |
| beneficiary_bank_code    | VARCHAR(20)  | Mã ngân hàng                     |
| beneficiary_bank_account | VARCHAR(50)  | Số tài khoản                     |
| beneficiary_bank_branch  | VARCHAR(255) | Chi nhánh ngân hàng              |
| is_favorite              | BOOLEAN      | Đánh dấu yêu thích               |
| created_at               | TIMESTAMP    | Thời điểm tạo                    |
| updated_at               | TIMESTAMP    | Thời điểm cập nhật cuối          |

### 6. transactions

Lưu trữ thông tin các giao dịch.

| Cột                 | Kiểu dữ liệu       | Mô tả                    |
| ------------------- | ------------------ | ------------------------ |
| id                  | UUID               | Khóa chính, tự động sinh |
| transaction_type_id | INTEGER            | Loại giao dịch           |
| payment_method_id   | INTEGER            | Phương thức thanh toán   |
| sender_id           | UUID               | Người gửi                |
| receiver_id         | UUID               | Người nhận               |
| sender_wallet_id    | UUID               | Ví nguồn                 |
| receiver_wallet_id  | UUID               | Ví đích                  |
| amount              | DECIMAL(19,4)      | Số tiền giao dịch        |
| currency            | VARCHAR(3)         | Loại tiền tệ             |
| fee_amount          | DECIMAL(19,4)      | Phí giao dịch            |
| status              | transaction_status | Trạng thái giao dịch     |
| description         | TEXT               | Mô tả giao dịch          |
| reference_number    | VARCHAR(100)       | Mã tham chiếu, unique    |
| created_at          | TIMESTAMP          | Thời điểm tạo            |
| updated_at          | TIMESTAMP          | Thời điểm cập nhật cuối  |

### 7. notifications

Quản lý thông báo cho người dùng.

| Cột            | Kiểu dữ liệu | Mô tả                    |
| -------------- | ------------ | ------------------------ |
| id             | UUID         | Khóa chính, tự động sinh |
| user_id        | UUID         | Người nhận thông báo     |
| transaction_id | UUID         | Giao dịch liên quan      |
| title          | VARCHAR(255) | Tiêu đề thông báo        |
| message        | TEXT         | Nội dung thông báo       |
| is_read        | BOOLEAN      | Trạng thái đã đọc        |
| created_at     | TIMESTAMP    | Thời điểm tạo            |

## Indexes

Database sử dụng các index sau để tối ưu hiệu năng truy vấn:

1. `idx_users_phone_number`: Index trên số điện thoại người dùng
2. `idx_users_email`: Index trên email người dùng
3. `idx_transactions_created_at`: Index theo thời gian tạo giao dịch
4. `idx_transactions_status`: Index theo trạng thái giao dịch
5. `idx_transactions_sender_id`: Index theo người gửi
6. `idx_transactions_receiver_id`: Index theo người nhận
7. `idx_notifications_user_id`: Index theo người nhận thông báo
8. `idx_beneficiaries_user_id`: Index theo người sở hữu danh sách thụ hưởng
