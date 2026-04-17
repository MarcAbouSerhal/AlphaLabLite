import pandas as pd

DATA = pd.read_csv("fetch_transformation_data.csv") # data is read once in case multiple rows are read
NAN = float('nan')

def fetch(datasource):
    row = DATA.loc[DATA["datasource"] == datasource].iloc[0]
    return row.astype(float).tolist()

def simple_moving_average(window, a):
    n = len(a)

    sum = 0 # sum of the window [t - window + 1, t]
    b = [NAN for t in range(n)]

    for t in range(n):
        sum += a[t]
        if t >= window:
            sum -= a[t - window]
        if t >= window - 1:
            b[t] = sum / window

    return b
        
def exponential_moving_average(alpha, a):
    n = len(a)

    b = [NAN for t in range(n)]

    b[0] = a[0]
    for t in range(1, n):
        b[t] = alpha * a[t] + (1 - alpha) * b[t - 1]

    return b

def rate_of_change(period, a):
    n = len(a)

    b = [NAN for t in range(n)]
    
    for t in range(period, n):
        if a[t - period] != 0:
            b[t] = (a[t] - a[t - period]) / a[t - period]
    
    return b

def cross_above(a1, a2):
    n = len(a1)

    b = [NAN] + [int(a1[t - 1] < a2[t - 1] and a1[t] > a2[t]) for t in range(1, n)]

    return b

def constant_series(k, a):
    n = len(a)

    return [k for t in range(n)]

def portfolio_estimation(balance, price, entry, exit):
    n = len(price)

    positions_held = 0
    portfolio = [NAN for t in range(n)]

    for i in range(n):
        if exit[i] == 1:
            balance += positions_held * price[i]
        elif entry[i] == 1:
            positions_held += 1
            balance -= price[i]
        portfolio[i] = balance + positions_held * price[i]

    return portfolio