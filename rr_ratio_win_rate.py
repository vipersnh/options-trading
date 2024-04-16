from collections import namedtuple

Parameters_t = namedtuple('Parameters_t', ['name', 'win_rate', 'profit_level', 'stop_level'])

# Strangle on ES
param0 = Parameters_t(name="10Δ Strangle", win_rate=90, profit_level=50, stop_level = 150)
param1 = Parameters_t(name="25Δ Strangle", win_rate=75, profit_level=80, stop_level = 100)
param2 = Parameters_t(name="30Δ Strangle", win_rate=70, profit_level=90, stop_level = 100)
param3 = Parameters_t(name="50Δ Straddle", win_rate=50, profit_level=60, stop_level = 25)

params = [param0, param1, param2, param3]

def process_parameters(param):
    name = param.name
    win_rate = param.win_rate/100
    profit_level = param.profit_level
    stop_level = param.stop_level
    expectancy = win_rate*profit_level - (1-win_rate)*stop_level
    rr_ratio = stop_level/profit_level
    return (name, expectancy, rr_ratio)
        

for param in params:
    (name, expectancy, rr_ratio) = process_parameters(param)
    print("For {0}, expectancy = {1:.2f}% of credit each trade, rr_ratio = {2:.2f}".format(name, expectancy, rr_ratio))
