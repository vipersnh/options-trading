import pdb
import matplotlib.pyplot as plt
import numpy as np
import random
import collections

# Current Setup of ~10 delta strangles
win_rate = 90/100
reward_to_credit_ratio = 50/100 # 50% of credit as profit target
stoploss_to_credit_ratio = 150/100 # 150% of credit as SL target
rr_ratio = reward_to_credit_ratio/stoploss_to_credit_ratio # Reward/Risk ratio
max_risk_per_trade = 5/100 # Max Loss as % of account size
max_risk_all_trades = 15/100
uncorrelated_parallel_trades = int(max_risk_all_trades/max_risk_per_trade)
account_size = 100*1000
average_trade_duration = 30
average_total_credit = uncorrelated_parallel_trades*max_risk_per_trade*account_size
credit = max_risk_per_trade*account_size

### Higher delta of ~20 delta strangles
##win_rate = 80/100
##reward_to_credit_ratio = 70/100 # 50% of credit as profit target
##stoploss_to_credit_ratio = 120/100 # 150% of credit as SL target
##rr_ratio = reward_to_credit_ratio/stoploss_to_credit_ratio # Reward/Risk ratio
##max_risk_per_trade = 2/100 # Max Loss as % of account size
##max_risk_all_trades = 6/100
##uncorrelated_parallel_trades = int(max_risk_all_trades/max_risk_per_trade)
##account_size = 100*1000
##average_trade_duration = 20
##average_total_credit = uncorrelated_parallel_trades*max_risk_per_trade*account_size

# Strangle & Iron Condor & Double Diagonal
#win_rate = 70/100
#reward_to_credit_ratio = 70/100 # 50% of credit as profit target
#stoploss_to_credit_ratio = 100/100 # 150% of credit as SL target
#rr_ratio = reward_to_credit_ratio/stoploss_to_credit_ratio # Reward/Risk ratio
#max_risk_per_trade = 4/100 # Max Loss as % of account size
#max_risk_all_trades = 10/100
#uncorrelated_parallel_trades = int(max_risk_all_trades/max_risk_per_trade)
#account_size = 100*1000
#average_trade_duration = 30
#average_total_credit = uncorrelated_parallel_trades*max_risk_per_trade*account_size
#credit = max_risk_per_trade*account_size


### Straddle setup 
#win_rate = 50/100
#reward_to_credit_ratio = 50/100 # 50% of credit as profit target
#stoploss_to_credit_ratio = 30/100 # 30% of credit as SL target
#rr_ratio = reward_to_credit_ratio/stoploss_to_credit_ratio # Reward/Risk ratio
#max_risk_per_trade = 1/100 # Max Loss as % of account size
#max_risk_all_trades = 6/100
#uncorrelated_parallel_trades = int(max_risk_all_trades/max_risk_per_trade)
#account_size = 100*1000
#average_trade_duration = 14


print("Trading Parameters")
print()
print("Account Size : ${0}".format(account_size))
print("Win-Rate : {0:.2f}% and RR Ratio : {1:.2f}%".format(win_rate*100, rr_ratio*100))
print("Reward to Credit Ratio   : {0:.2f}%".format(reward_to_credit_ratio*100))
print("Stoploss to Credit Ratio : {0:.2f}%".format(stoploss_to_credit_ratio*100))
print("Maximum Risk : ${0:.2f}".format(max_risk_per_trade*account_size))
rw = credit*reward_to_credit_ratio
sl = credit*stoploss_to_credit_ratio
print("For credit of ${0}, we'll have ${1} TP and ${2} SL limits".format(credit, int(rw), int(sl)))
print()

def get_account_samples(seed, win_rate, rr_ratio, max_risk, account_size, average_trade_duration, parallel_trades):
    trades_count = int(365/average_trade_duration)*parallel_trades
    population = [-1, rr_ratio]
    weights = [1-win_rate, win_rate]
    random.seed(seed)
    print("For win-rate of {0:.2f}% and Reward/Risk of {1:.2f}, SL = ${2:.2f} and TP = ${3:.2f}".format(win_rate*100, rr_ratio, max_risk*account_size, max_risk*rr_ratio*account_size))
    samples = random.choices([0, 1], weights, k=trades_count)

    account_value = account_size
    account_samples = [account_size]

    trades = []
    for index in range(trades_count):
        account_samples.append(account_value)
        sample = samples[index]
        win_loss = account_value*max_risk*population[sample]
        print("win_loss = ${0:4d}, total-account = ${1:.2f}".format(int(win_loss), account_value))
        account_value += win_loss
        trades.append(win_loss)
    
    return [account_value, account_samples, trades]

def ascii_histogram(seq) -> None:
    """A horizontal frequency-table/histogram plot."""
    counted = collections.Counter(seq)
    for k in sorted(counted):
        print('{0:5d}% {1}'.format(k, '+' * counted[k]))

trial_count = 10

annual_gain_average = 0
annual_gains = []
for seed in range(trial_count):
    [account_value, account_samples, trades] = get_account_samples(seed, win_rate, rr_ratio, max_risk_per_trade, account_size, average_trade_duration, uncorrelated_parallel_trades)
    total_trades = len(trades)
    total_wins = sum(1 for i in trades if i >= 0)
    total_losses = sum(1 for i in trades if i < 0)
    print("Annual Gain : {0:.1f}%".format((account_value-account_size)/account_size*100))
    print("Total Trades : {0}, Total Wins : {1}, Total Losses : {2}".format(total_trades, total_wins, total_losses))
    annual_gain = int((account_value-account_size)/account_size*100)
    annual_gains.append(annual_gain)
    annual_gain_average += annual_gain


print("Number of parallel trades    : {0}".format(uncorrelated_parallel_trades))
print("Maximum Simultaneous Credit  : {0}".format(average_total_credit))
ascii_histogram(annual_gains)

print("Annaul Gain Average : {0:.2f}".format(annual_gain_average/trial_count))


