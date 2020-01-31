from slugify import slugify
import sys
import datetime
from prometheus_client import start_http_server, Summary
import time
from prometheus_client.core import REGISTRY
import logging
import os
from prometheus_client.metrics_core import GaugeMetricFamily

from src.lib.osta import Osta

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('osta-exporter')


class OstaCollector(object):
    def __init__(self, api_url, user_id):
        self.user_id = user_id
        self.osta = Osta(logger, api_url)

    def date_format(self, date):
        if date is None:
            return '1970-01-01'
        return str(datetime.datetime.strptime(date, '%d.%m.%Y').date())

    @REQUEST_TIME.time()
    def collect(self):
        logger.info('Scraping osta.ee for new metrics...')

        user_items = self.osta.get_user_items(self.user_id)

        for user_item in user_items:
            gauge = GaugeMetricFamily("osta_item_price", 'Price of an auctioned item',
                                      labels=['user_id', 'item_id', 'title'])
            gauge.add_metric([str(self.user_id), str(user_item.get('itemId')), slugify(user_item.get('title'))],
                             float(user_item.get('currentPriceEur')))

            gauge = GaugeMetricFamily("osta_item_bids", 'Number of bids for an auctioned item',
                                      labels=['user_id', 'item_id', 'title'])
            gauge.add_metric([str(self.user_id), str(user_item.get('itemId')), slugify(user_item.get('title'))],
                             int(user_item.get('currentBids')))
            yield gauge

        logger.info('Scraping completed')


if __name__ == '__main__':
    logger.info('osta-exporter (https://github.com/anroots/osta-exporter) starting up...')
    user_id = os.environ.get('OSTA_USER_ID')
    if not user_id:
        logger.fatal('You need to set required env variables before starting the exporter')
        sys.exit(1)
    REGISTRY.register(OstaCollector('https://api.osta.ee/api', user_id))
    start_http_server(8080)
    logger.info('Collector started, listening on port :8080; waiting for scrapes...')

    while True:
        time.sleep(1)
