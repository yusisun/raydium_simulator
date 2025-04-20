# raydium_simulator/config/base_config.py
def default_config():
    return {
        "entry_rate": 10,
        "max_time": 30,
        "curve_type": "logarithmic",
        "curve_params": {
            "base_price": 0.01,
            "scale": 0.03
        },
        "lp_token": 10_000_000,
        "lp_sol": 50,
        "to_lp": True,
        "platform_lp_split": 0.1,
        "user_behavior": "fomo",
        "vesting_ratio": 0.10,
        "vesting_duration": 3,
        "target_raise": 30  # Stop selling when this amount of SOL is raised
    }