from .. import db
import time
from datetime import datetime
import pandas as pd
from ..models import TimeLine


def get_attribute_values(attribute):
    """Returns: Information about possible filtering
    (list of attributes and list of values for each attribute)"""

    result_list = []

    for value in db.session.query(attribute).distinct():
        result_list.append(value[0])

    return sorted(result_list)


def get_timeline_data(params):
    """Returns: JSON with timeline information according to input parameters"""

    start_date = _convert_date_to_timestamp(params.get('startDate'))
    end_date = _convert_date_to_timestamp(params.get('endDate'))

    filters = {}

    for kay, value in params.items():
        if kay in ('startDate', 'endDate', 'Type', 'Grouping'):
            continue
        else:
            filters.update({kay: value})

    query_set = TimeLine.query.filter(TimeLine.timestamp >= start_date,
                                      TimeLine.timestamp <= end_date)

    for attr, value in filters.items():
        query_set = query_set.filter(getattr(TimeLine, attr) == value)

    result = _timeline_formation(params.get('startDate'), params.get('endDate'),
                                 params.get('Type'), params.get('Grouping') or 'monthly',
                                 query_set)

    return result


def _timeline_formation(start_date, end_date, timeline_type, grouping_type, query_set):

    timeline = []

    freq = {'weekly': 'W', 'bi - weekly': 'SMS', 'monthly': 'M'}

    date_index = list(pd.bdate_range(start_date, end_date,
                                     freq=freq[grouping_type]).strftime('%Y-%m-%d'))

    start_date_query = start_date
    if timeline_type == 'usual':
        for end_date_query in date_index:
            start = _convert_date_to_timestamp(start_date_query)
            end = _convert_date_to_timestamp(end_date_query)
            query = query_set.filter(TimeLine.timestamp >= start).filter(
                                     TimeLine.timestamp <= end)
            timeline.append({'date': start_date_query, 'value': query.count()})
            start_date_query = end_date_query
    else:
        accumulator = 0
        for end_date_query in date_index:
            start = _convert_date_to_timestamp(start_date_query)
            end = _convert_date_to_timestamp(end_date_query)
            query = query_set.filter(TimeLine.timestamp >= start).filter(
                                     TimeLine.timestamp <= end)
            accumulator += query.count()
            timeline.append({'date': start_date_query, 'value': accumulator})
            start_date_query = end_date_query

    return timeline


def _convert_date_to_timestamp(date):

    t_stamp = int(time.mktime(datetime.strptime(date, '%Y-%m-%d').timetuple()))

    return t_stamp
