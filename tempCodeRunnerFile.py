# raydium_simulator/main.py

from engine import curve_engine, agent_engine, amm_module, revenue_tracker
from config.base_config import default_config
import matplotlib.pyplot as plt


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


if __name__ == "__main__":
    config = default_config()
    prices, tracker = run_simulation(config)
    plot_price_path(prices)
    print("Protocol Revenue:", tracker.platform_fee)
    print("LP Revenue:", tracker.lp_fee)
    print("Locked Revenue:", tracker.locked_tokens)
