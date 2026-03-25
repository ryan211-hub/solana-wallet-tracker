from fetch_transactions import get_signatures, get_transaction
from parse_transfers import parse_native_transfer

wallet = "CoPyPPWdm8SirumaAEe8S68nSJpHYhguN2L5i2YGxLB"

txs = get_signatures(wallet)

for tx in txs:

    sig = tx["signature"]

    full_tx = get_transaction(sig)

    transfers = parse_native_transfer(full_tx)
    print("raw transfers:", transfers)

    print("SIGNATURE:", sig)

    for t in transfers:
        print(t)