from pybit.unified_trading import HTTP
import requests

def G1(message,bot,gl_pr,black,pr):
    data_binance = []
    data_bybit = []

    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    response = requests.get(url)
    data_many_f = response.json()

    for coin in data_many_f:
        symbol = coin['symbol']
        price = coin['lastPrice']
        timestamp = coin['closeTime']

    url = "https://fapi.binance.com/fapi/v1/time"
    response = requests.get(url)
    data_t_f = response.json()

    server_time_f = data_t_f['serverTime']

    for i in data_many_f:
        if server_time_f - 86400000 < i['closeTime'] and float(i['lastPrice']) > 0:
            data_binance.append({'symbol': i['symbol'], 'price': i['lastPrice']})

    session = HTTP(
        testnet=False,
        api_key="9kBNn0gpUuXK6s80l4",
        api_secret="mZ3SJCj9FOuBQnVNnad3xqtrZZ0tp7aOm7qN",
        recv_window=60000
    )

    # spot
    # linear

    tickers_spot = session.get_tickers(category="linear")
    for i in tickers_spot['result']['list']:
        if i['symbol'][-1] == 'T':
            data_bybit.append({'symbol': i['symbol'], 'price': i['lastPrice']})

    txt = '📌ОПОВЕЩЕНИЕ!📌\n\n'

    for bin in data_binance:
        for by in data_bybit:
            if bin['symbol'] == by['symbol']:
                x = float(by['price'])
                y = float(bin['price'])
                z = (x / y - 1) * 100
                z = round(z, 5)
                if z < 0:
                    z *= -1
                elif z > 0:
                    pass

                if z >= pr and z <= gl_pr:
                    txt = txt + f"<code>{bin['symbol']}</code>:  {z}% \n⚡️<u>Binance:</u> <b>{bin['price']}</b> FUTURES \n⚡️<u>ByBit:</u> <b>{by['price']}</b> FUTURES \n\n"
    if txt == '📌ОПОВЕЩЕНИЕ!📌\n\n':
        return None
    else:
        return txt


def G2(message,bot,gl_pr,black,pr):
    data_binance = []
    data_bybit = []

    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data_many_s = response.json()

    for coin in data_many_s:
        symbol = coin['symbol']
        price = coin['lastPrice']
        timestamp = coin['closeTime']

    url = "https://api.binance.com/api/v3/time"
    response = requests.get(url)
    data_t_f = response.json()

    server_time_f = data_t_f['serverTime']

    for i in data_many_s:
        if server_time_f - 86400000 < i['closeTime'] and float(i['lastPrice']) > 0:
            data_binance.append({'symbol': i['symbol'], 'price': i['lastPrice']})

    session = HTTP(
        testnet=False,
        api_key="9kBNn0gpUuXK6s80l4",
        api_secret="mZ3SJCj9FOuBQnVNnad3xqtrZZ0tp7aOm7qN",
        recv_window=60000
    )

    # spot
    # linear

    tickers_spot = session.get_tickers(category="linear")
    for i in tickers_spot['result']['list']:
        if i['symbol'][-1] == 'T':
            data_bybit.append({'symbol': i['symbol'], 'price': i['lastPrice']})

    txt = '📌ОПОВЕЩЕНИЕ!📌\n\n'

    for bin in data_binance:
        for by in data_bybit:
            if bin['symbol'] == by['symbol']:
                x = float(by['price'])
                y = float(bin['price'])
                z = (x / y - 1) * 100
                z = round(z, 5)
                if z < 0:
                    z *= -1
                elif z > 0:
                    pass

                if z >= pr and z <= gl_pr:
                    txt = txt + f"<code>{bin['symbol']}</code>:  {z}% \n⚡️<u>Binance:</u> <b>{bin['price']}</b> SPOT \n⚡️<u>ByBit:</u> <b>{by['price']}</b> FUTURES \n\n"
    if txt == '📌ОПОВЕЩЕНИЕ!📌\n\n':
        return None
    else:
        return txt
def G3(message,bot,gl_pr,black,pr):
    data_binance = []
    data_bybit = []

    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    response = requests.get(url)
    data_many_f = response.json()

    for coin in data_many_f:
        symbol = coin['symbol']
        price = coin['lastPrice']
        timestamp = coin['closeTime']

    url = "https://fapi.binance.com/fapi/v1/time"
    response = requests.get(url)
    data_t_f = response.json()

    server_time_f = data_t_f['serverTime']

    for i in data_many_f:
        if server_time_f - 86400000 < i['closeTime'] and float(i['lastPrice']) > 0:
            data_binance.append({'symbol': i['symbol'], 'price': i['lastPrice']})

    session = HTTP(
        testnet=False,
        api_key="9kBNn0gpUuXK6s80l4",
        api_secret="mZ3SJCj9FOuBQnVNnad3xqtrZZ0tp7aOm7qN",
        recv_window=60000
    )

    # spot
    # linear

    tickers_spot = session.get_tickers(category="spot")
    for i in tickers_spot['result']['list']:
        if i['symbol'][-1] == 'T':
            data_bybit.append({'symbol': i['symbol'], 'price': i['lastPrice']})

    txt = '📌ОПОВЕЩЕНИЕ!📌\n\n'

    for bin in data_binance:
        for by in data_bybit:
            if bin['symbol'] == by['symbol']:
                x = float(by['price'])
                y = float(bin['price'])
                z = (x / y - 1) * 100
                z = round(z, 5)
                if z < 0:
                    z *= -1
                elif z > 0:
                    pass

                if z >= pr and z <= gl_pr:
                    txt = txt + f"<code>{bin['symbol']}</code>:  {z}% \n⚡️<u>Binance:</u> <b>{bin['price']}</b> FUTURES \n⚡️<u>ByBit:</u> <b>{by['price']}</b> SPOT \n\n"
    if txt == '📌ОПОВЕЩЕНИЕ!📌\n\n':
        return None
    else:
        return txt


def moex():
    def get_moex_stocks_with_prices():
        url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
        response = requests.get(url)
        data = response.json()
        f = []
        stocks = data["securities"]["data"]
        for stock in stocks:
            ticker, name, price = stock[2], stock[0], stock[3]
            f.append({'ticker': ticker, 'name': name, 'price': price})

        return f

    z = get_moex_stocks_with_prices()
    p = []
    for i in z:
        if i['name'][-1] == 'P':
            p.append(i)

    txt = '📌ОПОВЕЩЕНИЕ!📌\n\n'

    for P in p:
        for i in z:
            r = list(P['name'])
            r[-1] = ''
            r = ''.join(r)
            if i['name'] == r:
                # if i['name'][0] == 'S' or i['name'][0] == 's':
                x = (float(i['price']) / float(P['price']) - 1) * 100

                if x < 0:
                    x *= -1
                bl = ['KAZT', 'KGKC', 'KRKN', 'KRSB', 'MISB', 'SAGO', 'STSB', 'BANE']
                x = round(x, 5)

                if x <= 20:
                    if i['name'] in bl:
                        pass
                    else:
                        txt = txt + (f"✅ {x}%\n"
                                     f"📍 {i['ticker']} : {i['name']}👉{i['price']}\n"
                                     f"📍 {P['ticker']} : {P['name']}👉{P['price']}\n\n")

    if txt == '📌ОПОВЕЩЕНИЕ!📌\n\n':
        return None
    else:
        return txt
