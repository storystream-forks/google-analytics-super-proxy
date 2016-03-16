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

"""Handles all StoryStream Authenticated requests to the Google Analytics superProxy.

These handlers are for actions performed by StoryStream.

  QueryManagementHandler: Handles creation and deletion of queries.
  NotAuthorizedHandler: Handles unauthorized requests.
"""

__author__ = 'pete.frisella@gmail.com (Pete Frisella)'

import json

from controllers import base
from controllers.transform import transformers
from controllers.util import access_control
from controllers.util import co
from controllers.util import errors
from controllers.util import query_helper
import webapp2


class QueryManagementHandler(base.BaseHandler):
    """Handles authenticated requests for API Query management.

    The handler manages the creation and deletion of API queries
    """

    @access_control.AccessTokenValid
    def post(self):
        """Creates API queries for the app ID provided.

        Given an App ID, loop through the queries and date ranges and create the queries.
        Return an array of query IDs.
        """
        try:
            app_id = int(self.request.get('app_id'))
        except ValueError:
            app_id = None

        queries = []
        if app_id:
            for q in co.BASE_QUERIES:
                for date in co.QUERY_DATES:
                    name = q.get('name')
                    start_date = date.get('start')
                    end_date = date.get('end')
                    formatted_request = q.get('base_url').format(
                        analytics_property=co.ANALYTICS_PROPERTY,
                        app_id=app_id,
                        start_date=start_date,
                        end_date=end_date
                    )

                    query_input = {
                        'name': 'ID:{app_id} - {base_name} - {date}'.format(app_id=app_id, base_name=name, date=start_date),
                        'request': formatted_request,
                        'refresh_interval': q.get('refresh_interval')
                    }

                    query_input = query_helper.ValidateApiQuery(query_input)

                    api_query = query_helper.BuildApiQuery(**query_input)

                    query_helper.ScheduleAndSaveApiQuery(api_query, randomize=True)

                    queries.append({
                        'id': str(api_query.key()),
                        'name': name,
                        'start_date': start_date,
                        'end_date': end_date
                    })

        self.RenderJson({
            'query_ids': queries
        })

    @access_control.AccessTokenValid
    def put(self):
        """Delete an API Query.

        Deletes queries, responses and errors given a query ID.
        Accepts an array of query IDs
        Returns a JSON object with an array of deleted query IDs.
        """
        query_ids = json.loads(self.request.body).get('query_ids', [])
        deleted_query_ids = []
        for query_id in query_ids:
            api_query = query_helper.GetApiQuery(query_id)
            if api_query:

                success = query_helper.DeleteApiQuery(api_query)
                if success:
                    deleted_query_ids.append(query_id)

        self.RenderJson({
            'query_ids': deleted_query_ids
        })


class NotAuthorizedHandler(base.BaseHandler):
    """Handles unauthorized requests to management pages."""

    def get(self):
        self.RenderHtml('public.html', status=401)


app = webapp2.WSGIApplication(
    [(co.LINKS['management_api'], QueryManagementHandler),
     (co.LINKS['management_default'], NotAuthorizedHandler)],
    debug=True)
