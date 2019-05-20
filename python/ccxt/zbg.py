# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code
import hashlib
import math

from ccxt.base.exchange import Exchange

from ccxt.base.errors import ExchangeError, ArgumentsRequired
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import OrderNotFound


class zbg(Exchange):
    def describe(self):
        return self.deep_extend(super(zbg, self).describe(), {
            'id': 'zbg',
            'name': 'ZBG',
            'countries': ['CN'],
            'rateLimit': 2000,
            'version': 'v1',
            'has': {
                'fetchBalance': True,  # 获取用户资产
                'fetchMarkets': True,  # 获取市场交易对
                'createOrder': True,  # 创建委托订单
                'cancelOrder': True,  # 取消委托订单
                'cancelOrders': True,  # 批量取消用户委托
                'fetchClosedOrders': True,  # 获取用户交易完成委托订单记录
                'fetchOpenOrders': True,  # 获取用户正在交易委托订单记录
                'fetchTicker': True,  # 获取单个市场24H市场行情
                'fetchTickers': True,  # 获取所有市场24H市场行情
                'fetchTrades': True,  # 获取市场交易记录
                'fetchMyTrades': True,  # 获取用户交易记录
                'fetchOHLCV': True,  # 获取市场k线
                'fetchOrder': True,  # 获取用户单个委托订单记录
                'fetchOrders': True,  # 获取用户委托订单记录
                'fetchCurrencies': True,  # 获取币种列表
                'fetchOrderBook': True,  # 获取市场深度
                'fetchDepositAddress': True,  # 获取充币地址
            },
            'timeframes': {
                '1m': '1min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '1d': '1day',
                '1w': '1week',
            },
            'exceptions': {
                '6096': ArgumentsRequired,
                '1003': ArgumentsRequired,
                '2000': ArgumentsRequired,
                '6000': ArgumentsRequired,
                '2012': OrderNotFound,
                '2014': OrderNotFound,
                '2015': OrderNotFound,
                '6895': AuthenticationError,
                '6896': AuthenticationError,
                '6897': AuthenticationError,
                '6898': AuthenticationError,
            },
            'urls': {
                'logo': 'https://www.zbg.com/src/images/logo.png',
                # 'api': 'http://179.zbg.com',
                'api': 'https://www.zbg.com',
                # 'publicapi': 'http://179kline.zbg.com',
                'publicapi': 'https://kline.zbg.com',
                'www': 'https://www.zbg.com',
                'doc': 'https://www.zbg.com/help/restApi',
                'fees': 'https://www.zbg.com/help/rate',
                'referral': 'https://www.zbg.com/new?recommendCode=N2VPVXRMQkZYVFU=',
            },
            'api': {
                'public': {
                    'get': [
                        'exchange/config/controller/website/marketcontroller/getByWebId',
                        'exchange/config/controller/website/currencycontroller/getCurrencyList',
                        'api/data/v1/ticker',
                        'api/data/v1/tickers',
                        'api/data/v1/entrusts',
                        'api/data/v1/trades',
                        'api/data/v1/klines',
                    ],
                },
                'private': {
                    'get': [
                        'exchange/entrust/controller/website/EntrustController/getEntrustById',
                        'exchange/entrust/controller/website/EntrustController/getUserEntrustList',
                        'exchange/entrust/controller/website/EntrustController/batchCancelEntrustByMarketId',
                        'exchange/entrust/controller/website/entrustcontroller/getuserentrustrecordfromcache',
                        'exchange/entrust/controller/website/entrustcontroller/getuserentrustrecordfromcachewithpage',
                        'exchange/entrust/controller/website/entrustcontroller/gettransactionpage',
                    ],
                    'post': [
                        'exchange/fund/controller/website/fundcontroller/findbypage',
                        'exchange/entrust/controller/website/EntrustController/addEntrust',
                        'exchange/entrust/controller/website/EntrustController/cancelEntrust',
                        'exchange/entrust/controller/website/entrustcontroller/batchcancelentrust',
                        'exchange/fund/controller/website/fundcontroller/getPayinAddress',
                    ],
                },
            },
            'fees': {
                'funding': {
                    'withdraw': {
                        'BTC': 0.0001,
                        'BCH': 0.0006,
                        'LTC': 0.005,
                        'ETH': 0.01,
                        'ETC': 0.01,
                        'BTS': 3,
                        'EOS': 1,
                        'QTUM': 0.01,
                        'HSR': 0.001,
                        'XRP': 0.1,
                        'USDT': '0.1%',
                        'QCASH': 5,
                        'DASH': 0.002,
                        'BCD': 0,
                        'UBTC': 0,
                        'SBTC': 0,
                        'INK': 20,
                        'TV': 0.1,
                        'BTH': 0,
                        'BCX': 0,
                        'LBTC': 0,
                        'CHAT': 20,
                        'bitCNY': 20,
                        'HLC': 20,
                        'BTP': 0,
                        'BCW': 0,
                    },
                },
                'trading': {
                    'maker': 0.1 / 100,
                    'taker': 0.1 / 100,
                },
            },
            'commonCurrencies': {
                'ENT': 'ENTCash',
            },
        })

    def fetch_currencies(self, params={}):
        response = self.public_get_exchange_config_controller_website_currencycontroller_getcurrencylist(params)

        result = {}
        currencies = response['datas']
        for currency in currencies:
            id = str(currency['currencyId'])
            name = currency['name']
            code = self.common_currency_code(id)
            result[code] = {
                'id': id,
                'code': code,
                'info': currency,
                'name': name.upper(),
            }
        return result

    def fetch_markets(self, params={}):
        markets = self.public_get_exchange_config_controller_website_marketcontroller_getbywebid()
        result = []
        for market in markets['datas']:
            name = market['name']
            [baseId, quoteId] = name.split('_')
            base = self.common_currency_code(baseId.upper())
            quote = self.common_currency_code(quoteId.upper())
            symbol = base + '/' + quote
            active = market['state'] == 1
            precision = {
                'amount': market['amountDecimal'],
                'price': market['priceDecimal'],
            }
            limits = {
                'amount': {
                    'min': self.safe_float(market, 'minAmount'),
                    'max': None,
                },
                'price': {
                    'min': None,
                    'max': None,
                },
                'cost': {
                    'min': None,
                    'max': None,
                },
            }
            result.append({
                'id': market['marketId'],
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'precision': precision,
                'limits': limits,
                'info': market,
            })
        return result

    def fetch_balance(self, page_size=200, page_num=1, params={}):
        self.load_markets()

        request = {
            'pageSize': page_size,
            'pageNum': page_num,
        }

        response = self.private_post_exchange_fund_controller_website_fundcontroller_findbypage(self.extend(params, request))
        balances = response['datas']['list']
        result = {'info': response}
        for balance in balances:
            account = self.account()
            currencyId = str(balance['currencyTypeId'])

            if currencyId in self.currencies_by_id:
                name = self.currencies_by_id[currencyId]['name']
            else:
                name = self.common_currency_code(currencyId)

            account['free'] = float(balance['amount'])
            account['used'] = float(balance['freeze'])
            account['total'] = self.sum(account['free'], account['used'])

            result[name] = account
        return self.parse_balance(result)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()

        request = {
            'marketId': self.market_id(symbol.upper()),
            'price': price,
            'amount': amount,
            'rangeType': 0,
            'type': 1 if 'buy' == side else 0,
        }

        response = self.private_post_exchange_entrust_controller_website_entrustcontroller_addentrust(self.extend(request, params))
        data = response['datas']
        return {
            'info': response,
            'id': self.safe_string(data, 'entrustId'),
            'price': price,
            'amount': amount,
            'side': 1 if side == 'buy' else 0,
        }

    def cancel_order(self, id, symbol=None, params={}):
        """
            取消订单，zbg取消订单，marketId是必须传的，所以symbol不能为空
        """
        if symbol is None:
            raise ExchangeError(self.id + 'cancel_order requires a symbol parameter')

        self.load_markets()
        request = {
            'entrustId': id,
            'marketId': self.market_id(symbol.upper()),
        }

        results = self.private_post_exchange_entrust_controller_website_entrustcontroller_cancelentrust(self.extend(request, params))
        success = results['resMsg']
        returnVal = {'info': results, 'success': success['message']}
        return returnVal

    def cancel_orders(self, symbol, *entrust_ids):
        """
            批量取消订单，zbg取消订单，marketId是必须传的，所以symbol不能为空
        """
        if symbol is None:
            raise ExchangeError(self.id + 'cancel_orders requires a symbol parameter')

        self.load_markets()
        request = {
            'entrustIds': entrust_ids,
            'marketId': self.market_id(symbol.upper()),
        }

        results = self.private_post_exchange_entrust_controller_website_entrustcontroller_batchcancelentrust(request)
        success = results['resMsg']
        return {'info': results, 'success': success['message']}

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + 'fetch_order requires a symbol parameter')

        self.load_markets()
        market = self.market(symbol.upper())

        request = {
            'marketId': self.market_id(symbol),
            'entrustId': id,
        }
        response = self.private_get_exchange_entrust_controller_website_entrustcontroller_getentrustbyid(self.extend(request, params))
        return self.parse_order(response['datas'], market)

    def parse_order(self, order, market=None):
        if order is None:
            raise ExchangeError(self.id + ' 获取订单数据为空')

        timestamp = self.safe_integer(order, 'createTime')
        iso8601 = self.iso8601(timestamp)

        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount')
        filled = self.safe_float(order, 'completeAmount')
        average = self.safe_float(order, 'completeTotalMoney') / filled if filled > 0 else 0
        remaining = amount - filled
        cost = filled * price
        status = self.parse_order_status(self.safe_integer(order, 'status'))
        return {
            'info': order,
            'id': self.safe_string(order, 'entrustId'),
            'datetime': iso8601,
            'timestamp': timestamp,
            'lastTradeTimestamp': timestamp,
            'status': status,
            'symbol': market['symbol'] if market else self.get_symbol(order),
            'type': None,
            'side': 'buy' if order['type'] == 1 else 'sell',
            'price': price,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'cost': cost,
            'average': average,
            'trades': None,
            'fee': None,
        }

    @staticmethod
    def parse_order_status(status):
        if status == 0 or status == 3:
            return 'open'
        elif status == 2:
            return 'closed'
        elif status == 1:
            return 'canceled'
        else:
            return None

    def fetch_orders(self, symbol=None, since=None, limit=50, params={}):
        if symbol is None:
            raise ExchangeError(self.id + 'fetch_orders requires a symbol parameter')

        self.load_markets()
        market = self.market(symbol.upper())
        request = {
            'marketId': market['id'],
            'pageIndex': 1,  # default pageIndex is 1
            'pageSize': limit,  # default pageSize is 50
        }

        if since:
            request['startDateTime'] = since

        response = self.private_get_exchange_entrust_controller_website_entrustcontroller_getuserentrustlist(self.extend(request, params))

        entrust_list = response['datas']['entrustList']
        if not entrust_list:
            return []

        return self.parse_orders(entrust_list, market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=20, params={}):
        """查询未完成成交的的委托记录"""
        if symbol is None:
            raise ExchangeError(self.id + 'fetch_open_orders requires a symbol parameter')

        self.load_markets()
        request = {
            'marketId': self.market_id(symbol.upper()),
            'pageIndex': 1,  # default pageIndex is 1
            'pageSize': limit,  # default pageSize is 20
            'entrustType': 0,  # 委托单类型 0 普通委托单 1 杠杆委托单
        }

        response = self.private_get_exchange_entrust_controller_website_entrustcontroller_getuserentrustrecordfromcachewithpage(
            self.extend(request, params))
        entrust_list = response['datas']['entrustList']
        if not entrust_list:
            return []

        return self.parse_orders(entrust_list, None, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        """查询已经完结委托记录"""
        params['status'] = 2
        return self.fetch_orders(symbol, since, limit, params)

    def fetch_my_trades(self, symbol=None, since=None, limit=50, params={}):
        """
        查询用户某个市场的成交记录
        """
        if symbol is None:
            raise ExchangeError(self.id + 'fetch_my_trades requires a symbol parameter')

        self.load_markets()
        market = self.market(symbol.upper())
        request = {
            'marketId': market['id'],
            'pageNum': 1,  # default pageNum is 1
            'pageSize': limit,  # default pageSize is 20
        }

        if since:
            request['startTime'] = since

        response = self.private_get_exchange_entrust_controller_website_entrustcontroller_gettransactionpage(self.extend(request, params))
        entrust_list = response['datas']['list']
        print(entrust_list)
        return self._parse_my_trades(entrust_list, market, since, limit)

    def _parse_my_trades(self, trades, market=None, since=None, limit=None):
        array = self.to_array(trades)
        array = [self._parse_my_trade(trade, market) for trade in array]
        array = self.sort_by(array, 'timestamp')
        symbol = market['symbol'] if market else None
        return self.filter_by_symbol_since_limit(array, symbol, since, limit)

    def _parse_my_trade(self, trade, market=None):
        if trade is None:
            raise ExchangeError(self.id + ' 获取订单数据为空')

        timestamp = self.safe_integer(trade, 'createTime')

        symbol = market['symbol'] if market else self.get_symbol(trade)
        order_type = self.safe_integer(trade, 'type')
        currency = symbol.split('/')[0] if order_type == 1 else symbol.split('/')[1]

        return {
            'info': trade,
            'id': trade['transrecordId'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': trade['entrustId'] if 'entrustId' in trade.keys() else None,
            'type': None,
            'side': 'buy' if order_type == 1 else 'sell',
            'takerOrMaker': 'maker' if trade['markerFlag'] else 'taker',
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'amount'),
            'cost': self.safe_float(trade, 'totalPrice'),
            'fee': {
                'cost': self.safe_float(trade, 'fee'),
                'currency': currency,
                'rate': None,
            }
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()

        request = {
            'marketId': self.market_id(symbol.upper()),
        }

        response = self.public_get_api_data_v1_ticker(self.extend(request, params))
        data = response['datas']

        return self._parse_ticker(data, symbol)

    def fetch_tickers(self, symbols=None, params={}):
        """所有市场24H市场行情，目前暂不支持特定多个币种的查询"""

        self.load_markets()
        if symbols:
            raise ExchangeError(self.id + 'fetch_tickers does not support the "symbols" parameter')

        request = {
            'isUseMarketName': True,  # 必传，选择true则返回的结果中用BTC_USDT这样的市场名替代掉marketId,false则使用marketId
        }

        response = self.public_get_api_data_v1_tickers(self.extend(request, params))
        datas = response['datas']
        tickers = [self._parse_ticker(data, symbol.replace('_', '/')) for symbol, data in datas.items()]
        return self.to_array(tickers)

    def _parse_ticker(self, data, symbol):
        timestamp = self.milliseconds()

        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': data[2],
            'low': data[3],
            'bid': data[7],
            'bidVolume': None,
            'ask': data[8],
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': data[1],
            'last': data[1],
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': data[4],
            'quoteVolume': None,
            'info': data,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """查询市场交易记录"""
        self.load_markets()

        market = self.markets[symbol.upper()]

        request = {
            'marketId': market['id'],
            'dataSize': min(limit, 20) if limit else 20,
        }

        response = self.public_get_api_data_v1_trades(self.extend(request, params))
        return self.parse_trades(response['datas'], market, since, limit)

    def parse_trade(self, trade, market):
        timestamp = int(trade[2]) * 1000
        amount = float(trade[6])
        price = float(trade[5])
        cost = amount * price
        side = 'buy' if (trade[4] == 'bid') else 'sell'

        return {
            'info': trade,
            'id': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'order': None,
            'fee': None,
        }

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        marketId = self.market_id(symbol.upper())
        request = {
            'marketId': marketId,
        }

        if limit:
            request['dataSize'] = limit

        response = self.public_get_api_data_v1_entrusts(self.extend(request, params))
        data = response['datas']
        timestamp = data['timestamp']

        return self.parse_order_book(data, timestamp)

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol.upper())
        request = {
            'marketId': market['id'],
            'type': timeframe.upper(),
        }

        if limit:
            request['dataSize'] = limit

        response = self.public_get_api_data_v1_klines(self.extend(request, params))
        return self.parse_ohlcvs(response['datas'], market, timeframe, since, limit)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            int(ohlcv[3]) * 1000,  # timestamp
            float(ohlcv[4]),  # // Open
            float(ohlcv[5]),  # // High
            float(ohlcv[6]),  # // Low
            float(ohlcv[7]),  # // Close
            float(ohlcv[8]),  # // vol
        ]

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        request = {
            'currencyTypeName': code
        }

        response = self.private_post_exchange_fund_controller_website_fundcontroller_getpayinaddress(self.extend(request, params))
        data = response['datas']
        address = self.safe_string(data, 'address')
        tag = self.safe_string(data, 'memo')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': tag,
            'info': response,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        if api == 'public':
            url = self.urls['publicapi'] if path.find('api/data/v1') >= 0 else self.urls['api']
            url = url + '/' + path
            if params:
                url += '?' + self.urlencode(params)
        else:
            timestamp = str(self.milliseconds())
            url = self.urls['api'] + '/' + path
            param = ''
            if method == 'GET' and params:
                url = url + '?' + self.urlencode(params)
                for k in sorted(params):
                    param += k + str(params[k])
            elif method == 'POST' and params:
                param = self.json(params)
                body = param

            sig_str = self.apiKey + timestamp + param + self.secret
            signature = hashlib.md5(sig_str.encode('utf-8')).hexdigest()

            headers = {
                'Apiid': self.apiKey,
                'Timestamp': timestamp,
                'Sign': signature
            }

        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, http_code, reason, url, method, headers, body, response):
        if len(body) < 2:
            return  # fallback to default error handler
        if body[0] == '{':
            feedback = self.id + ' ' + self.json(response) + ' url:' + url

            code = self.safe_string(response['resMsg'], 'code')
            if 'code':
                if code in self.exceptions:
                    ExceptionClass = self.exceptions[code]
                    raise ExceptionClass(feedback)
                elif code != '1':
                    raise ExchangeError(feedback)

    def get_symbol(self, record):
        key = record["marketId"] if record["marketId"] in self.markets_by_id.keys() else record["originalMarketId"]
        return self.markets_by_id[key]['symbol']