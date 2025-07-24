import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
Faker.seed(42)
np.random.seed(42)

# Define number of fake transactions
num_transactions = 100

# Generate fake data
timestamps = pd.date_range(start="2025-06-01", periods=num_transactions, freq="6h")
amounts = np.random.randint(50, 10000, size=num_transactions)

data = {
    "transaction_id": [f"TX{str(i).zfill(4)}" for i in range(1, num_transactions + 1)],
    "account_id": np.random.choice(["A001", "A002", "A003"], size=num_transactions),
    "timestamp": timestamps,
    "amount": amounts,
    "currency": "EUR",
    "description": [fake.sentence(nb_words=3) for _ in range(num_transactions)],
    "counterparty_name": [fake.company() for _ in range(num_transactions)],
    "counterparty_iban": [fake.iban() for _ in range(num_transactions)],
    "category": np.random.choice(["crypto", "shopping", "travel", "health", "food", "utilities"], size=num_transactions),
    "payment_type": np.random.choice(["single", "bulk"], size=num_transactions)
}

df_fake = pd.DataFrame(data)

# Save to CSV
output_path = "data/transactions_demo.csv"
df_fake.to_csv(output_path, index=False)

output_path