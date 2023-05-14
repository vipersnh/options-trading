import matplotlib.pyplot as plt
import numpy as np
from random import choices

win_rate = 90/100
rr_ratio = 1/2 # Reward/Risk ratio
max_risk = 2/100 # Max Loss as % of account size
account_size = 20*1000
average_trade_duration = 14
trades_count = int(365/average_trade_duration)

population = [rr_ratio, -1]
weights = [win_rate, 1-win_rate]

samples = choices(population, weights, k=trades_count)

account_value = account_size
account_samples = []
for sample in samples:
    account_samples.append(account_value)
    old_account_value = account_value
    win_loss = account_size*max_risk*sample
    account_value += win_loss
    print("Account Value = {0}->{1}, change = {2}".format(old_account_value, account_value, win_loss))

print("Annual Gain : {0:.2f}".format((account_value-account_size)/account_size*100))

plt.plot(range(trades_count), account_samples)
plt.show()
