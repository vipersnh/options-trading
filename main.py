import pdb
import matplotlib.pyplot as plt
import numpy as np
import random
import collections

## Current Setup of ~10 delta strangles
#win_rate = 90/100
#rw_to_cr_ratio = 1/2 # 50% profit target
#cr_to_sl_ratio = 1/1.5 # 150% SL of the credit received
#rr_ratio = rw_to_cr_ratio*cr_to_sl_ratio # Reward/Risk ratio
#max_risk_per_trade = 5/100 # Max Loss as % of account size
#max_risk_all_trades = 15/100
#uncorrelated_parallel_trades = int(max_risk_all_trades/max_risk_per_trade)
#account_size = 20*1000
#average_trade_duration = 14

## Higher delta of ~20 delta strangles
#win_rate = 80/100
#rw_to_cr_ratio = 1/2 # 50% profit target
#cr_to_sl_ratio = 1/1 # 150% SL of the credit received
#rr_ratio = rw_to_cr_ratio*cr_to_sl_ratio # Reward/Risk ratio
#max_risk_per_trade = 5/100 # Max Loss as % of account size
#max_risk_all_trades = 15/100
#uncorrelated_parallel_trades = int(max_risk_all_trades/max_risk_per_trade)
#account_size = 20*1000
#average_trade_duration = 14

# Straddle setup 
win_rate = 50/100
rw_to_cr_ratio = 0.5/1 # 50% profit target
cr_to_sl_ratio = 0.3/1 # 100% SL of the credit received
rr_ratio = rw_to_cr_ratio/cr_to_sl_ratio
max_risk_per_trade = 3/100
max_risk_all_trades = 10/100
uncorrelated_parallel_trades = int(max_risk_all_trades/max_risk_per_trade)
account_size = 10000
average_trade_duration = 14
print("Straddle Parameters")
print("Reward to Credit Ratio : {0:.2f}%".format(rw_to_cr_ratio*100))
print("Credit to SL Ratio : {0:.2f}%".format(cr_to_sl_ratio*100))
print("Reward/Risk Ratio : {0:.2f}%".format(rr_ratio*100))

def get_account_samples(seed, win_rate, rr_ratio, max_risk, account_size, average_trade_duration, parallel_trades):
    trades_count = int(365/average_trade_duration)
    population = [-1, rr_ratio]
    weights = [1-win_rate, win_rate]
    random.seed(seed)
    parallel_samples = list()
    for symbol in range(parallel_trades):
        samples = random.choices([0, 1], weights, k=trades_count)
        parallel_samples.append(samples)

    account_value = account_size
    account_samples = [account_size]

    trades_by_symbol = [[] for _ in range(parallel_trades)]
    for index in range(trades_count):
        account_samples.append(account_value)
        for trade in range(parallel_trades):
            sample = parallel_samples[trade][index]
            win_loss = account_size*max_risk*population[sample]
            account_value += win_loss
            trades_by_symbol[trade].append(win_loss)
    
    return [account_value, account_samples, trades_by_symbol]

def ascii_histogram(seq) -> None:
    """A horizontal frequency-table/histogram plot."""
    counted = collections.Counter(seq)
    for k in sorted(counted):
        print('{0:5d}% {1}'.format(k, '+' * counted[k]))

trial_count = 100

annual_gain_average = 0
annual_gains = []
for seed in range(trial_count):
    [account_value, account_samples, trades_by_symbol] = get_account_samples(seed, win_rate, rr_ratio, max_risk_per_trade, account_size, average_trade_duration, uncorrelated_parallel_trades)
    print("Annual Gain : {0:.1f}%".format((account_value-account_size)/account_size*100))
    annual_gain = int((account_value-account_size)/account_size*100)
    annual_gains.append(annual_gain)
    annual_gain_average += annual_gain

print("Number of parallel trades : {0}".format(uncorrelated_parallel_trades))
ascii_histogram(annual_gains)

#print("Annaul Gain Average : {0:.2f}".format(annual_gain_average/trial_count))

#plt.plot(range(len(account_samples)), account_samples)
#plt.show()


