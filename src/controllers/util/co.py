#!/usr/bin/python2.7
#
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Application settings/constants for the Google Analytics superProxy."""

__author__ = 'pete.frisella@gmail.com (Pete Frisella)'

# Determines if account info is removed from responses.
# Set to True to remove Google Analytics account info from public responses.
# TODO(pfrisella): Move this into an Admin Web UI.
ANONYMIZE_RESPONSES = True

# Determines which timezone relative dates will be resolved to.
# North American timezones are supported and UTC.
# Acceptable values are (case-insensitive):
#   atlantic, atc, adt, eastern, est, edt, central, cst, cdt, mountain, mst,
#   mdt, pacific, pst, pdt, utc
# TODO(pfrisella): Move this into an Admin Web UI.
TIMEZONE = 'utc'

# A list of all supported formats for responses.
# The key represents the query paramter value to use to request a format.
# For example &format=csv will return a CSV response.
# The label key/value is the friendly name for this format. It is displayed
# in the Web UI.
DEFAULT_FORMAT = 'json'
SUPPORTED_FORMATS = {
    'json': {
        'label': 'JSON'
    },
    'csv': {
        'label': 'CSV'
    },
    'data-table': {
        'label': 'DataTable (JSON String)'
    },
    'data-table-response': {
        'label': 'DataTable (JSON Response)'
    },
    'tsv': {
        'label': 'TSV for Excel'
    }
}


# Log API Response Errors
# It's not recommended to set this to False.
LOG_ERRORS = True

# Scheduling: Max number of errors until query scheduling is paused.
QUERY_ERROR_LIMIT = 3

# Scheduling: How many seconds until a query is considered abandoned. (i.e.
# there have been no requests for the data). Calculated as a multiple of the
# query's refresh interval.
ABANDONED_INTERVAL_MULTIPLE = 2

# Scheduling: Used to randomize start times for scheduled tasks to prevent
# multiple queries from all starting at the same time.
MAX_RANDOM_COUNTDOWN = 60  # seconds

# API Query Limitations (CreateForm)
MAX_NAME_LENGTH = 115   # characters
MAX_URL_LENGTH = 2000   # characters
MIN_INTERVAL = 15       # seconds
MAX_INTERVAL = 2505600  # seconds

# Sharding Key Names
REQUEST_COUNTER_KEY_TEMPLATE = 'request-count-{}'
REQUEST_TIMESTAMP_KEY_TEMPLATE = 'last-request-{}'

# General Error Messages
ERROR_INACTIVE_QUERY = 'inactiveQuery'
ERROR_INVALID_REQUEST = 'invalidRequest'
ERROR_INVALID_QUERY_ID = 'invalidQueryId'

ERROR_MESSAGES = {
    ERROR_INACTIVE_QUERY: ('The query is not yet available. Wait and try again '
                           'later.'),
    ERROR_INVALID_REQUEST: ('The query id is invalid or the API Query is '
                            'disabled.'),
    ERROR_INVALID_QUERY_ID: 'Invalid query id.'
}

DEFAULT_ERROR_MESSAGE = {
    'error': ERROR_INVALID_REQUEST,
    'code': 400,
    'message': ERROR_MESSAGES[ERROR_INVALID_REQUEST]
}

# All Links for Google Analytics superProxy
LINKS = {
    # Admin links
    'admin_users': '/admin/proxy/users',
    'admin_runtask': '/admin/proxy/runtask',

    # Owner links
    'owner_default': r'/admin.*',
    'owner_index': '/admin',
    'owner_auth': '/admin/auth',
    'owner_activate': '/admin/activate',
    'query_manage': '/admin/query/manage',
    'query_edit': '/admin/query/edit',
    'query_delete': '/admin/query/delete',
    'query_delete_errors': '/admin/query/errors/delete',
    'query_create': '/admin/query/create',
    'query_status_change': '/admin/query/status',
    'query_run': '/admin/query/run',
    'query_schedule': '/admin/query/schedule',

    # Management links
    'management_default': r'/management.*',
    'management_api': '/management/api.*',

    # Public links
    'public_default': r'/.*',
    'public_index': '/',
    'public_query': '/query',

    # Static directories
    'css': '/static/gasuperproxy/css/',
    'js': '/static/gasuperproxy/js/'
}

ANALYTICS_PROPERTY = 'ga:105878091'
QUERY_DATES = [
    {
        'start': '7daysAgo',
        'end': 'yesterday'
    },
    {
        'start': '30daysAgo',
        'end': 'yesterday'
    },
    {
        'start': '90daysAgo',
        'end': 'yesterday'
    }
]
BASE_QUERIES = [
    {
        'name': 'Total Sessions',
        'base_url': 'https://www.googleapis.com/analytics/v3/data/ga?'
                    'ids={analytics_property}&'
                    'metrics=ga:sessions&'
                    'filters=ga:dimension3%3D%3D{app_id}&'
                    'start-date={start_date}&'
                    'end-date={end_date}&'
                    'samplingLevel=HIGHER_PRECISION',
        'refresh_interval': 86400
    },
    {
        'name': 'Average Time On Page',
        'base_url': 'https://www.googleapis.com/analytics/v3/data/ga?'
                    'ids={analytics_property}&'
                    'metrics=ga:avgTimeOnPage&'
                    'filters=ga:dimension3%3D%3D{app_id}'
                    '&start-date={start_date}'
                    '&end-date={end_date}&'
                    'samplingLevel=HIGHER_PRECISION',
        'refresh_interval': 86400
    },
    {
        'name': 'New vs Returning',
        'base_url': 'https://content.googleapis.com/analytics/v3/data/ga?'
                    'ids={analytics_property}&'
                    'dimensions=ga%3AuserType&'
                    'metrics=ga%3Asessions&'
                    'filters=ga%3Adimension3%3D%3D{app_id}&'
                    'start-date={start_date}&'
                    'end-date={end_date}&'
                    'samplingLevel=HIGHER_PRECISION',
        'refresh_interval': 86400
    },
    {
        'name': 'Clicked Content Items',
        'base_url': 'https://content.googleapis.com/analytics/v3/data/ga?'
                    'ids={analytics_property}&'
                    'dimensions=ga%3AeventLabel&'
                    'metrics=ga%3AtotalEvents&'
                    'filters=ga%3Adimension3%3D%3D{app_id};ga:eventCategory%3D%3DContent%20Item&'
                    'sort=-ga%3AtotalEvents&'
                    'max-results=10&'
                    'start-date={start_date}&'
                    'end-date={end_date}&'
                    'samplingLevel=HIGHER_PRECISION',
        'refresh_interval': 86400
    },
    {
        'name': 'Shared Content Items',
        'base_url': 'https://www.googleapis.com/analytics/v3/data/ga?'
                    'ids={analytics_property}&'
                    'dimensions=ga:eventCategory,ga:eventLabel&'
                    'metrics=ga:totalEvents&'
                    'filters=ga:dimension3%3D%3D{app_id};ga:eventAction%3D%3Dshare;ga:eventAction%3D%3Dshare;ga:eventAction%3D%3Dshare&'
                    'sort=-ga:totalEvents&'
                    'max-results=10&'
                    'start-date={start_date}&'
                    'end-date={end_date}&'
                    'samplingLevel=HIGHER_PRECISION',
        'refresh_interval': 86400
    },
    {
        'name': 'Location',
        'base_url': 'https://content.googleapis.com/analytics/v3/data/ga?'
                    'ids={analytics_property}&'
                    'dimensions=ga%3Acountry&'
                    'metrics=ga%3Asessions&'
                    'filters=ga%3Adimension3%3D%3D{app_id}&'
                    'start-date={start_date}&'
                    'end-date={end_date}&'
                    'samplingLevel=HIGHER_PRECISION',
        'refresh_interval': 86400
    },
    {
        'name': 'Sessions by Day',
        'base_url': 'https://content.googleapis.com/analytics/v3/data/ga?'
                    'ids={analytics_property}&'
                    'dimensions=ga%3Aday&'
                    'metrics=ga%3Asessions&'
                    'filters=ga%3Adimension3%3D%3D{app_id}&'
                    'start-date={start_date}&'
                    'end-date={end_date}&'
                    'samplingLevel=HIGHER_PRECISION',
        'refresh_interval': 86400
    }
]

MANAGEMENT_TOKENS = ['L2d10Jtjsn1PbJoq11paSOR8Ze902X6R']
