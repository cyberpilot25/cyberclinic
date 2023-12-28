import csv
import random
from datetime import datetime, timedelta

def generate_synthetic_data(num_accounts_per_code, num_transactions, output_file):
    currencies = ['INR', 'USD', 'AUD', 'CAD', 'GBP', 'BTC', 'JPY', 'EUR', 'MXN', 'DINAR']
    payment_formats = ['Credit card', 'Reinvestment', 'ACH', 'BTC', 'cheque', 'cash', 'wire']
    num_bank_codes = 10
    total_unique_accounts = 500

    # Create a pool of unique account numbers
    account_numbers_pool = list(range(10023495, 10023495 + total_unique_accounts))

    start_date = datetime(2023, 6, 1)
    end_date = start_date + timedelta(days=75)

    transactions = []

    for bank_code in range(1, num_bank_codes + 1):
        # Ensure each bank code has 50 unique account numbers
        bank_accounts = random.sample(account_numbers_pool, num_accounts_per_code)
        account_numbers_pool = list(set(account_numbers_pool) - set(bank_accounts))

        for _ in range(num_transactions // num_bank_codes):
            for sender_account_number in bank_accounts:
                timestamp = start_date + timedelta(days=random.randint(0, 75),
                                                   hours=random.randint(0, 23),
                                                   minutes=random.randint(0, 59),
                                                   seconds=random.randint(0, 59))
                receiver_bank_code = random.choice(range(1, num_bank_codes + 1))
                # Ensure receiver account is different from sender account
                receiver_account_number = random.choice(list(set(bank_accounts) - {sender_account_number}))
                currency = random.choice(currencies)
                payment_format = random.choice(payment_formats)

                # Fix payment currency and format for BTC transactions
                if currency == 'BTC':
                    payment_format = 'BTC'

                amount = round(random.uniform(0.0001, 2), 6) if currency == 'BTC' else round(random.uniform(10.0, 100000.0), 2)
                is_laundered = random.choice([0, 1])

                transactions.append({
                    'Transaction timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'Sender bank code': bank_code,
                    'Sender bank a/c number': sender_account_number,
                    'Receiver bank code': receiver_bank_code,
                    'Receiver bank a/c number': receiver_account_number,
                    'Payment currency': currency,
                    'Payment format': payment_format,
                    'Transaction amount': amount,
                    'Is laundered': is_laundered,
                })

    # Shuffle the transactions
    random.shuffle(transactions)

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Transaction timestamp', 'Sender bank code', 'Sender bank a/c number',
                      'Receiver bank code', 'Receiver bank a/c number', 'Payment currency',
                      'Payment format', 'Transaction amount', 'Is laundered']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for transaction in transactions:
            writer.writerow(transaction)

if __name__ == "__main__":
    num_accounts_per_code = 50
    num_transactions = 1000
    output_file = 'H:/College/Fall 23-24/Cyber clinic/Dataset/dataset.csv'

    generate_synthetic_data(num_accounts_per_code, num_transactions, output_file)
    print(f"Synthetic dataset generated and saved to {output_file}")
