import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import random
import os

# Seed for reproducibility
random.seed(42)

# Initialize Faker with a specific seed for consistency
fake = Faker()
Faker.seed(42)

# Function to generate a random timestamp within a given date range
def generate_random_timestamp(start_date, end_date):
    seconds_difference = int((end_date - start_date).total_seconds())
    random_seconds = random.randint(0, seconds_difference)
    timestamp = start_date + timedelta(seconds=random_seconds)

    # Ensure the generated timestamp is within the specified range
    timestamp = min(end_date, max(start_date, timestamp))

    return timestamp.strftime('%d/%m/%Y %H:%M:%S')

# Function to generate random account age in years
def generate_random_account_age():
    return round(random.uniform(0, 10), 1)

# Generate dataset
transactions_per_bank = 10000 #number of transactions per bank
num_unique_accounts = 500 #number of unique a/c
start_date = datetime(2023, 10, 8)
end_date = start_date + timedelta(days=7)#set number of days for transaction period

data = []

# Define account number ranges for each bank
account_number_ranges = {
    1: (10005670, 10005721),
    2: (20004542, 20004593),
    3: (30009800, 30009851),
    4: (40004510, 40004561),
    5: (50009520, 50009571),
    6: (60002475, 60002526),
    7: (70003605, 70003656),
    8: (80001806, 80001857),
    9: (90006723, 90006774),
    10: (11001406, 11001457),
}

# Create a dictionary to keep track of used account numbers for each bank
used_account_numbers_by_bank = {bank: set() for bank in range(1, 11)}

#generate unique account numbers
def generate_unique_account_numbers_for_bank(bank, num_accounts):
    account_number_range = account_number_ranges[bank]
     # Choose every other account number except starting and ending numbers
    available_account_numbers = list(range(account_number_range[0], account_number_range[1]))[:-1]

    # Ensure we have enough available account numbers
    if len(available_account_numbers) < num_accounts:
        raise ValueError("Not enough available account numbers for bank {}.".format(bank))
    
    unique_account_numbers = random.sample(available_account_numbers, num_accounts)
    used_account_numbers_by_bank[bank].update(unique_account_numbers)
    return unique_account_numbers

#generate unique accounts
for bank_code in range(1, 11):
    num_accounts = 50  # number of unique accounts in each bank
    generate_unique_account_numbers_for_bank(bank_code, num_accounts)

#function to calculate risk score
def calculate_realistic_risk_score(sender_account_age, receiver_account_age, sender_country, receiver_country, amount_transacted, payment_format, transaction_type):
    # Your logic to calculate risk score based on the specified features
    # Add your own calculations based on the provided features
    base_risk_score = 0.8  # Default base risk score
    
    #based on country involved
    if sender_country or receiver_country == 'Afghanistan':
        base_risk_score += 1.0
    elif sender_country or receiver_country == 'Germany':
        base_risk_score -= 0.4
    elif sender_country or  receiver_country == 'India':
        base_risk_score += 0.6
    elif sender_country or  receiver_country == 'UK':
        base_risk_score -= 0.4
    else:
        #sender_country or receiver_country == 'USA':
        base_risk_score += 0.4
    
    #based on account age
    if (sender_account_age or receiver_account_age) <= 2.5:
        base_risk_score += 0.6
    elif 2.6 < (sender_account_age or receiver_account_age) <= 4:
        base_risk_score += 0.2
    elif 4.1 < (sender_account_age or receiver_account_age) <= 6:
        base_risk_score += 0.0
    elif 6.1 < (sender_account_age or receiver_account_age) <= 8:
        base_risk_score -= 0.2
    else:
    #8.1 < (sender_account_age or receiver_account_age) <= 10:
        base_risk_score -=0.3
        
    #based on transaction amount    
    if  300 <= amount_transacted == 10000:
        base_risk_score -= 0.5
    elif  10001 >= amount_transacted == 50000:
        base_risk_score += 0.5
    else:
        #amount_transacted >=50001 or amount_transacted = 100000:
        base_risk_score += 0.8
    
    #based on payment format
    if payment_format == 'Cash':
        base_risk_score += 1.0
    elif payment_format =='Cheque':
        base_risk_score += 0.6
    elif payment_format =='Credit card':
        base_risk_score += 0.6
    elif payment_format =='Reinvestment':
        base_risk_score -= 0.5
    elif payment_format =='Wire':
        base_risk_score -= 0.8
    else:
        #payment_format =='ACH':
        base_risk_score -= 0.6
    
    #based on transaction type:
    if transaction_type == 'International':
        base_risk_score += 0.6
    else:
        #transaction_type == 'Domestic':
        base_risk_score -= 0.2
    
    # Ensure the risk score is within the valid range of 0 to 5
    return max(0, min(4.8, base_risk_score))

#Generate transactions
num_transactions_per_account = 200 #number of transactions per a/c
#transactions_per_bank = 10000 # number of transactions per bank
for sender_bank_code in range(1, 11):
    sender_country_mapping = {
        1: 'India',
        2: 'India',
        3: 'Afghanistan',
        4: 'Afghanistan',
        5: 'Germany',
        6: 'Germany',
        7: 'UK',
        8: 'UK',
        9: 'USA',
        10: 'USA',
    }
    sender_country = sender_country_mapping[sender_bank_code]

    for sender_account_number in used_account_numbers_by_bank[sender_bank_code]:
        sender_account_age = generate_random_account_age()  # Add sender account age
        for _ in range(num_transactions_per_account):
            timestamp_str = generate_random_timestamp(start_date, end_date)
            
            # Determine the bank for the receiver
            receiver_bank_code = fake.random_element(elements=range(1, 11))
            receiver_country = sender_country_mapping[receiver_bank_code]

            # Generate unique account number for the receiver
            num_receiver_accounts = 1
            receiver_account_numbers = generate_unique_account_numbers_for_bank(receiver_bank_code, num_receiver_accounts)
            receiver_account_number = receiver_account_numbers[0]
            receiver_account_age = generate_random_account_age()  # Add receiver account age

            # Ensure sender country and payment currency match
            payment_currency_mapping = {
                'India': 'INR',
                'USA': 'USD',
                'Germany': 'EUR',
                'Afghanistan': 'AFN',
                'UK': 'GBP'
            }
            payment_currency = payment_currency_mapping[sender_country]
            
            # add payment format and transaction amount
            payment_format = fake.random_element(elements=('Cheque', 'Credit Card', 'Reinvestment', 'ACH', 'Cash', 'Wire'))
            amount_transacted = round(random.uniform(300, 100000), 2) #set transaction amount range
            
            # Add Transaction Type as int or domestic
            transaction_type = 'Domestic' if sender_country == receiver_country else 'International'
            
            # Calculate realistic risk score
            risk_score = calculate_realistic_risk_score(sender_account_age, receiver_account_age, sender_country, receiver_country, amount_transacted, payment_format, transaction_type)
            is_laundered = fake.random_int(min=0, max=1)

            data.append([timestamp_str, sender_country, sender_bank_code, sender_account_number, sender_account_age,
                         receiver_country, receiver_bank_code, receiver_account_number, receiver_account_age,
                         payment_format, payment_currency, amount_transacted, transaction_type, risk_score, is_laundered])
                       
# Create DataFrame
columns = ['Timestamp', 'Sender_country', 'Sender_bank_code', 'Sender_a/c_number', 'Sender_a/c_age',
           'Receiver_country', 'Receiver_bank_code', 'Receiver_a/c_number', 'Receiver_a/c_age',
           'Payment_format', 'Payment currency', 'Amount_transacted', 'Transaction_type', 'Risk_score', 'Is_Laundered']

df = pd.DataFrame(data, columns=columns)

# Save DataFrame to a CSV file
df = df.sample(frac=1).reset_index(drop=True) #shuffles transactions
#df.to_csv("generated_dataset.csv", index=False) #saves the output in csv format in same folder

#saves file in downloads folder
output_file_path = os.path.join(os.path.expanduser("~"), "Downloads", "generated_dataset.csv")
df.to_csv(output_file_path, index=False)