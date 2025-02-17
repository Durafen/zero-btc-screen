import json
import random
import time
from datetime import datetime, timezone, timedelta
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config.builder import Builder
from config.config import config
from logs import logger
from presentation.observer import Observable
from leds import Leds

DATA_SLICE_DAYS = 1
DATETIME_FORMAT = "%Y-%m-%dT%H:%M"


def get_dummy_data():
    logger.info('Generating dummy data')



def fetch_prices():
    logger.info('Fetching prices')
    timeslot_end = datetime.now(timezone.utc)
    end_date = timeslot_end.strftime(DATETIME_FORMAT)
    start_data = (timeslot_end - timedelta(days=DATA_SLICE_DAYS)).strftime(DATETIME_FORMAT)
    url = f'https://production.api.coindesk.com/v2/price/values/{config.currency}?ohlc=true&start_date={start_data}&end_date={end_date}'
    req = Request(url)
    data = urlopen(req, timeout=10).read()
    external_data = json.loads(data)
    prices = [entry[1:] for entry in external_data['data']['entries']]
    return prices


def main():

	logger.info('Initialize')
	
	data_sink = Observable()
	builder = Builder(config)
	builder.bind(data_sink)
	leds = Leds()

	
	while True:
		try:
			prices = [entry[1:] for entry in get_dummy_data()] if config.dummy_data else fetch_prices()
			data_sink.update_observers(prices)
			leds.off()
			time.sleep(config.refresh_interval)

		except Exception as e:
			logger.error(str(e))
			leds.on()
			time.sleep(10)
	
		except KeyboardInterrupt:
	    		logger.info('Exit')
	    		data_sink.close()
	    		exit()
	


if __name__ == "__main__":
    main()
