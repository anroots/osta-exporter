from json import JSONDecodeError

import requests
import sys


class Osta:
    def __init__(self, logger, api_url):
        self.api_url = api_url
        self.logger = logger

    def get_user_items(self, user_id):
        self.logger.debug('Starting collection of osta.ee meters')
        query_params = {
            'userId': [user_id]
        }
        items = self.make_request('/items/active', query_params)
        self.logger.debug('Received {} items from osta.ee'.format(len(items)))

        return items

    @staticmethod
    def get_request_headers():
        return {
            'Accept': 'application/json',
            'Accept-Language': 'en',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
        }

    def make_request(self, uri, query_params):
        self.logger.debug('Sending request to Osta API')
        uri = self.api_url + uri
        try:
            r = requests.get(url=uri, params=query_params, headers=self.get_request_headers())
        except requests.exceptions.RequestException as e:
            self.logger.fatal(e)
            self.logger.fatal('Received error from HTTP request, exiting')
            sys.exit(1)
        try:
            response = r.json()
        except JSONDecodeError as e:
            self.logger.fatal('Osta HTTP endpoint returned invalid JSON, can not parse it')
            self.logger.fatal(r.text)
            sys.exit(1)
        return response
