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

# ───── FORCE FAKE FRAUD FOR TESTING ─────
fraud_rows = pd.DataFrame({
    "transaction_id": ["TXF001", "TXF002", "TXF003"],
    "account_id": ["A999"] * 3,
    "timestamp": [
        "2025-06-10T10:00:00",
        "2025-06-10T10:01:00",
        "2025-06-10T10:02:00"
    ],
    "amount": [9999, 8888, 7777],
    "currency": ["EUR"] * 3,
    "description": ["suspicious transfer"] * 3,
    "counterparty_name": ["FAKECO"] * 3,
    "counterparty_iban": ["FAKEIBAN123"] * 3,
    "category": ["crypto"] * 3,
    "payment_type": ["single"] * 3
})

df_fake = pd.concat([df_fake, fraud_rows], ignore_index=True)

# Save to CSV
output_path = "data/transactions_demo.csv"
df_fake.to_csv(output_path, index=False)

output_path
