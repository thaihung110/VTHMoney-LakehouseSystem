import os
import random
import string
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Set

import psycopg2

# Database connection configuration
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "vth_money"),
    "user": os.getenv("POSTGRES_USER", "admin"),
    "password": os.getenv("POSTGRES_PASSWORD", "admin"),
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}


def generate_phone():
    return f"0{''.join(random.choices(string.digits, k=9))}"


def generate_email():
    return f"user{''.join(random.choices(string.digits, k=5))}@example.com"


def generate_name():
    first_names = [
        "Nguyễn",
        "Trần",
        "Lê",
        "Phạm",
        "Hoàng",
        "Huỳnh",
        "Phan",
        "Vũ",
        "Võ",
        "Đặng",
    ]
    middle_names = [
        "Văn",
        "Thị",
        "Đức",
        "Minh",
        "Hoàng",
        "Thành",
        "Đình",
        "Xuân",
        "Hữu",
    ]
    last_names = [
        "An",
        "Bình",
        "Cường",
        "Dũng",
        "Em",
        "Phúc",
        "Giang",
        "Hùng",
        "Khang",
        "Linh",
    ]
    return f"{random.choice(first_names)} {random.choice(middle_names)} {random.choice(last_names)}"


class DataGenerator:
    def __init__(self):
        self.connect_with_retry()
        self.user_ids = set()
        self.wallet_ids = set()
        self.phone_numbers = set()
        self.emails = set()
        # Add counters for logging
        self.stats = {
            "users": 0,
            "wallets": 0,
            "transactions": 0,
            "notifications": 0,
            "beneficiaries": 0,
        }
        self.load_existing_data()

    def connect_with_retry(self, max_retries=5, delay=5):
        for attempt in range(max_retries):
            try:
                self.conn = psycopg2.connect(**DB_CONFIG)
                self.cur = self.conn.cursor()
                print("Successfully connected to database")
                return
            except psycopg2.OperationalError as e:
                if attempt == max_retries - 1:
                    raise e
                print(
                    f"Connection attempt {attempt + 1} failed, retrying in {delay} seconds..."
                )
                time.sleep(delay)

    def load_existing_data(self):
        print("Loading existing data...")
        # Load existing user IDs
        self.cur.execute("SELECT id FROM users")
        self.user_ids.update(row[0] for row in self.cur.fetchall())

        # Load existing wallet IDs
        self.cur.execute("SELECT id FROM wallets")
        self.wallet_ids.update(row[0] for row in self.cur.fetchall())

        # Load existing phone numbers
        self.cur.execute("SELECT phone_number FROM users")
        self.phone_numbers.update(row[0] for row in self.cur.fetchall())

        # Load existing emails
        self.cur.execute("SELECT email FROM users WHERE email IS NOT NULL")
        self.emails.update(row[0] for row in self.cur.fetchall())

        print(
            f"Loaded {len(self.user_ids)} users, {len(self.wallet_ids)} wallets"
        )

    def generate_unique_phone(self):
        while True:
            phone = generate_phone()
            if phone not in self.phone_numbers:
                self.phone_numbers.add(phone)
                return phone

    def generate_unique_email(self):
        while True:
            email = generate_email()
            if email not in self.emails:
                self.emails.add(email)
                return email

    def insert_user(self) -> str:
        user_id = str(uuid.uuid4())
        while user_id in self.user_ids:
            user_id = str(uuid.uuid4())

        query = """
        INSERT INTO users (id, phone_number, email, full_name, date_of_birth, gender, status, password_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        phone = self.generate_unique_phone()
        email = self.generate_unique_email()
        name = generate_name()
        user_data = (
            user_id,
            phone,
            email,
            name,
            datetime.now()
            - timedelta(days=random.randint(6570, 25550)),  # 18-70 years
            random.choice(["male", "female", "other"]),
            "active",
            "hashed_password_123",  # In real system, this would be properly hashed
        )
        self.cur.execute(query, user_data)
        self.conn.commit()
        self.user_ids.add(user_id)
        self.stats["users"] += 1
        print(
            f"✅ Inserted user: {name} (ID: {user_id[:8]}...) | Phone: {phone} | Email: {email}"
        )
        return user_id

    def insert_wallet(self, user_id: str) -> str:
        wallet_id = str(uuid.uuid4())
        while wallet_id in self.wallet_ids:
            wallet_id = str(uuid.uuid4())

        balance = random.uniform(100000, 10000000)
        query = """
        INSERT INTO wallets (id, user_id, balance, currency, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        wallet_data = (
            wallet_id,
            user_id,
            balance,
            "VND",
            "active",
        )
        self.cur.execute(query, wallet_data)
        self.conn.commit()
        self.wallet_ids.add(wallet_id)
        self.stats["wallets"] += 1
        print(
            f"💰 Created wallet: {wallet_id[:8]}... | Balance: {balance:,.0f} VND | User: {user_id[:8]}..."
        )
        return wallet_id

    def insert_transaction(
        self, sender_wallet_id: str, receiver_wallet_id: str
    ):
        transaction_id = str(uuid.uuid4())
        reference_number = f"TRX{int(time.time())}{random.randint(1000, 9999)}"

        # Check if reference number exists
        self.cur.execute(
            "SELECT 1 FROM transactions WHERE reference_number = %s",
            (reference_number,),
        )
        while self.cur.fetchone() is not None:
            reference_number = (
                f"TRX{int(time.time())}{random.randint(1000, 9999)}"
            )
            self.cur.execute(
                "SELECT 1 FROM transactions WHERE reference_number = %s",
                (reference_number,),
            )

        amount = random.uniform(10000, 1000000)
        query = """
        INSERT INTO transactions (
            id, transaction_type_id, payment_method_id,
            sender_wallet_id, receiver_wallet_id,
            amount, currency, fee_amount, status, description, reference_number
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        transaction_data = (
            transaction_id,
            random.randint(1, 5),  # Assuming we have 5 transaction types
            random.randint(1, 4),  # Assuming we have 4 payment methods
            sender_wallet_id,
            receiver_wallet_id,
            amount,
            "VND",
            amount * 0.001,  # 0.1% fee
            "completed",
            "Test transaction",
            reference_number,
        )
        self.cur.execute(query, transaction_data)
        self.conn.commit()
        self.stats["transactions"] += 1
        print(
            f"💸 New transaction: {reference_number} | Amount: {amount:,.0f} VND | From: {sender_wallet_id[:8]}... To: {receiver_wallet_id[:8]}..."
        )
        return transaction_id

    def insert_notification(self, user_id: str, transaction_id: str):
        notification_id = str(uuid.uuid4())
        query = """
        INSERT INTO notifications (id, user_id, transaction_id, title, message, is_read)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        notification_data = (
            notification_id,
            user_id,
            transaction_id,
            "Giao dịch thành công",
            "Giao dịch của bạn đã được thực hiện thành công",
            False,
        )
        self.cur.execute(query, notification_data)
        self.conn.commit()
        self.stats["notifications"] += 1
        print(
            f"🔔 Sent notification to user: {user_id[:8]}... | ID: {notification_id[:8]}..."
        )

    def insert_beneficiary(self, user_id: str):
        beneficiary_id = str(uuid.uuid4())
        query = """
        INSERT INTO beneficiaries (
            id, user_id, beneficiary_name, beneficiary_phone,
            beneficiary_bank_code, beneficiary_bank_account, beneficiary_bank_branch
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        bank_codes = ["VCB", "TCB", "ACB", "VPB", "MBB"]
        name = generate_name()
        phone = self.generate_unique_phone()
        bank_code = random.choice(bank_codes)
        account = "".join(random.choices(string.digits, k=10))

        beneficiary_data = (
            beneficiary_id,
            user_id,
            name,
            phone,
            bank_code,
            account,
            "Chi nhánh trung tâm",
        )
        self.cur.execute(query, beneficiary_data)
        self.conn.commit()
        self.stats["beneficiaries"] += 1
        print(
            f"👤 Added beneficiary: {name} | Bank: {bank_code} | Account: {account} | For user: {user_id[:8]}..."
        )

    # def update_user(self):
    #     if not self.user_ids:
    #         print("⚠️ No users to update")
    #         return

    #     user_id = random.choice(list(self.user_ids))
    #     query = """
    #     UPDATE users
    #     SET full_name = %s,
    #         gender = %s,
    #         status = %s
    #     WHERE id = %s
    #     RETURNING id, full_name;
    #     """
    #     new_name = generate_name()
    #     new_gender = random.choice(["male", "female", "other"])
    #     new_status = random.choice(["active", "blocked"])

    #     self.cur.execute(query, (new_name, new_gender, new_status, user_id))
    #     updated_user = self.cur.fetchone()
    #     self.conn.commit()
    #     print(
    #         f"✏️ Updated user {user_id[:8]}... | New name: {new_name} | New status: {new_status}"
    #     )

    # def update_wallet(self):
    #     if not self.wallet_ids:
    #         print("⚠️ No wallets to update")
    #         return

    #     wallet_id = random.choice(list(self.wallet_ids))
    #     query = """
    #     UPDATE wallets
    #     SET balance = balance + %s,
    #         status = %s
    #     WHERE id = %s
    #     RETURNING id, balance;
    #     """
    #     balance_change = random.uniform(-500000, 500000)
    #     new_status = random.choice(["active", "blocked"])

    #     self.cur.execute(query, (balance_change, new_status, wallet_id))
    #     updated_wallet = self.cur.fetchone()
    #     self.conn.commit()
    #     print(
    #         f"✏️ Updated wallet {wallet_id[:8]}... | Balance change: {balance_change:,.0f} VND | New status: {new_status}"
    #     )

    # def delete_beneficiary(self):
    #     # Get a random beneficiary
    #     self.cur.execute(
    #         "SELECT id, beneficiary_name FROM beneficiaries ORDER BY RANDOM() LIMIT 1"
    #     )
    #     beneficiary = self.cur.fetchone()

    #     if not beneficiary:
    #         print("⚠️ No beneficiaries to delete")
    #         return

    #     query = (
    #         "DELETE FROM beneficiaries WHERE id = %s AND beneficiary_name = %s"
    #     )
    #     self.cur.execute(query, (beneficiary[0], beneficiary[1]))
    #     self.conn.commit()
    #     print(
    #         f"🗑️ Deleted beneficiary: {beneficiary[1]} (ID: {beneficiary[0][:8]}...)"
    #     )

    # def delete_notification(self):
    #     # Delete read notifications that are older
    #     query = """
    #     DELETE FROM notifications
    #     WHERE is_read = true
    #     AND id IN (SELECT id FROM notifications WHERE is_read = true ORDER BY RANDOM() LIMIT 1)
    #     RETURNING id;
    #     """
    #     self.cur.execute(query)
    #     deleted = self.cur.fetchone()
    #     if deleted:
    #         self.conn.commit()
    #         print(f"🗑️ Deleted notification: {deleted[0][:8]}...")
    #     else:
    #         print("⚠️ No read notifications to delete")

    def run(self, duration_seconds: int = 30):
        start_time = time.time()
        print("\n🚀 Starting data generation process...")

        # First, create some initial users and wallets if needed
        if len(self.user_ids) < 10:
            print("\n📌 Creating initial users and wallets...")
            initial_count = 10 - len(self.user_ids)
            for _ in range(initial_count):
                user_id = self.insert_user()
                self.insert_wallet(user_id)

        print("\n🔄 Starting continuous insertion, updates, and deletions...")
        try:
            while time.time() - start_time < duration_seconds:
                try:
                    # Randomly choose what operation to perform
                    action = random.choice(
                        [
                            "insert_user",
                            # "insert_transaction",
                            # "insert_beneficiary",
                            # "insert_notification"
                            # "update_user",
                            # "update_wallet",
                            # "delete_beneficiary",
                            # "delete_notification",
                        ]
                    )

                    if action == "insert_user":
                        user_id = self.insert_user()
                        self.insert_wallet(user_id)
                    # if action == "insert_transaction":
                    #     if len(self.wallet_ids) >= 2:
                    #         sender, receiver = random.sample(
                    #             list(self.wallet_ids), 2
                    #         )
                    #         transaction_id = self.insert_transaction(
                    #             sender, receiver
                    #         )
                    # if action == "insert_beneficiary":
                    #     if self.user_ids:
                    #         user_id = random.choice(list(self.user_ids))
                    #         self.insert_beneficiary(user_id)
                    # if action == "insert_notification":
                    #     if self.user_ids:
                    #         user_id = random.choice(list(self.user_ids))
                    #         self.insert_notification(user_id, str(uuid.uuid4()))
                    # elif action == "update_user":
                    #     self.update_user()
                    # elif action == "update_wallet":
                    #     self.update_wallet()
                    # elif action == "delete_beneficiary":
                    #     self.delete_beneficiary()
                    # elif action == "delete_notification":
                    #     self.delete_notification()

                    time.sleep(
                        0.1
                    )  # Small delay to prevent overwhelming the database

                except Exception as e:
                    print(f"❌ Error: {e}")
                    self.conn.rollback()

        except KeyboardInterrupt:
            print("\n⚠️ Process interrupted by user")

        finally:
            # Print summary
            print("\n📊 Generation Summary:")
            print(f"✅ Users created: {self.stats['users']}")
            print(f"💰 Wallets created: {self.stats['wallets']}")
            print(f"💸 Transactions processed: {self.stats['transactions']}")
            print(f"🔔 Notifications sent: {self.stats['notifications']}")
            print(f"👤 Beneficiaries added: {self.stats['beneficiaries']}")
            print("\n✨ Data generation completed!")

            self.cur.close()
            self.conn.close()


if __name__ == "__main__":
    print("🔌 Starting data generator...")
    generator = DataGenerator()
    generator.run(duration_seconds=900)
