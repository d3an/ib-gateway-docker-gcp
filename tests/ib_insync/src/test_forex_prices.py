import logging
import os
import random
import sys

import ib_insync as ibis


# Set module-wide log level here
LOG_LEVEL = logging.INFO


def connect_to_ib():
    # Connect to market gateway
    ibinstance = ibis.IB()
    ibinstance.connect(host=os.getenv('IB_GATEWAY_PAPER_URLNAME', 'tws-paper'),
                       port=int(os.getenv('IB_GATEWAY_PAPER_URLPORT', '4004')),
                       clientId=int(os.getenv('EFP_CLIENT_ID', (5+random.randint(0, 4)))),
                       timeout=15,
                       readonly=True)
    logging.info("Connected to IB")
    ibinstance.reqMarketDataType(int(os.getenv('MKT_DATA_TYPE', '4')))
    return ibinstance


def consume_tickers(single_tick):
    tick_basec = single_tick["contract"]["Forex"]["localSymbol"][:3]
    tick_pairc = single_tick["contract"]["Forex"]["localSymbol"][-3:]
    tick_time = single_tick["time"]
    tick_bid = single_tick["bid"]
    tick_ask = single_tick["ask"]
    print(f"Time: {tick_time}, {tick_basec}-{tick_pairc}, Bid: {tick_bid}, Ask:{tick_ask}")
    print("Got a tick. Exiting with success.")
    sys.exit(0)


def get_forex_pairs(ib_conn):
    """
    Get a list of contract IDs from the database, and qualify them in IB
    :param ib_conn:
    :param db_conn:
    :return:
    """
    currency_pairs = ["USDAUD", "USDGBP", "USDEUR"]
    contracts = [ibis.Forex(pair) for pair in currency_pairs]
    ib_conn.qualifyContracts(*contracts)
    return contracts


def request_market_data(contracts, ib_conn):
    for each_contract in contracts:
        ib_conn.reqMktData(each_contract, '', False, False)
        ib_conn.ticker(each_contract)


def request_current_ticker(contracts, ib_conn):
    for each_contract in contracts:
        ib_conn.ticker(each_contract)


def start_ticker_feed(contracts, ib_conn):
    """
    For a given currency, get the current exchange rate from the sharemarket
    :param contract_ids: List of contract IDs to
    :param ibinstance: The IB instance we're using to query the sharemarket
    :return: A stream of ticks for the currency pair in dict form
    """
    request_market_data(contracts, ib_conn)

    def onPendingTickers(tickers):
        for tick in tickers:
            # We can't test the below unless we are within 24/5 trading!
            if tick.midpoint() > 0:
                single_tick = ibis.util.tree(tick)['Ticker']
                consume_tickers(single_tick)

    def onTimeoutOccuring(time_since_event):
        ib_conn.disconnect()  # Nicely disconnect from IB and DB
        sys.exit(f"test_forex_prices got no ticks in {time_since_event} seconds - restarting!")

    # Add function as event
    ib_conn.pendingTickersEvent += onPendingTickers
    ib_conn.timeoutEvent += onTimeoutOccuring
    # Start the timeout after the tickers have been requested
    ibis.util.sleep(10)  # Give IB 5 seconds grace to start giving us tickers
    ib_conn.setTimeout(20)


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(LOG_LEVEL)
    logging.info("Reporting INFO-level messages")
    
    ibis.util.sleep(90)
    ibis.util.startLoop()
    ibis.util.logToConsole(level=LOG_LEVEL)
    
    ib_conn = connect_to_ib()
    logging.info("test_forex_prices connected to IB")
    contracts = get_forex_pairs(ib_conn)
    start_ticker_feed(contracts, ib_conn)


if __name__ == '__main__':
    main()
