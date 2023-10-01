import pdb
import matplotlib.pyplot as plt
import numpy as np
import random
import collections

## Current Setup of ~10 delta strangles
#win_rate = 90/100
#reward_to_credit_ratio = 50/100 # 50% of credit as profit target
#stoploss_to_credit_ratio = 150/100 # 150% of credit as SL target
#rr_ratio = reward_to_credit_ratio/stoploss_to_credit_ratio # Reward/Risk ratio
#max_risk_per_trade = 5/100 # Max Loss as % of account size
#max_risk_all_trades = 15/100
#uncorrelated_parallel_trades = int(max_risk_all_trades/max_risk_per_trade)
#account_size = 20*1000
#average_trade_duration = 14

## Higher delta of ~20 delta strangles
#win_rate = 80/100
#reward_to_credit_ratio = 50/100 # 50% of credit as profit target
#stoploss_to_credit_ratio = 100/100 # 150% of credit as SL target
#rr_ratio = reward_to_credit_ratio/stoploss_to_credit_ratio # Reward/Risk ratio
#max_risk_per_trade = 5/100 # Max Loss as % of account size
#max_risk_all_trades = 15/100
#uncorrelated_parallel_trades = int(max_risk_all_trades/max_risk_per_trade)
#account_size = 10*1000
#average_trade_duration = 14

## Straddle setup 
win_rate = 50/100
reward_to_credit_ratio = 50/100 # 50% of credit as profit target
stoploss_to_credit_ratio = 30/100 # 30% of credit as SL target
rr_ratio = reward_to_credit_ratio/stoploss_to_credit_ratio # Reward/Risk ratio
max_risk_per_trade = 5/100 # Max Loss as % of account size
max_risk_all_trades = 15/100
uncorrelated_parallel_trades = int(max_risk_all_trades/max_risk_per_trade)
account_size = 10*1000
average_trade_duration = 14


print("Trading Parameters")
print()
print("Account Size : ${0}".format(account_size))
print("Win-Rate : {0:.2f}% and RR Ratio : {1:.2f}%".format(win_rate*100, rr_ratio*100))
print("Reward to Credit Ratio   : {0:.2f}%".format(reward_to_credit_ratio*100))
print("Stoploss to Credit Ratio : {0:.2f}%".format(stoploss_to_credit_ratio*100))
print("Maximum Risk : ${0:.2f}".format(max_risk_per_trade*account_size))
credit = 1000
rw = credit*reward_to_credit_ratio
sl = credit*stoploss_to_credit_ratio
print("For credit of ${0}, we'll have ${1} TP and ${2} SL limits".format(credit, int(rw), int(sl)))
print()

def get_account_samples(seed, win_rate, rr_ratio, max_risk, account_size, average_trade_duration, parallel_trades):
    trades_count = int(365/average_trade_duration)
    population = [-1, rr_ratio]
    weights = [1-win_rate, win_rate]
    random.seed(seed)
    print("For win-rate of {0:.2f}% and Reward/Risk of {1:.2f}, SL = ${2:.2f} and TP = ${3:.2f}".format(win_rate*100, rr_ratio, max_risk*account_size, max_risk*rr_ratio*account_size))
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
            win_loss = account_value*max_risk*population[sample]
            print("win_loss = ${0:4d}, total-account = ${1:.2f}".format(int(win_loss), account_value))
            account_value += win_loss
            trades_by_symbol[trade].append(win_loss)
    
    return [account_value, account_samples, trades_by_symbol]

def ascii_histogram(seq) -> None:
    """A horizontal frequency-table/histogram plot."""
    counted = collections.Counter(seq)
    for k in sorted(counted):
        print('{0:5d}% {1}'.format(k, '+' * counted[k]))

trial_count = 1

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


