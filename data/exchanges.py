import requests


def get_binance_pair(first, second):
    server = 'https://api.binance.com/api/v3/ticker/price'
    search_params = {
        'symbol': first + second
    }
    return requests.get(server, params=search_params).json()


def get_okx_pair(first, second):
    server = 'https://aws.okx.com/api/v5/market/ticker'
    search_params = {
        'instId': first + '-' + second + '-SWAP'
    }
    return requests.get(server, params=search_params).json()


def get_bybit_pair(first, second):
    server = 'https://api.bybit.com/v5/market/tickers'
    search_params = {
        'category': 'spot',
        'symbol': first + second
    }
    return requests.get(server, params=search_params).json()


def get_bitget_pair(first, second):
    server = 'https://api.bitget.com/api/spot/v1/market/ticker'
    search_params = {
        'symbol': first + second + '_SPBL'
    }
    return requests.get(server, params=search_params).json()
