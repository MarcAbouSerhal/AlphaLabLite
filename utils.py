import re
from transformations import *

def remove_whitespace(s):
    """
    Parameters:
        `s`: a string

    Returns:
        `str`: `s` after removing all whitespace characters
    """
    return "".join(s.split())

def extract_components(s):
    """
    Parameters:
        `s`: an expression from the following grammar:
            S = ID "=" call 
            
            call = ID "{" [args] "}" "{" [args] "}" ;

            args = ID { "," ID } ;

            ID = [A-Za-z0-9_]+ ;
        where S is the starting symbol
    
    Returns:
        `str`: left-hand side ID within S (series name)
        `str`: left-hand side ID within call (transformation name)
        `list[str]`: left-hand side args (configurations)
        `list[str]`: right-hand side args (timeseries)
    """
    series_name, call = s.split("=")
    transformation_name, args1, args2 = re.match(
        r'^([^{}]*)\{([^{}]*)\}\{([^{}]*)\}$',
        call
    ).groups()
    configurations = [] if args1 == "" else args1.split(",")
    timeseries = [] if args2 == "" else args2.split(",")
    return series_name, transformation_name, configurations, timeseries

# Every transformation name corresponds to a function, input configuration types and number of input series
TRANSFORMATION_MAP = {
    "Fetch": (fetch, (str, ), 0),
    "SimpleMovingAverage": (simple_moving_average, (int, ), 1),
    "ExponentialMovingAverage": (exponential_moving_average, (float, ), 1),
    "RateOfChange": (rate_of_change, (int, ), 1),
    "CrossAbove": (cross_above, (), 2),
    "ConstantSeries": (constant_series, (float, ), 1),
    "PortfolioSimulation": (portfolio_simulation, (float, ), 3), 
}

def call_transformation(context, transformation_name, configurations, timeseries):
    """
    Parameters:
        `context`: map from series names to values
        `transformation_name`: name of the called transformation
        `configurations`: input configurations as strings
        `timeseries`: names of input time series
    
    Returns:
        `list[float]`: output time series of the call with the given inputs   
    """
    transformation_function, configuration_types, num_timeseries = TRANSFORMATION_MAP[transformation_name]
    
    # Convert input configurations to appropriate types
    configurations = [
        config_type(config)
        for config_type, config in zip(configuration_types, configurations)
    ]
    # Extract timeseries from stored context
    timeseries = [context[series] for series in timeseries]
    # Assert number of time series is appropriate
    assert(len(timeseries) == num_timeseries)
   
    # Find and return output
    return transformation_function(*configurations, *timeseries)
