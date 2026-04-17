from utils import *
from db_utils import *
import uuid

def execute(lines):
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
    context = fetch(id)
    return {series_name: series_value for series_name, series_value in context.items() if series_name in series_names}