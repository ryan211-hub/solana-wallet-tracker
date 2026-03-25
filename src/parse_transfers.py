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

SYSTEM_PROGRAM = "11111111111111111111111111111111"


def parse_native_transfer(tx):

    result = []

    if tx is None:
        return result

    message = tx.get("transaction", {}).get("message", {})
    instructions = message.get("instructions", [])
    account_keys = message.get("accountKeys", [])

    for ins in instructions:

        program_idx = ins.get("programIdIndex")
        program_id = account_keys[program_idx]

        # 只处理 system program
        if program_id != SYSTEM_PROGRAM:
            continue

        accounts = ins.get("accounts", [])

        # system transfer 一般是两个账户
        if len(accounts) < 2:
            continue

        from_addr = account_keys[accounts[0]]
        to_addr = account_keys[accounts[1]]

        # ⚠️ 这里先不解析 amount（因为需要 decode data）
        result.append({
            "from": from_addr,
            "to": to_addr,
            "note": "system transfer detected"
        })

    return result