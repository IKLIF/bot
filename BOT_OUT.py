import telebot
from telebot import types
import threading
import requests
import time
import traceback
import sqlite3


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

cursor.execute('CREATE TABLE IF NOT EXISTS parametrs ('
               'nam FLOAT,'
               'pr_max FLOAT,'
               'pr_min FLOAT,'
               'chat_main_id INTEGER'
               ')')

x0 = 0
x1 = 2
x2 = 2
x3 = -4223979059
cursor.execute('SELECT * FROM parametrs')
if cursor.fetchone() == None:
    cursor.execute('INSERT INTO parametrs (nam, pr_max, pr_min, chat_main_id) VALUES (?,?,?,?)', (x0, x1,x2,x3,))
    conn.commit()


conn.close()


def volue(symbol):
    try:
        url = f'https://api.binance.com/api/v3/klines'
        params = {
                'symbol': symbol,
                'interval': '5m',  # Интервал - 1 час
                'limit': 576,  # 24 часа
                }

        response = requests.get(url, params=params)
        data_back = response.json()

        url = f'https://api.binance.com/api/v3/klines'
        params = {
                'symbol': symbol,
                'interval': '5m',  # Интервал - 1 час
                'limit': 14,  # 24 часа
                }

        response = requests.get(url, params=params)
        data_now = response.json()

        data_back = [data_back[i][5] for i in range(0,288)]

        #for i in data_back:
         #   i[0] = pd.to_datetime(i[0], unit='ms')
          #  print(f'timestamp: {i[0]}, open: {i[1]}, high: {i[2]}, low: {i[3]}, close: {i[4]}, volume: {i[5]}, close_time: {i[6]}, quote_asset_volume:{i[7]}, trades: {i[8]}, taker_buy_base: {i[9]}, taker_buy_quote: {i[10]}')

        all = 0
        for i in data_back:
            all += float(i)

        all /= 288


        data_now = [i[5] for i in data_now]
        all_now = 0
        for i in data_now:
            all_now += float(i)

        all_sr = all_now/14

        #z = (x / y - 1) * 100
        pr_all = (all_sr/all-1)*100
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
                'limit': 576,  # 24 часа
                }

        response = requests.get(url, params=params)
        data_back = response.json()

        url = f'https://api.binance.com/api/v3/klines'
        params = {
                'symbol': symbol,
                'interval': '5m',  # Интервал - 1 час
                'limit': 14,  # 24 часа
                }

        response = requests.get(url, params=params)
        data_now = response.json()

        data_back = [data_back[i][8] for i in range(0,288)]

        #for i in data_back:
         #   i[0] = pd.to_datetime(i[0], unit='ms')
          #  print(f'timestamp: {i[0]}, open: {i[1]}, high: {i[2]}, low: {i[3]}, close: {i[4]}, volume: {i[5]}, close_time: {i[6]}, quote_asset_volume:{i[7]}, trades: {i[8]}, taker_buy_base: {i[9]}, taker_buy_quote: {i[10]}')

        all = 0
        for i in data_back:
            all += float(i)

        all /= 288


        data_now = [i[8] for i in data_now]
        all_now = 0
        for i in data_now:
            all_now += float(i)

        all_sr = all_now/14

        #z = (x / y - 1) * 100
        pr_all = (all_sr/all-1)*100
        pr_all = round(pr_all, 3)


        return f'📌Traders: 👉 {pr_all}%'

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
        "limit": 24  # Количество записей
    }

    response = requests.get(base_url + endpoint, params=params)
    data = response.json()

    return data


def start_main():
    kol_vo =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
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
            data_back = [result_get_open_interest[i]['sumOpenInterest'] for i in range(0, 12)]  # sumOpenInterestValue
            data_back_vol = [result_get_open_interest[i]['sumOpenInterestValue'] for i in range(0, 12)]  # sumOpenInterestValue

            data_back_sr = 0
            data_back_vol_sr = 0

            for i in data_back:
                data_back_sr += float(i)

            for i in data_back_vol:
                data_back_vol_sr += float(i)

            data_back_sr = data_back_sr / 12
            data_back_vol_sr = data_back_vol_sr / 12

            data_now = (float(result_get_open_interest[-1]['sumOpenInterest']) + float(
                result_get_open_interest[-2]['sumOpenInterest']) + float(
                result_get_open_interest[-3]['sumOpenInterest']) + float(
                result_get_open_interest[-4]['sumOpenInterest']) + float(
                result_get_open_interest[-5]['sumOpenInterest']) + float(result_get_open_interest[-6][
                                                                             'sumOpenInterest'])+ float(result_get_open_interest[-7]['sumOpenInterest'])+ float(result_get_open_interest[-8]['sumOpenInterest'])+ float(result_get_open_interest[-9]['sumOpenInterest'])+ float(result_get_open_interest[-10]['sumOpenInterest'])+ float(result_get_open_interest[-11]['sumOpenInterest'])+ float(result_get_open_interest[-12]['sumOpenInterest'])) / 12  # (float(result_get_open_interest[-1]['sumOpenInterest']) + float(result_get_open_interest[-2]['sumOpenInterest']) + float(result_get_open_interest[-3]['sumOpenInterest']) + float(result_get_open_interest[-4]['sumOpenInterest'])+ float(result_get_open_interest[-5]['sumOpenInterest'])+ float(result_get_open_interest[-6]['sumOpenInterest'])+ float(result_get_open_interest[-7]['sumOpenInterest'])+ float(result_get_open_interest[-8]['sumOpenInterest'])+ float(result_get_open_interest[-9]['sumOpenInterest'])+ float(result_get_open_interest[-10]['sumOpenInterest'])+ float(result_get_open_interest[-11]['sumOpenInterest'])+ float(result_get_open_interest[-12]['sumOpenInterest'])+ float(result_get_open_interest[-13]['sumOpenInterest'])+ float(result_get_open_interest[-14]['sumOpenInterest']))/14
            data_vol_now = (float(result_get_open_interest[-1]['sumOpenInterestValue']) + float(
                result_get_open_interest[-2]['sumOpenInterestValue']) + float(
                result_get_open_interest[-3]['sumOpenInterestValue']) + float(
                result_get_open_interest[-4]['sumOpenInterestValue']) + float(
                result_get_open_interest[-5]['sumOpenInterestValue']) + float(result_get_open_interest[-6][
                                                                                  'sumOpenInterestValue'])+ float(result_get_open_interest[-7]['sumOpenInterestValue'])+ float(result_get_open_interest[-8]['sumOpenInterestValue'])+ float(result_get_open_interest[-9]['sumOpenInterestValue'])+ float(result_get_open_interest[-10]['sumOpenInterestValue'])+ float(result_get_open_interest[-11]['sumOpenInterestValue'])+ float(result_get_open_interest[-12]['sumOpenInterestValue'])) / 12  # (float(result_get_open_interest[-1]['sumOpenInterestValue']) + float(result_get_open_interest[-2]['sumOpenInterestValue']) + float(result_get_open_interest[-3]['sumOpenInterestValue']) + float(result_get_open_interest[-4]['sumOpenInterestValue'])+ float(result_get_open_interest[-5]['sumOpenInterestValue'])+ float(result_get_open_interest[-6]['sumOpenInterestValue'])+ float(result_get_open_interest[-7]['sumOpenInterestValue'])+ float(result_get_open_interest[-8]['sumOpenInterestValue'])+ float(result_get_open_interest[-9]['sumOpenInterestValue'])+ float(result_get_open_interest[-10]['sumOpenInterestValue'])+ float(result_get_open_interest[-11]['sumOpenInterestValue'])+ float(result_get_open_interest[-12]['sumOpenInterestValue'])+ float(result_get_open_interest[-13]['sumOpenInterestValue'])+ float(result_get_open_interest[-14]['sumOpenInterestValue']))/14

            pr_all = (data_back_sr / data_now - 1) * 100
            pr_all = round(pr_all, 3)

            pr_vol_all = (data_back_vol_sr / data_vol_now - 1) * 100
            pr_vol_all = round(pr_vol_all, 3)

            zzzz = f'📍Открытый интерес:👉 {pr_all}%'
            zzzz_vol = f'📍Общий открытый интерес:👉 {pr_vol_all}%'

            markup = types.InlineKeyboardMarkup()

            b1 = types.InlineKeyboardButton(text='TV',
                                            url=f"https://ru.tradingview.com/chart/{result_get_open_interest[0]['symbol']}.P")
            b2 = types.InlineKeyboardButton(text='CG',
                                            url=f"https://www.coinglass.com/tv/ru/Binance_{result_get_open_interest[0]['symbol']}")

            markup.add(b1, b2)

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
                                     f"🟩📈<code>{result_get_open_interest[0]['symbol']}</code> #{result_get_open_interest[0]['symbol']}\n\n{zzzz}\n{zzzz_vol}\n\n{result_volue}\n{result_trades}\n\n<i>Chg%24h=</i> <b><u>{priceChangePercent}%</u></b>\n За 4ч: {kol_vo_nam}",
                                     parse_mode='HTML', reply_markup=markup)
                else:
                    bot.send_message(chat_main_id,
                                     f"🟩📈<code>{result_get_open_interest[0]['symbol']}</code> #{result_get_open_interest[0]['symbol']}\n\n{zzzz}\n\n{zzzz_vol}\n\n<i>Chg%24h=</i> <b><u>{priceChangePercent}%</u></b>\n За 4ч: {kol_vo_nam}",
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
                                     f"🟥📉<code>{result_get_open_interest[0]['symbol']}</code> #{result_get_open_interest[0]['symbol']}\n\n{zzzz}\n{zzzz_vol}\n\n{result_volue}\n{result_trades}\n\n<i>Chg%24h=</i> <b><u>{priceChangePercent}%</u></b>\n За 4ч: {kol_vo_nam}",
                                     parse_mode='HTML', reply_markup=markup)
                else:
                    bot.send_message(chat_main_id,
                                     f"🟥📉<code>{result_get_open_interest[0]['symbol']}</code> #{result_get_open_interest[0]['symbol']}\n\n{zzzz}\n\n{zzzz_vol}\n\n<i>Chg%24h=</i> <b><u>{priceChangePercent}%</u></b>\n За 4ч: {kol_vo_nam}",
                                     parse_mode='HTML', reply_markup=markup)


                time.sleep(2)
        except Exception as e:
            #print('\nОшибка:\n', traceback.format_exc())
            #print(i)
            pass


    time.sleep(300)
    main(kol_vo)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, '/UPDATE\n'
                                      '/PARAMETERS')

@bot.message_handler(commands=['PARAMETERS'])
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


@bot.message_handler(commands=['UPDATE'])
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



if __name__ == '__main__':
    thread = threading.Thread(target=start_main)
    thread.start()
    bot.polling(none_stop=True, timeout=123)
