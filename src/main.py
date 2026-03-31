from fetch_transactions import get_signatures, get_transaction
from parse_transfers import parse_token_transfer

wallet = "Hsma8UoBaoo2Unszj9DdwK6QWMYbc8b3zzsbLNHGVAce"

txs = get_signatures(wallet)

if not txs:
    print("Failed to get signatures or no transactions found")
    exit(1)

for tx in txs:

    sig = tx["signature"]
    print("main() : SIGNATURE:", sig)

    full_tx = get_transaction(sig)
    # print("main() : full_tx:", full_tx)
    if full_tx is None:
        print(f"Skipping {sig}: failed to fetch")
        continue

    transfers = parse_token_transfer(full_tx)
    print("main() : TOKEN TRANSFERS:", transfers)

    # for t in transfers:
    #     print(t)