#!/usr/bin/env python

import argparse
import datetime
import json

import time
from time import sleep

import sys

sys.path.append('lib')

from lib.logger import init_logger

init_logger('log/monitor.log', 'INFO')
import logging

logger = logging.getLogger('monitor')
import requests


def monitor(args):
    logger.info("start monitor with args: {0}".format(args))

    parser = argparse.ArgumentParser(prog='monitor',
                                     description="monitor (and report) metrics of elastic search cluster and applications")

    parser.add_argument('-i', '--interval', default='30', type=int, metavar='interval',
                        help='report interval in seconds. default: 30 (0.5min)')

    try:

        a = parser.parse_args(args)

        interval = a.interval

        eth_balance = '0'
        current_hashrate = '0'
        average_hashrate = '0'
        daily_hashrate = '0'
        reported_hashrate = '0'
        online_count = '0'
        last_eth_balance = '0'
        last_current_hashrate = '0'
        last_average_hashrate = '0'
        last_reported_hashrate = '0'
        last_online_count = '0'
        updatedTime = datetime.datetime.now()
        time_to_payout = '0'
        gas_price = '0'

        while True:
            start_time = time.time()

            logger.info('start new round of monitor')
            html_str = """
            <table border=1>
            <caption, border=1,align=left>Ezil Address</caption>
                <tr><td>ETH</td><td>0xd100eA705Bf62fbB5F07daB652f52A0D2f0a1FBF</td></tr>
            </table>
            <br />
            <table border=1>
            <caption, align=left>Worker Stats</caption>
                <tr>
                   <th>Item</th>
                   <th>Current Value</th>
                   <th>Last Value</th>
                </tr>
                    #rows#
            </table>
            <br />
            <table border=1>
                <tr><td>Updated Time</td><td>#UpdatedTime#</td></tr>
                <tr><td>Time to Payout</td><td>#time_to_reach_min_payout#</td></tr>
                <tr><td>Est Next Payout Time</td><td>#next_payout_time#</td></tr>
                <tr><td>Gas Price</td><td>#current_gas_price#</td></tr>
            </table>
            """

            payload = {}
            headers = {}

            # url = "https://billing.ezil.me/balances/0xd100eA705Bf62fbB5F07daB652f52A0D2f0a1FBF"
            # try:
            #     response = requests.request("GET", url, headers=headers, data=payload)
            #     dict = json.loads(response.text)
            #
            #     if eth_balance != dict['eth']:
            #         last_eth_balance = eth_balance
            #         eth_balance = dict['eth']
            #         updatedTime = datetime.datetime.now()
            # except:
            #     print("Oops!", sys.exc_info()[0], "occurred.")
            #     continue

            url = "https://billing.ezil.me/v2/accounts/0xd100eA705Bf62fbB5F07daB652f52A0D2f0a1FBF"
            try:
                response = requests.request("GET", url, headers=headers, data=payload)
                dict = json.loads(response.text)

                if eth_balance != dict['balances'][0]['amount']:
                    last_eth_balance = eth_balance
                    eth_balance = round(dict['balances'][0]['amount'], 6)
                    updatedTime = datetime.datetime.now()
                time_to_payout_in_min = int(float(dict['balances'][0]['payout']['time_to_reach_min_payout']) / 60)
                time_to_payout = '{0} hours'.format(
                    round(time_to_payout_in_min / 60, 2))
                next_payout_time = datetime.datetime.now() + datetime.timedelta(minutes=time_to_payout_in_min)
                if dict['balances'][0]['payout']['current_gas_price'] is not None:
                    gas_price = str(round(dict['balances'][0]['payout']['current_gas_price'], 0))
            except:
                print("Oops!", sys.exc_info()[0], "occurred.")
                continue

            rows = ''
            rows = rows + '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>'.format('ETH Balance', eth_balance,
                                                                                 last_eth_balance)

            url = "https://stats.ezil.me/current_stats/0xd100eA705Bf62fbB5F07daB652f52A0D2f0a1FBF/workers/stats?coin=eth"
            try:
                response = requests.request("GET", url, headers=headers, data=payload)
                dict = json.loads(response.text)

                if current_hashrate != dict['current_hashrate']:
                    last_current_hashrate = current_hashrate
                    current_hashrate = dict['current_hashrate']
                    updatedTime = datetime.datetime.now()
                if average_hashrate != dict['average_hashrate']:
                    last_average_hashrate = average_hashrate
                    average_hashrate = dict['average_hashrate']
                    updatedTime = datetime.datetime.now()
                if daily_hashrate != dict['daily_hashrate']:
                    last_daily_hashrate = daily_hashrate
                    daily_hashrate = dict['daily_hashrate']
                    updatedTime = datetime.datetime.now()
                if reported_hashrate != dict['reported_hashrate']:
                    last_reported_hashrate = reported_hashrate
                    reported_hashrate = dict['reported_hashrate']
                    updatedTime = datetime.datetime.now()
                if online_count != dict['workers']['online_count']:
                    last_online_count = online_count
                    online_count = dict['workers']['online_count']
                    updatedTime = datetime.datetime.now()
            except:
                print("Oops!", sys.exc_info()[0], "occurred.")
                continue

            rows = rows + '<tr><td>{0}</td><td>{1} MHz/s</td><td>{2} MHz/s</td></tr>'.format('30 min', round(float(
                current_hashrate) / 1000000, 2), round(float(last_current_hashrate) / 1000000, 2))
            rows = rows + '<tr><td>{0}</td><td>{1} MHz/s</td><td>{2} MHz/s</td></tr>'.format('3 hour', round(float(
                average_hashrate) / 1000000, 2), round(float(last_average_hashrate) / 1000000, 2))
            rows = rows + '<tr><td>{0}</td><td>{1} MHz/s</td><td>{2} MHz/s</td></tr>'.format('24 hour', round(float(
                daily_hashrate) / 1000000, 2), round(float(last_daily_hashrate) / 1000000, 2))
            rows = rows + '<tr><td>{0}</td><td>{1} MHz/s</td><td>{2} MHz/s</td></tr>'.format('Reported', round(float(
                reported_hashrate) / 1000000, 2), round(float(last_reported_hashrate) / 1000000, 2))
            rows = rows + '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>'.format('Worker Status', online_count,
                                                                                 last_online_count)

            html_str = html_str.replace('#rows#', rows)
            html_str = html_str.replace('#UpdatedTime#', updatedTime.strftime('%Y-%m-%d %H:%M:%S'))
            html_str = html_str.replace('#time_to_reach_min_payout#', time_to_payout)
            html_str = html_str.replace('#next_payout_time#', next_payout_time.strftime('%Y-%m-%d %H:%M:%S'))
            html_str = html_str.replace('#current_gas_price#', gas_price)

            Html_file = open("index.html", "w")
            Html_file.write(html_str)
            Html_file.close()

            end_time = time.time()
            elapsed = end_time - start_time
            diff = interval - elapsed

            logger.info('finish this round of monitor, took: {0}s'.format(elapsed))
            logger.info('sleep: {0}s ...'.format(diff))

            if diff > 0:
                sleep(diff)

    except Exception as e:
        logger.exception('error in monitor')
        return 1

r = monitor(sys.argv[1:])
sys.exit(r)
