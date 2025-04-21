# raydium_simulator/main.py

from engine import curve_engine, agent_engine, amm_module, revenue_tracker
from config.base_config import default_config
import matplotlib.pyplot as plt
import pandas as pd


def run_simulation(config):
    tracker = revenue_tracker.RevenueTracker()
    pool = amm_module.AMMPool(config["lp_token"], config["lp_sol"])
    buyers = agent_engine.simulate_buyers(config["entry_rate"], config["max_time"], behavior=config["user_behavior"])

    total_q = 0
    prices = []
    sol_raised = 0

    for t, n in enumerate(buyers):
        for i in range(n):
            if config["target_raise"] and sol_raised >= config["target_raise"]:
                break

            if config["curve_type"] == "linear":
                price = curve_engine.linear_curve(total_q, **config["curve_params"])
            elif config["curve_type"] == "logarithmic":
                price = curve_engine.logarithmic_curve(total_q, **config["curve_params"])
            elif config["curve_type"] == "exponential":
                price = curve_engine.exponential_curve(total_q, **config["curve_params"])
            else:
                raise ValueError("Invalid curve type")

            if agent_engine.is_locked(total_q, config):
                tracker.record_locked(price)
            else:
                tracker.record_txn(price, to_lp=config["to_lp"], lp_split=config["platform_lp_split"])

            prices.append(price)
            total_q += 1
            sol_raised += price

    tracker.unlock_tokens(config["vesting_duration"])
    return prices, tracker


def plot_price_path(prices):
    plt.plot(prices)
    plt.title("Token Sale Price Curve")
    plt.xlabel("Buyer Index")
    plt.ylabel("Price (SOL)")
    plt.grid(True)
    plt.show()


# if __name__ == "__main__":
#     print("🚀 Starting simulation...")
#     config = default_config()
#     prices, tracker = run_simulation(config)
#     print("✅ Simulation finished.")
#     plot_price_path(prices)
#     print("📊 Protocol Revenue:", tracker.platform_fee)
#     print("📊 LP Revenue:", tracker.lp_fee)
#     print("📊 Locked Revenue:", tracker.locked_tokens)


def run_experiments():
    configs = [
        {
            "name": "LaunchLab (log, vesting, LP)",
            "config": default_config()
        },
        {
            "name": "JustSendIt (linear, no vesting, no LP)",
            "config": {
                **default_config(),
                "curve_type": "linear",
                "curve_params": {"base_price": 0.01, "slope": 0.000002},
                "to_lp": False,
                "vesting_ratio": 0.0,
                "platform_lp_split": 0.0
            }
        },
        {
            "name": "LaunchLab (exp, stronger vesting)",
            "config": {
                **default_config(),
                "curve_type": "exponential",
                "curve_params": {"base_price": 0.01, "growth": 0.00005},
                "vesting_ratio": 0.2,
                "vesting_duration": 5
            }
        }
    ]

    results = []
    for experiment in configs:
        name = experiment["name"]
        cfg = experiment["config"]
        prices, tracker = run_simulation(cfg)
        results.append({
            "Strategy": name,
            "Protocol Revenue": round(tracker.platform_fee, 4),
            "LP Revenue": round(tracker.lp_fee, 4),
            "Locked Revenue": round(tracker.locked_tokens, 4),
            "Final Price": round(prices[-1], 6),
            "Buyers": len(prices)
        })

    df = pd.DataFrame(results)
    print("\n==== Simulation Comparison Results ====")
    print(df.to_markdown(index=False))


if __name__ == "__main__":
    run_experiments()