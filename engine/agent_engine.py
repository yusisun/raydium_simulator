# raydium_simulator/engine/agent_engine.py
def simulate_buyers(entry_rate, max_time, behavior="fomo"):
    if behavior == "fomo":
        return [int(entry_rate * (1 + 0.05 * t)) for t in range(max_time)]
    elif behavior == "uniform":
        return [entry_rate] * max_time
    else:
        raise ValueError("Unknown behavior type")

def is_locked(index, config):
    ratio = config.get("vesting_ratio", 0)
    return (index % int(1 / ratio)) == 0 if ratio > 0 else False