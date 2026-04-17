from utils import *
from db_utils import *
import uuid

def execute(lines):
    """
    Executes a script and returns id

    Parameters:
        `lines`: list of transformations

    Returns:
        `str`: id
    """
    context = {} # Stores all created series

    for line in lines:
        # Extract components of line
        series_name, transformation_name, configurations, timeseries = extract_components(line)

        # Call appropriate transformation and stores output in context
        context[series_name] = call_transformation(context, transformation_name, configurations, timeseries)

    id = str(uuid.uuid4())
    upload(id, context)
    return id

def view(id, series_names):
    """
    Returns dict of series corresponding to a given id

    Parameters:
        `id`: id of the series
        `series_names`: list of requested series

    Returns:
        `dict`: maps series name to its value
    """
    context = fetch(id)
    return {series_name: series_value for series_name, series_value in context.items() if series_name in series_names}