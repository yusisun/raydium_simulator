# Raydium Launch Simulation Framework



## Purpose
This repository provides a quantitative simulation framework for analyzing token launch mechanisms on Raydium, particularly contrasting:

- **LaunchLab**: Raydium's upcoming customizable token issuance platform.
- **JustSendIt**: A simplified, linear, Pump.fun-style issuance with no vesting or LP incentives.

Our objective is to evaluate which launch configuration maximizes:
- Protocol revenue (platform earnings)
- LP incentives (liquidity sustainability)
- Price path stability (user fairness)

---

## Model Architecture

The simulation models token sales over time using configurable parameters:

| Component            | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| **Bonding Curve**   | Supports `linear`, `logarithmic`, and `exponential` pricing strategies       |
| **Buyer Arrival**   | Simulates stochastic user participation over time                           |
| **Revenue Routing** | Splits inflows into protocol fee, LP incentive, and vesting lockups         |
| **Vesting Engine**  | Models deferred revenue unlock over multiple periods                        |
| **AMM Pool Logic**  | Optional LP migration and dynamic revenue sharing                           |

---

## Strategies Compared

Three issuance strategies were tested on identical buyer behavior assumptions:

| Strategy                           | Curve Type    | LP Incentive | Vesting      | Platform / LP Split |
|------------------------------------|---------------|--------------|--------------|----------------------|
| **LaunchLab (log)**                | Logarithmic   | ✅ Enabled    | 10% / 3 t     | 97% protocol / 3% LP |
| **JustSendIt (Pump.fun style)**    | Linear        | ❌ Disabled   | None          | 100% protocol        |
| **LaunchLab (exp, strong vesting)**| Exponential   | ✅ Enabled    | 20% / 5 t     | 97% protocol / 3% LP |

---

## Results Summary

| Strategy                           | Protocol Revenue | LP Revenue | Locked Revenue | Final Price | Buyers |
|------------------------------------|------------------|------------|----------------|-------------|--------|
| LaunchLab (log, vesting, LP)       | 0.1977           | 0.0120     | 0.3928         | 0.01187     | 510    |
| JustSendIt (linear, no LP)         | 0.0134           | 0.0000     | 0.0000         | 0.01102     | 510    |
| LaunchLab (exp, stronger vesting)  | **0.2076**       | 0.0093     | **0.8264**     | **0.01026** | 510    |

---

## Key Insights

- **LaunchLab far exceeds JustSendIt in protocol revenue** — up to **15x more** earnings with modest curve and vesting settings.
- **LP rewards are only possible via LaunchLab**. Without LP migration, JustSendIt generates zero sustainable liquidity incentives.
- **Vesting boosts protocol revenue and reduces volatility**. Stronger vesting (20%) led to the most stable price path.
- **JustSendIt is efficient for fast launches but fails to generate long-term value** for the Raydium ecosystem.

---

## Optimization Recommendations


**1. Bonding Curve**  
• *Side Effect*: Linear bonding curves lead to slow price appreciation, resulting in limited protocol revenue.  
• *Optimization*: Use logarithmic or exponential bonding curves to increase marginal price with supply.  
• *Improvement*: Captures more value from late-stage buyers, boosting revenue without deterring early participants.

**2. LP Migration**  
• *Side Effect*: No LP migration reduces long-term liquidity and disincentivizes LP participation.  
• *Optimization*: Enable `to_lp=True` with 5–10% of funds migrated into LP pools.  
• *Improvement*: Enhances post-launch liquidity, reduces slippage, and aligns incentives between protocol and LPs.

**3. Vesting Ratio**  
• *Side Effect*: Immediate unlock of all funds enables aggressive sell-off, causing price instability.  
• *Optimization*: Apply 10–20% vesting with 3–6 time-period unlock schedules.  
• *Improvement*: Smooths post-launch sell pressure, increases protocol revenue retention, and fosters long-term engagement.

**4. Curve Steepness**  
• *Side Effect*: Excessively steep exponential curves may discourage later buyers due to high entry costs.  
• *Optimization*: Calibrate growth rate to maintain a balance between early incentives and late-stage accessibility.  
• *Improvement*: Prevents buyer attrition while preserving FOMO-based revenue gains.

**5. Liquidity Timing**  
• *Side Effect*: Migrating funds to LP too early may incur impermanent loss before price discovery stabilizes.  
• *Optimization*: Allow LP migration to begin post-raise or at a pre-defined liquidity trigger.  
• *Improvement*: Minimizes IL risk, encourages LP participation, and aligns liquidity provision with active trading phases.

**6. Adaptive Vesting**  
• *Side Effect*: Fixed vesting ignores market volatility and trading behavior.  
• *Optimization*: Implement unlock conditions based on price floors, TVL milestones, or daily volume triggers.  
• *Improvement*: Promotes healthy market behavior, incentivizes creator effort, and reduces manipulation risk.

**7. Creator Alignment**  
• *Side Effect*: Unconditional creator unlocks may lead to rug pulls or short-term behavior.  
• *Optimization*: Tie unlocks to protocol health metrics such as $RAY buybacks, on-chain volume, or verified LP depth.  
• *Improvement*: Aligns creator incentives with Raydium’s long-term ecosystem stability and trading growth.

###  Optimization Recommendations Summary

| Parameter         | Recommendation                                                  |
|------------------|------------------------------------------------------------------|
| **Bonding Curve** | Use log or exp for price stability and incentive alignment       |
| **LP Migration**  | Enable `to_lp=True` with 5–10% share to reward liquidity support |
| **Vesting Ratio** | Apply 10–20% vesting with 3–6 period unlock to reduce sell risk |
| **Curve Steepness** | Avoid overly steep exponential curves that deter retail participation; calibrate for participation and protocol value capture |
| **Liquidity Timing** | Allow delayed LP migration (e.g., post-raise) to minimize early impermanent loss and strengthen secondary liquidity |
| **Adaptive Vesting** | Consider vesting schedules that respond to price drawdowns or trading volume milestones |
| **Creator Alignment** | Introduce performance-based unlock or buyback triggers to align creator incentives with Raydium protocol health |

---

## Strategic Context: PumpSwap vs. LaunchLab

This simulation directly supports the real-world debate:
- **PumpSwap**: Fast, creator-centric, minimal protocol revenue, LP-heavy
- **LaunchLab**: Platform-driven, flexible, monetizable, long-term alignment

My simulation confirms that **Raydium can outperform PumpSwap in revenue and sustainability**, provided LaunchLab launches with the right set of customizable economic levers.

> _“If LaunchLab debuts soon with competitive features like low fees and flexible tokenomics, it could disrupt Pumpswap by offering a comprehensive solution under Raydium’s umbrella.”_

## Notebook & Code Overview

This project consists of modular components written in Python. Below is a brief description of each module or function to help you navigate the codebase:

### `main.py`
This is the main entry point. It runs either a single simulation using `default_config()` or a batch of simulations via `run_experiments()`.
- `run_simulation(config)`: Core simulation logic for one strategy. It simulates buyers, calculates prices via bonding curves, and tracks revenues.
- `plot_price_path(prices)`: Displays the price evolution throughout the simulation.
- `run_experiments()`: Compares multiple issuance configurations and prints a Markdown-formatted summary.

### `curve_engine.py`
Defines price curves based on token supply:
- `linear_curve(q, base_price, slope)`
- `logarithmic_curve(q, base_price, scale)`
- `exponential_curve(q, base_price, growth)`
These are used to model price appreciation under different bonding mechanisms.

### `agent_engine.py`
Controls buyer arrival and vesting lock logic:
- `simulate_buyers(entry_rate, max_time, behavior)`: Returns an array of buyer counts per timestep.
- `is_locked(q, config)`: Determines whether the transaction should be counted as locked (vested).

### `amm_module.py`
Models LP pool behavior:
- `AMMPool(lp_token, lp_sol)`: Initializes an LP pool, tracks liquidity allocation.

### `revenue_tracker.py`
Tracks earnings from the protocol’s perspective:
- `record_txn(price, to_lp, lp_split)`: Splits revenue among protocol, LP, and locked bucket.
- `record_locked(price)`: Registers locked revenue.
- `unlock_tokens(duration)`: Unlocks previously locked tokens over time.

### `config/base_config.py`
Houses the baseline configuration used for simulations:
- `default_config()`: Returns a dictionary containing default simulation parameters (curve type, fees, vesting, etc.)

## Author
This project was designed and developed by **Maggie Sun** from UC Berkeley Haas Financial Engineering, as part of a strategic research initiative inspired by Raydium’s evolving token launch infrastructure.