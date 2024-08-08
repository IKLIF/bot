from pybit.unified_trading import HTTP
import telebot
from telebot import types
import threading
import requests
import time
import sqlite3
from threading import Thread

API = '7442583453:AAEEhPn5qFnc6TvYjwFGVyo93aIL4GvD6d8'
bot = telebot.TeleBot(API)

conn = sqlite3.connect('OI.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS parametrs ('
               'nam FLOAT,'
               'pr_max FLOAT,'
               'pr_min FLOAT,'
               'chat_main_id INTEGER'
               ')')

cursor.execute('CREATE TABLE IF NOT EXISTS parametrs_b ('
               'nam FLOAT,'
               'pr_max FLOAT,'
               'pr_min FLOAT,'
               'chat_main_id INTEGER'
               ')')

x0 = 0
x1 = 2.5
x2 = 2.5
x1_ = 8
x2_ = 8
x3 = -1002208711059
cursor.execute('SELECT * FROM parametrs')
if cursor.fetchone() == None:
    cursor.execute('INSERT INTO parametrs (nam, pr_max, pr_min, chat_main_id) VALUES (?,?,?,?)', (x0, x1,x2,x3,))
    conn.commit()
    cursor.execute('INSERT INTO parametrs_b (nam, pr_max, pr_min, chat_main_id) VALUES (?,?,?,?)', (x0, x1,x2,x3,))
    conn.commit()


conn.close()




def volue(symbol):
    try:
        url = f'https://api.binance.com/api/v3/klines'
        params = {
                'symbol': symbol,
                'interval': '5m',  # Интервал - 1 час
                'limit': 24,  # 24 часа
                }

        response = requests.get(url, params=params)
        data_back = response.json()

        url = f'https://api.binance.com/api/v3/klines'
        params = {
                'symbol': symbol,
                'interval': '5m',  # Интервал - 1 час
                'limit': 12,  # 24 часа
                }

        response = requests.get(url, params=params)
        data_now = response.json()

        data_back = [data_back[i][5] for i in range(0,12)]

        #for i in data_back:
         #   i[0] = pd.to_datetime(i[0], unit='ms')
          #  print(f'timestamp: {i[0]}, open: {i[1]}, high: {i[2]}, low: {i[3]}, close: {i[4]}, volume: {i[5]}, close_time: {i[6]}, quote_asset_volume:{i[7]}, trades: {i[8]}, taker_buy_base: {i[9]}, taker_buy_quote: {i[10]}')

        all = 0
        for i in data_back:
            all += float(i)

        all /= 12


        data_now = [i[5] for i in data_now]
        all_now = 0
        for i in data_now:
            all_now += float(i)

        all_sr = all_now/12

        #z = (x / y - 1) * 100
        pr_all = (all_sr-all)/all_sr * 100#(data_vol_now - data_back_vol_sr)/data_vol_now * 100
        pr_all = round(pr_all, 3)
        return f'📌Volume: 👉 {pr_all}%'

    except Exception as e:
        pass
        #print('\nОшибка:\n', traceback.format_exc())

def trades(symbol):
    try:
        url = f'https://api.binance.com/api/v3/klines'
        params = {
            'symbol': symbol,
            'interval': '5m',  # Интервал - 1 час
            'limit': 96,  # 24 часа
        }

        response = requests.get(url, params=params)
        data_back = response.json()

        x = 0
        for i in data_back:
            print(i[8])
            x += i[8]


        return f'📌Trades:(8h) 👉 {x}'

    except Exception as e:
        pass
        #print('\nОшибка:\n', traceback.format_exc())



def sombol():
    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    response = requests.get(url)
    data_many_f = response.json()

    data = []

    for coin in data_many_f:
        symbol = coin['symbol']
        if symbol[-1] == 'T':
            data.append({'symbol':coin['symbol'], 'priceChangePercent':coin['priceChangePercent']})

    return data


def get_open_interest(symbol):
    base_url = "https://fapi.binance.com"
    endpoint = "/futures/data/openInterestHist"
    params = {
        "symbol": symbol,
        "period": "5m",  # Интервал времени (5 минут, 1 час, 1 день и т. д.)
        "limit": 48  # Количество записей
    }

    response = requests.get(base_url + endpoint, params=params)
    data = response.json()
    print('Binance')
    return data


def start_main():
    kol_vo =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    main(kol_vo)



def main(kol_vo):
    kol_vo.pop(0)
    kol_vo.append([])



    conn = sqlite3.connect('OI.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM parametrs WHERE nam = ?', (0,))
    result = cursor.fetchone()

    pr_max = result[1]
    pr_min = result[2]
    chat_main_id = result[3]

    conn.close()

    result_symbol = sombol()
    #print('---------------------------------------------')
    #print(f'len: {len(result_symbol)}')
    #print('---------------------------------------------')

    for i in result_symbol:
        try:
            priceChangePercent = round(float(i['priceChangePercent']), 1)
            symbol__ = i['symbol']

            result_get_open_interest = get_open_interest(i['symbol'])
            data_back = [result_get_open_interest[i]['sumOpenInterest'] for i in range(44, 46)]  # sumOpenInterestValue
            data_back_vol = [result_get_open_interest[i]['sumOpenInterestValue'] for i in range(44, 46)]  # sumOpenInterestValue

            data_back_sr = 0
            data_back_vol_sr = 0

            for i in data_back:
                data_back_sr += float(i)

            for i in data_back_vol:
                data_back_vol_sr += float(i)

            data_back_sr = data_back_sr / 2
            data_back_vol_sr = data_back_vol_sr / 2

            data_now = (float(result_get_open_interest[-1]['sumOpenInterest'])) / 1  # (float(result_get_open_interest[-1]['sumOpenInterest']) + float(result_get_open_interest[-2]['sumOpenInterest']) + float(result_get_open_interest[-3]['sumOpenInterest']) + float(result_get_open_interest[-4]['sumOpenInterest'])+ float(result_get_open_interest[-5]['sumOpenInterest'])+ float(result_get_open_interest[-6]['sumOpenInterest'])+ float(result_get_open_interest[-7]['sumOpenInterest'])+ float(result_get_open_interest[-8]['sumOpenInterest'])+ float(result_get_open_interest[-9]['sumOpenInterest'])+ float(result_get_open_interest[-10]['sumOpenInterest'])+ float(result_get_open_interest[-11]['sumOpenInterest'])+ float(result_get_open_interest[-12]['sumOpenInterest'])+ float(result_get_open_interest[-13]['sumOpenInterest'])+ float(result_get_open_interest[-14]['sumOpenInterest']))/14
            data_vol_now = (float(result_get_open_interest[-1]['sumOpenInterestValue']))/ 1  # (float(result_get_open_interest[-1]['sumOpenInterestValue']) + float(result_get_open_interest[-2]['sumOpenInterestValue']) + float(result_get_open_interest[-3]['sumOpenInterestValue']) + float(result_get_open_interest[-4]['sumOpenInterestValue'])+ float(result_get_open_interest[-5]['sumOpenInterestValue'])+ float(result_get_open_interest[-6]['sumOpenInterestValue'])+ float(result_get_open_interest[-7]['sumOpenInterestValue'])+ float(result_get_open_interest[-8]['sumOpenInterestValue'])+ float(result_get_open_interest[-9]['sumOpenInterestValue'])+ float(result_get_open_interest[-10]['sumOpenInterestValue'])+ float(result_get_open_interest[-11]['sumOpenInterestValue'])+ float(result_get_open_interest[-12]['sumOpenInterestValue'])+ float(result_get_open_interest[-13]['sumOpenInterestValue'])+ float(result_get_open_interest[-14]['sumOpenInterestValue']))/14

            pr_all = (data_now - data_back_sr)/data_now * 100
            pr_all = round(pr_all, 3)

            pr_vol_all = (data_vol_now - data_back_vol_sr)/data_vol_now * 100#(data_back_vol_sr / data_vol_now - 1) * 100
            pr_vol_all = round(pr_vol_all, 3)

            pr_4h = (float(result_get_open_interest[-1]['sumOpenInterest']) - float(result_get_open_interest[1]['sumOpenInterest']))/float(result_get_open_interest[-1]['sumOpenInterest'])*100
            pr_4h = round(pr_4h, 3)
            if pr_4h>0:
                txt_pr_4h =f'↗️<i>OI: Chg%4h=</i> <b><u>{pr_4h}%</u></b>\n'
            elif pr_4h<0:
                txt_pr_4h =f'↘️<i>OI: Chg%4h=</i> <b><u>{pr_4h}%</u></b>\n'
            else:
                txt_pr_4h =f''

            zzzz = f'📍Открытый интерес: 👉 {pr_all}%'
            zzzz_vol = f'📍Общий открытый интерес: 👉 {pr_vol_all}%'

            markup = types.InlineKeyboardMarkup()

            b1 = types.InlineKeyboardButton(text='TV',
                                            url=f"https://ru.tradingview.com/chart/{result_get_open_interest[0]['symbol']}.P")
            b2 = types.InlineKeyboardButton(text='CG',
                                            url=f"https://www.coinglass.com/tv/ru/Binance_{result_get_open_interest[0]['symbol']}")
            b3 = types.InlineKeyboardButton(text='ПЕРЕХОДИТЬ В БОТ',
                                            url=f"https://t.me/+JnErqgdsSuBmZWRi")
            markup.add(b1, b2)
            markup.add(b3)
            if pr_all > pr_max:

                kol_vo[-1].append(result_get_open_interest[0]['symbol'])

                kol_vo_nam = 0
                for k in kol_vo:
                    for i in k:
                        if i == result_get_open_interest[0]['symbol']:
                            kol_vo_nam += 1

                result_trades = trades(symbol__)
                if result_trades == None:
                    result_trades = 'NONE'
                result_volue = volue(symbol__)
                if result_volue == None:
                    result_volue = 'NONE'


                if result_trades != 'NONE' and result_volue != 'NONE':
                    bot.send_message(chat_main_id,
                                     f"🟩📈<code>{result_get_open_interest[0]['symbol']}</code> \n🟡#Binance\n#{result_get_open_interest[0]['symbol']} #UP\n\n{zzzz}\n{zzzz_vol}\n\n{result_volue}\n{result_trades}\n\n{txt_pr_4h}<i>Сoin: Chg%24h=</i> <b><u>{priceChangePercent}%</u></b>\n За 6ч: {kol_vo_nam}",
                                     parse_mode='HTML', reply_markup=markup)
                else:
                    bot.send_message(chat_main_id,
                                     f"🟩📈<code>{result_get_open_interest[0]['symbol']}</code> \n🟡#Binance\n#{result_get_open_interest[0]['symbol']} #UP\n\n{zzzz}\n{zzzz_vol}\n\n{txt_pr_4h}<i>Сoin: Chg%24h=</i> <b><u>{priceChangePercent}%</u></b>\n За 6ч: {kol_vo_nam}",
                                     parse_mode='HTML', reply_markup=markup)


                time.sleep(2)
            if pr_all < -pr_min:

                kol_vo[-1].append(result_get_open_interest[0]['symbol'])

                kol_vo_nam = 0
                for k in kol_vo:
                    for i in k:
                        if i == result_get_open_interest[0]['symbol']:
                            kol_vo_nam += 1


                result_trades = trades(symbol__)
                if result_trades == None:
                    result_trades = 'NONE'
                result_volue = volue(symbol__)
                if result_volue == None:
                    result_volue = 'NONE'


                if result_trades != 'NONE' and result_volue != 'NONE':
                    bot.send_message(chat_main_id,
                                     f"🟥📉<code>{result_get_open_interest[0]['symbol']}</code> \n🟡#Binance\n#{result_get_open_interest[0]['symbol']} #DOWN\n\n{zzzz}\n{zzzz_vol}\n\n{result_volue}\n{result_trades}\n\n{txt_pr_4h}<i>Сoin: Chg%24h=</i> <b><u>{priceChangePercent}%</u></b>\n За 6ч: {kol_vo_nam}",
                                     parse_mode='HTML', reply_markup=markup)
                else:
                    bot.send_message(chat_main_id,
                                     f"🟥📉<code>{result_get_open_interest[0]['symbol']}</code> \n🟡#Binance\n#{result_get_open_interest[0]['symbol']} #DOWN\n\n{zzzz}\n{zzzz_vol}\n\n{txt_pr_4h}<i>Сoin: Chg%24h=</i> <b><u>{priceChangePercent}%</u></b>\n За 6ч: {kol_vo_nam}",
                                     parse_mode='HTML', reply_markup=markup)


                time.sleep(2)
        except Exception as e:
            #print('\nОшибка:\n', traceback.format_exc())
            #print(i)
            pass


    time.sleep(10)
    main(kol_vo)


def get_open_interest_bybit(symbol):
    session = HTTP(
        testnet=False,
        api_key="9kBNn0gpUuXK6s80l4",
        api_secret="mZ3SJCj9FOuBQnVNnad3xqtrZZ0tp7aOm7qN",
        recv_window=60000
    )

    result = session.get_open_interest(symbol=symbol, category='linear', intervalTime='5min', limit=48)
    data_interes = result['result']['list']
    data_interes.reverse()
    print('ByBit')
    return data_interes



def sombol_bybit():
    session = HTTP(
        testnet=False,
        api_key="9kBNn0gpUuXK6s80l4",
        api_secret="mZ3SJCj9FOuBQnVNnad3xqtrZZ0tp7aOm7qN",
        recv_window=60000
    )

    # spot
    # linear

    tickers_spot = session.get_tickers(category="linear")
    data_tickers = tickers_spot['result']['list']

    return data_tickers

#sombol_bybit()
#get_open_interest_bybit('BTCUSDT')

def start_main_Bybit():
    kol_vo =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    main_Bybit(kol_vo)

def main_Bybit(kol_vo):
    kol_vo.pop(0)
    kol_vo.append([])



    conn = sqlite3.connect('OI.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM parametrs_b WHERE nam = ?', (0,))
    result = cursor.fetchone()

    pr_max = result[1]
    pr_min = result[2]
    chat_main_id = result[3]

    conn.close()

    result_symbol_bybit = sombol_bybit()
    #print('---------------------------------------------')
    #print(f'len: {len(result_symbol)}')
    #print('---------------------------------------------')
    for i in result_symbol_bybit:
        try:
            symbol__ = i['symbol']
            data_i = i
            result_get_open_interest_bybit = get_open_interest_bybit(symbol__)

            data_back = [result_get_open_interest_bybit[i]['openInterest'] for i in range(44, 46)]  # sumOpenInterestValue
            #data_back_vol = [result_get_open_interest_bybit[i]['sumOpenInterestValue'] for i in range(44, 46)]  # sumOpenInterestValue

            data_back_sr = 0

            for i in data_back:
                data_back_sr += float(i)


            data_back_sr = data_back_sr / 2

            data_now = (float(result_get_open_interest_bybit[-1]['openInterest'])) / 1  # (float(result_get_open_interest[-1]['sumOpenInterest']) + float(result_get_open_interest[-2]['sumOpenInterest']) + float(result_get_open_interest[-3]['sumOpenInterest']) + float(result_get_open_interest[-4]['sumOpenInterest'])+ float(result_get_open_interest[-5]['sumOpenInterest'])+ float(result_get_open_interest[-6]['sumOpenInterest'])+ float(result_get_open_interest[-7]['sumOpenInterest'])+ float(result_get_open_interest[-8]['sumOpenInterest'])+ float(result_get_open_interest[-9]['sumOpenInterest'])+ float(result_get_open_interest[-10]['sumOpenInterest'])+ float(result_get_open_interest[-11]['sumOpenInterest'])+ float(result_get_open_interest[-12]['sumOpenInterest'])+ float(result_get_open_interest[-13]['sumOpenInterest'])+ float(result_get_open_interest[-14]['sumOpenInterest']))/14

            pr_all = (data_now - data_back_sr)/data_now * 100
            pr_all = round(pr_all, 3)

            pr_4h = (float(result_get_open_interest_bybit[-1]['openInterest']) - float(result_get_open_interest_bybit[1]['openInterest']))/float(result_get_open_interest_bybit[-1]['openInterest'])*100
            pr_4h = round(pr_4h, 3)
            if pr_4h>0:
                txt_pr_4h =f'↗️<i>OI: Chg%4h=</i> <b><u>{pr_4h}%</u></b>\n'
            elif pr_4h<0:
                txt_pr_4h =f'↘️<i>OI: Chg%4h=</i> <b><u>{pr_4h}%</u></b>\n'
            else:
                txt_pr_4h =f''

            zzzz = f'📍Открытый интерес: 👉 {pr_all}%'
            #zzzz_vol = f'📍Общий открытый интерес: 👉 {pr_vol_all}%'

            markup = types.InlineKeyboardMarkup()

            b1 = types.InlineKeyboardButton(text='TV',
                                            url=f"https://ru.tradingview.com/chart/{symbol__}.P")
            b2 = types.InlineKeyboardButton(text='CG',
                                            url=f"https://www.coinglass.com/tv/ru/Bybit_{symbol__}")
            b3 = types.InlineKeyboardButton(text='ПЕРЕХОДИТЬ В БОТ',
                                            url=f"https://t.me/+JnErqgdsSuBmZWRi")
            markup.add(b1, b2)
            markup.add(b3)

            if pr_all > pr_max:

                kol_vo[-1].append(symbol__)

                kol_vo_nam = 0
                for k in kol_vo:
                    for i in k:
                        if i == symbol__:
                            kol_vo_nam += 1

                #result_trades = trades(symbol__)
                #if result_trades == None:
                #    result_trades = 'NONE'
                #result_volue = volue(symbol__)
                #if result_volue == None:
                #    result_volue = 'NONE'


                #if result_trades != 'NONE' and result_volue != 'NONE':
                #    bot.send_message(chat_main_id,
                #                     f"🟩📈<code>{symbol__}</code> \n#{symbol__} #UP\n\n{zzzz}\n{None}\n\n{result_volue}\n{result_trades}\n\n{txt_pr_4h}<i>Сoin: Chg%24h=</i> <b><u>{None}%</u></b>\n За 6ч: {kol_vo_nam}",
                #                     parse_mode='HTML', reply_markup=markup)
                #else:
                bot.send_message(chat_main_id,
                                     f"🟩📈<code>{symbol__}</code> \n⚫️#ByBit \n#{symbol__} #UP\n\n{zzzz}\n\n{txt_pr_4h}<i>Сoin: Chg%24h=</i> <b><u>{round(float(data_i['price24hPcnt']), 3)}%</u></b>\n За 6ч: {kol_vo_nam}",
                                     parse_mode='HTML', reply_markup=markup)


                time.sleep(2)
            if pr_all < -pr_min:

                kol_vo[-1].append(symbol__)

                kol_vo_nam = 0
                for k in kol_vo:
                    for i in k:
                        if i == symbol__:
                            kol_vo_nam += 1


                #result_trades = trades(symbol__)
                #if result_trades == None:
                #    result_trades = 'NONE'
                #result_volue = volue(symbol__)
                #if result_volue == None:
                #    result_volue = 'NONE'


                #if result_trades != 'NONE' and result_volue != 'NONE':
                    #bot.send_message(chat_main_id,
                                     #f"🟥📉<code>{result_get_open_interest[0]['symbol']}</code> \n#{result_get_open_interest[0]['symbol']} #DOWN\n\n{zzzz}\n{zzzz_vol}\n\n{result_volue}\n{result_trades}\n\n{txt_pr_4h}<i>Сoin: Chg%24h=</i> <b><u>{priceChangePercent}%</u></b>\n За 6ч: {kol_vo_nam}",
                                     #parse_mode='HTML', reply_markup=markup)
                #else:
                bot.send_message(chat_main_id,
                                     f"🟥📉<code>{symbol__}</code> \n⚫️#ByBit \n#{symbol__} #DOWN\n\n{zzzz}\n\n{txt_pr_4h}<i>Сoin: Chg%24h=</i> <b><u>{round(float(data_i['price24hPcnt']), 3)}%</u></b>\n За 6ч: {kol_vo_nam}",
                                     parse_mode='HTML', reply_markup=markup)


                time.sleep(2)
        except Exception as e:
            #print('\nОшибка:\n', traceback.format_exc())
            #print(i)
            pass


    time.sleep(10)
    main_Bybit(kol_vo)







@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, 'Мы приветствуем тебя трейдер. На все вопросы я отвечаю в группе👍\n\n'
                                      '/PARBI - Параметры на Binance\n\n'
                                      '/UPDBI - Обновить параметры Binance\n\n'
                                      '/PARBY - Параметры на Bybit\n\n'
                                      '/UPDBY - Обновить параметры Bybit')

@bot.message_handler(commands=['PARBI'])
def PARAMETERS(message):
    conn = sqlite3.connect('OI.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM parametrs WHERE nam = ?', (0,))
    result = cursor.fetchone()

    pr_max = result[1]
    pr_min = result[2]
    chat_main_id = result[3]

    conn.close()

    bot.send_message(message.chat.id, f'NOW parameters:\n\n1: {pr_max} - x>n\n\n2: {pr_min} - x<-n\n\n3: {chat_main_id}')


@bot.message_handler(commands=['UPDBI'])
def UPDATE(message):
    conn = sqlite3.connect('OI.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM parametrs WHERE nam = ?', (0,))
    result = cursor.fetchone()

    pr_max = result[1]
    pr_min = result[2]
    chat_main_id = result[3]

    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton(pr_max)
    b2 = types.KeyboardButton(pr_min)
    b3 = types.KeyboardButton(chat_main_id)
    markup.add(b1, b2, b3)
    bot.send_message(message.chat.id, f'NOW parameters:\n\n1: {pr_max} - x>n\n\n2: {pr_min} - x<-n\n\n3: {chat_main_id}\n\nВведите первый параметр:', reply_markup=markup)
    bot.register_next_step_handler(message, UPDATE_0)

def UPDATE_0(message):
    try:
        txt = float(message.text)
        data = [txt]

        bot.send_message(message.chat.id,'Введите второй параметр:')
        bot.register_next_step_handler(message, UPDATE_1, data)
    except:
        bot.send_message(message.chat.id,
                         f'ERROR')
        bot.register_next_step_handler(message, UPDATE_0)


def UPDATE_1(message, data):
    try:
        txt = float(message.text)
        data.append(txt)
        bot.send_message(message.chat.id,'Введите третий параметр:')
        bot.register_next_step_handler(message, UPDATE_2, data)
    except:
        bot.send_message(message.chat.id,
                         f'ERROR')
        bot.register_next_step_handler(message, UPDATE_1, data)

def UPDATE_2(message, data):
    try:
        txt = int(message.text)
        data.append(txt)
        save(message, data)
    except Exception as e:
        #print('\nОшибка:\n', traceback.format_exc())
        bot.send_message(message.chat.id,
                         f'ERROR')
        #print('ERROR')
        bot.register_next_step_handler(message, UPDATE_2, data)

def save(message, data):
    new_nam = 0
    new_pr_max = data[0]
    new_pr_min = data[1]
    new_chat_main_id = data[2]


    conn = sqlite3.connect('OI.db', check_same_thread=False)
    cursor = conn.cursor()

    # Запрос на обновление строки с новыми параметрами
    update_query = '''
        UPDATE parametrs
        SET pr_max = ?, pr_min = ?, chat_main_id = ?
        WHERE nam = ?
    '''

    # Выполнение запроса на обновление
    cursor.execute(update_query, (new_pr_max, new_pr_min, new_chat_main_id, new_nam))

    # Сохранение изменений в базе данных
    conn.commit()
    conn.close()
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, f'SAVE parameters:\n\n1: {new_pr_max} - x>n\n\n2: {new_pr_min} - x<-n\n\n3: {new_chat_main_id}', reply_markup=a)

@bot.message_handler(commands=['PARBY'])
def PARAMETERS(message):
    conn = sqlite3.connect('OI.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM parametrs_b WHERE nam = ?', (0,))
    result = cursor.fetchone()

    pr_max = result[1]
    pr_min = result[2]
    chat_main_id = result[3]

    conn.close()

    bot.send_message(message.chat.id, f'NOW parameters:\n\n1: {pr_max} - x>n\n\n2: {pr_min} - x<-n\n\n3: {chat_main_id}')


@bot.message_handler(commands=['UPDBY'])
def UPDATE(message):
    conn = sqlite3.connect('OI.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM parametrs_b WHERE nam = ?', (0,))
    result = cursor.fetchone()

    pr_max = result[1]
    pr_min = result[2]
    chat_main_id = result[3]

    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton(pr_max)
    b2 = types.KeyboardButton(pr_min)
    b3 = types.KeyboardButton(chat_main_id)
    markup.add(b1, b2, b3)
    bot.send_message(message.chat.id, f'NOW parameters:\n\n1: {pr_max} - x>n\n\n2: {pr_min} - x<-n\n\n3: {chat_main_id}\n\nВведите первый параметр:', reply_markup=markup)
    bot.register_next_step_handler(message, UPDATE_0_bybit)

def UPDATE_0_bybit(message):
    try:
        txt = float(message.text)
        data = [txt]

        bot.send_message(message.chat.id,'Введите второй параметр:')
        bot.register_next_step_handler(message, UPDATE_1_bybit, data)
    except:
        bot.send_message(message.chat.id,
                         f'ERROR')
        bot.register_next_step_handler(message, UPDATE_0_bybit)


def UPDATE_1_bybit(message, data):
    try:
        txt = float(message.text)
        data.append(txt)
        bot.send_message(message.chat.id,'Введите третий параметр:')
        bot.register_next_step_handler(message, UPDATE_2_bybit, data)
    except:
        bot.send_message(message.chat.id,
                         f'ERROR')
        bot.register_next_step_handler(message, UPDATE_1_bybit, data)

def UPDATE_2_bybit(message, data):
    try:
        txt = int(message.text)
        data.append(txt)
        save_bybit(message, data)
    except Exception as e:
        #print('\nОшибка:\n', traceback.format_exc())
        bot.send_message(message.chat.id,
                         f'ERROR')
        #print('ERROR')
        bot.register_next_step_handler(message, UPDATE_2_bybit, data)

def save_bybit(message, data):
    new_nam = 0
    new_pr_max = data[0]
    new_pr_min = data[1]
    new_chat_main_id = data[2]


    conn = sqlite3.connect('OI.db', check_same_thread=False)
    cursor = conn.cursor()

    # Запрос на обновление строки с новыми параметрами
    update_query = '''
        UPDATE parametrs_b
        SET pr_max = ?, pr_min = ?, chat_main_id = ?
        WHERE nam = ?
    '''

    # Выполнение запроса на обновление
    cursor.execute(update_query, (new_pr_max, new_pr_min, new_chat_main_id, new_nam))

    # Сохранение изменений в базе данных
    conn.commit()
    conn.close()
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, f'SAVE parameters:\n\n1: {new_pr_max} - x>n\n\n2: {new_pr_min} - x<-n\n\n3: {new_chat_main_id}', reply_markup=a)





def many():
    conn = sqlite3.connect('OI.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM parametrs_b WHERE nam = ?', (0,))
    result = cursor.fetchone()

    pr_max = result[1]
    pr_min = result[2]
    chat_main_id = result[3]

    conn.close()

    bot.send_message(chat_main_id,'')
    time.sleep(2700)


def GO():
    thread1 = Thread(target=start_main)
    thread1.start()
    thread2 = Thread(target=start_main_Bybit)
    thread2.start()
    #thread3 = Thread(target=many)
    #thread3.start()
    #Process(target=start_main).start()
    #Process(target=start_main_Bybit).start()

if __name__ == '__main__':
    thread = threading.Thread(target=GO)
    thread.start()
    bot.polling(none_stop=True, timeout=123)












