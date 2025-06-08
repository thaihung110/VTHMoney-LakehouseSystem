-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE user_status AS ENUM ('active', 'inactive', 'blocked', 'pending');
CREATE TYPE gender AS ENUM ('male', 'female', 'other');
CREATE TYPE transaction_status AS ENUM ('pending', 'completed', 'failed', 'cancelled');
CREATE TYPE kyc_status AS ENUM ('unverified', 'pending', 'verified', 'rejected');

-- Create tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    gender gender,
    status user_status DEFAULT 'pending',
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_kyc (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    id_type VARCHAR(50) NOT NULL,
    id_number VARCHAR(50) NOT NULL,
    id_issue_date DATE,
    id_expiry_date DATE,
    front_image_url TEXT,
    back_image_url TEXT,
    selfie_image_url TEXT,
    status kyc_status DEFAULT 'unverified',
    verified_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, id_type, id_number)
);

CREATE TABLE wallets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    balance DECIMAL(19,4) DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'VND',
    status user_status DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, currency)
);

CREATE TABLE transaction_types (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payment_methods (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    status user_status DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE beneficiaries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    beneficiary_name VARCHAR(255) NOT NULL,
    beneficiary_phone VARCHAR(15),
    beneficiary_bank_code VARCHAR(20),
    beneficiary_bank_account VARCHAR(50),
    beneficiary_bank_branch VARCHAR(255),
    is_favorite BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_type_id INTEGER,
    payment_method_id INTEGER,
    sender_id UUID,
    receiver_id UUID,
    sender_wallet_id UUID,
    receiver_wallet_id UUID,
    amount DECIMAL(19,4) NOT NULL,
    currency VARCHAR(3) DEFAULT 'VND',
    fee_amount DECIMAL(19,4) DEFAULT 0,
    status transaction_status DEFAULT 'pending',
    description TEXT,
    reference_number VARCHAR(100) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    transaction_id UUID,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


-- Create indexes
CREATE INDEX idx_users_phone_number ON users(phone_number);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_sender_id ON transactions(sender_id);
CREATE INDEX idx_transactions_receiver_id ON transactions(receiver_id);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_beneficiaries_user_id ON beneficiaries(user_id);

ALTER TABLE public.users REPLICA IDENTITY FULL;
ALTER TABLE public.wallets REPLICA IDENTITY FULL;
ALTER TABLE public.transactions REPLICA IDENTITY FULL;
ALTER TABLE public.notifications REPLICA IDENTITY FULL;
ALTER TABLE public.beneficiaries REPLICA IDENTITY FULL;

-- Insert some initial data
INSERT INTO transaction_types (id, code, name, description) VALUES
    (1, 'DEPOSIT', 'Nạp tiền', 'Nạp tiền vào ví VTH Money'),
    (2,'WITHDRAW', 'Rút tiền', 'Rút tiền từ ví VTH Money'),
    (3,'TRANSFER', 'Chuyển tiền', 'Chuyển tiền giữa các ví VTH Money'),
    (4,'PAYMENT', 'Thanh toán', 'Thanh toán hóa đơn/dịch vụ qua VTH Money'),
    (5,'REFUND', 'Hoàn tiền', 'Hoàn tiền giao dịch VTH Money'),
    (6,'MOBILE_TOPUP', 'Nạp điện thoại', 'Nạp tiền điện thoại qua VTH Money'),
    (7,'BILL_PAYMENT', 'Thanh toán hóa đơn', 'Thanh toán các loại hóa đơn qua VTH Money');

INSERT INTO payment_methods (id, code, name, description) VALUES
    (1, 'VTH_WALLET', 'Ví VTH Money', 'Thanh toán qua ví VTH Money'),
    (2, 'BANK_TRANSFER', 'Chuyển khoản', 'Chuyển khoản ngân hàng liên kết'),
    (3, 'CREDIT_CARD', 'Thẻ tín dụng', 'Thanh toán bằng thẻ tín dụng qua VTH Money'),
    (4, 'DEBIT_CARD', 'Thẻ ghi nợ', 'Thanh toán bằng thẻ ghi nợ qua VTH Money'),
    (5, 'LINKED_BANK', 'Tài khoản ngân hàng', 'Tài khoản ngân hàng liên kết với VTH Money');
