import pandas as pd

NAN = float('nan')
DATA_FILE = "fetch_transformation_data.csv"

def fetch(datasource):
    """
    Fetches specific data source from fetch_transformation_data.csv
    """
    df = pd.read_csv(DATA_FILE, header = None)
    match = df[df.iloc[:, 0] == datasource]

    return match.iloc[0, 1:].astype(float).tolist()

def simple_moving_average(window, a):
    """
    Applies simple moving average on `a` with window size `window`
    """
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
    """
    Applies exponential moving average on `a` with parameter `alpha`
    """
    n = len(a)

    b = [NAN for t in range(n)]

    b[0] = a[0]
    for t in range(1, n):
        b[t] = alpha * a[t] + (1 - alpha) * b[t - 1]

    return b

def rate_of_change(period, a):
    """
    Finds rate of change of `a` of period of size `period`
    """
    n = len(a)

    b = [NAN for t in range(n)]
    
    for t in range(period, n):
        if a[t - period] != 0:
            b[t] = (a[t] - a[t - period]) / a[t - period]
    
    return b

def cross_above(a1, a2):
    """
    Finds times `a1` crosses over `a2`
    """
    n = len(a1)

    return [0] + [int(a1[t - 1] < a2[t - 1] and a1[t] > a2[t]) for t in range(1, n)]

def constant_series(k, a):
    """
    Constant series of value `k` with same length as `a`
    """
    n = len(a)

    return [k for t in range(n)]

def portfolio_simulation(balance, entry, exit, price):
    """
    Simulates portfolio starting with `balance`, buying 1 item at time t if `entry[t] = 1` and exitting when `exit[t] = 1`, with the price at time `t` being `price[t]`
    """
    n = len(price)

    positions_held = 0
    portfolio = [NAN for t in range(n)]

    for i in range(n):
        if exit[i] == 1.0:
            balance += positions_held * price[i]
            positions_held = 0
        elif entry[i] == 1.0:
            positions_held += 1
            balance -= price[i]
        portfolio[i] = balance + positions_held * price[i]

    return portfolio