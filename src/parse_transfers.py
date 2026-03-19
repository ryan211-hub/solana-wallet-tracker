import base64


def decode_system_transfer(data_base64):

    raw = base64.b64decode(data_base64)

    # 至少要 12 字节
    if len(raw) < 12:
        return None

    # 前4字节是 instruction id
    instruction_type = int.from_bytes(raw[0:4], "little")

    # 2 = transfer
    if instruction_type != 2:
        return None

    # 后8字节是 amount
    lamports = int.from_bytes(raw[4:12], "little")

    return lamports



def parse_sol_transfer(tx):

    result = []

    if tx is None:
        return result

    meta = tx.get("meta")
    message = tx.get("transaction", {}).get("message", {})

    if not meta or not message:
        return result

    pre_balances = meta.get("preBalances", [])
    post_balances = meta.get("postBalances", [])
    accounts = message.get("accountKeys", [])

    fee = meta.get("fee", 0)

    for i in range(len(accounts)):

        pre = pre_balances[i]
        post = post_balances[i]

        diff = post - pre

        if diff == 0:
            continue

        address = accounts[i]

        # 过滤手续费（通常是负数且等于 fee）
        if diff == -fee:
            continue

        result.append({
            "address": address,
            "change": diff
        })

    return result