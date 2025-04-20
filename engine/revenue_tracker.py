# raydium_simulator/engine/revenue_tracker.py
class RevenueTracker:
    def __init__(self):
        self.platform_fee = 0
        self.lp_fee = 0
        self.locked_tokens = 0

    def record_txn(self, txn_amount, fee_rate=0.0025, to_lp=False, lp_split=0.0):
        fee = txn_amount * fee_rate
        if to_lp:
            lp_portion = fee * (1 - lp_split)
            self.lp_fee += lp_portion
            self.platform_fee += fee - lp_portion
        else:
            self.platform_fee += fee

    def record_locked(self, value):
        self.locked_tokens += value

    def unlock_tokens(self, vesting_duration):
        if vesting_duration > 0:
            unlocked = self.locked_tokens / vesting_duration
            self.platform_fee += unlocked
            self.locked_tokens -= unlocked
