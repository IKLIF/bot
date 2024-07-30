import telebot
from telebot import types
import traceback
import time
from binance.um_futures import UMFutures
from pybit.unified_trading import HTTP
from binance.client import Client
import requests
import threading
import time
import schedule
import telebot
from telebot import types
import datetime

from GOGO import G1,G2,G3,moex


import sqlite3

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS users ('
               'user_id INTEGER PRIMARY KEY'
               ')')

conn.close()

API_TOKEN = '7267240488:AAHx03D--_SyHxRBlCTnJnIZh9CEcZy_pZ8'
bot = telebot.TeleBot(API_TOKEN)

black = ['SLPUSDT']#['DGBUSDT','DASHUSDT','ZECUSDT']
gl_pr = 15



@bot.message_handler(commands=['start', 'help'] )
def start(message):
    back = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'GO', reply_markup=back)
    markup = types.InlineKeyboardMarkup(row_width=1)

    b1 = types.InlineKeyboardButton(text='Binance: FUTURES-Bybit: FUTURES', callback_data='Bybit: FUTURES Binance: FUTURES')
    b2 = types.InlineKeyboardButton(text='Binance: SPOT-Bybit: FUTURES', callback_data='Bybit: FUTURES Binance: SPOT')
    b3 = types.InlineKeyboardButton(text='Binance: FUTURES-Bybit: SPOT', callback_data='Bybit: SPOT Binance: FUTURES')
    b4 = types.InlineKeyboardButton(text='MOEX', callback_data='Bybit: SPOT Binance: SPOT')

    markup.add(b1,b2,b3,b4)

    bot.send_message(message.chat.id, f'Выберите:', reply_markup=markup)

def G0():
    x = 0
    message = 583048425
    GO_1(message,bot,gl_pr,x)
def GO_1(message,bot,gl_pr,x):
    now = datetime.datetime.now()
    print(f'опрос № {x}: {now.strftime("%d-%m-%Y %H:%M:%S")}')
    x += 1
    pr = 1.3

    conn = sqlite3.connect('users.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM users")
    myresult = cursor.fetchall()

    conn.close()

    result_G1 = None
    result_G2 = None
    result_G3 = None
    result_moex = None

    try:
        result_G1 = G1(message,bot,gl_pr,black,pr)
    except Exception as e:
        print('Ошибка:\n', traceback.format_exc())
    try:
        result_G2 = G2(message,bot,gl_pr,black,pr)
    except Exception as e:
        print('Ошибка:\n', traceback.format_exc())
    try:
        pass
        #result_moex = moex()
    except Exception as e:
        print('Ошибка:\n', traceback.format_exc())
    #G4(message,bot,gl_pr,black,pr)

    if result_G1 != None:
        for i in myresult:
            bot.send_message(i[0], result_G1, parse_mode='HTML')
    if result_G2 != None:
        for i in myresult:
            bot.send_message(i[0], result_G2, parse_mode='HTML')
    if result_G3 != None:
        for i in myresult:
            bot.send_message(i[0], result_G3, parse_mode='HTML')
    if result_moex != None:
        for i in myresult:
            bot.send_message(i[0], result_moex, parse_mode='HTML')

    time.sleep(60)
    GO_1(message,bot,gl_pr,x)

@bot.message_handler(commands=['GO'] )
def GOY(message):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    cursor = conn.cursor()
    user_id = message.from_user.id
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    if cursor.fetchone() is None:
        cursor.execute(
            'INSERT INTO users (user_id) VALUES (?)',
            (user_id,))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, 'Вы подписались на рассылку.')
    else:
        bot.send_message(message.chat.id, 'Вы уже подписаны!')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton("Главное меню")
        markup.add(b1)
        if call.data == 'Bybit: FUTURES Binance: FUTURES':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            bot.send_message(call.message.chat.id, "Введите %:", reply_markup=markup)
            bot.register_next_step_handler(call.message, By_F_Bi_F)
        elif call.data == 'Bybit: FUTURES Binance: SPOT':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            bot.send_message(call.message.chat.id, "Введите %:", reply_markup=markup)
            bot.register_next_step_handler(call.message, By_F_Bi_S)
        elif call.data == 'Bybit: SPOT Binance: FUTURES':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            bot.send_message(call.message.chat.id, "Введите %:", reply_markup=markup)
            bot.register_next_step_handler(call.message, By_S_Bi_F)
        elif call.data == 'Bybit: SPOT Binance: SPOT':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            bot.send_message(call.message.chat.id, "Введите %:", reply_markup=markup)
            bot.register_next_step_handler(call.message, By_S_Bi_S)





def By_F_Bi_F(message):
    if message.text != 'Главное меню':
        try:
            pr = float(message.text)

            bot.send_message(message.chat.id, '💬')

            data_binance = []
            data_bybit = []

            url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
            response = requests.get(url)
            data_many_f = response.json()

            for coin in data_many_f:
                symbol = coin['symbol']
                price = coin['lastPrice']
                timestamp = coin['closeTime']
                print(f"{symbol}: {price}, Last Update: {timestamp}")

            url = "https://fapi.binance.com/fapi/v1/time"
            response = requests.get(url)
            data_t_f = response.json()

            server_time_f = data_t_f['serverTime']

            for i in data_many_f:
                if server_time_f - 86400000 < i['closeTime'] and float(i['lastPrice']) > 0:
                    data_binance.append({'symbol':i['symbol'], 'price':i['lastPrice']})

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
                    data_bybit.append({'symbol':i['symbol'], 'price':i['lastPrice']})

            txt = 'RESULT:\n'

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
                            txt = txt + f"<code>{bin['symbol']}</code>:  {z}% \n⚡️<u>Binance:</u> <b>{bin['price']}</b> FUTURES \n⚡️<u>ByBit:</u> <b>{by['price']}</b> FUTURES\n\n"
            if txt == 'RESULT:\n':
                txt = '🤷‍♂️'
            bot.send_message(message.chat.id, txt, parse_mode='HTML')

            bot.send_message(message.chat.id, 'Введите %:')
            bot.register_next_step_handler(message, By_F_Bi_F)
        except:
            bot.send_message(message.chat.id, 'ERROR')
            bot.send_message(message.chat.id, 'Введите %:')
            bot.register_next_step_handler(message, By_F_Bi_F)
    else:
        start(message)


def By_F_Bi_S(message):
    if message.text != 'Главное меню':
        try:
            pr = float(message.text)

            bot.send_message(message.chat.id, '💬')

            data_binance = []
            data_bybit = []

            url = "https://api.binance.com/api/v3/ticker/24hr"
            response = requests.get(url)
            data_many_s = response.json()

            for coin in data_many_s:
                symbol = coin['symbol']
                price = coin['lastPrice']
                timestamp = coin['closeTime']
                print(f"{symbol}: {price}, Last Update: {timestamp}")

            url = "https://api.binance.com/api/v3/time"
            response = requests.get(url)
            data_t_f = response.json()

            server_time_f = data_t_f['serverTime']

            for i in data_many_s:
                if server_time_f - 86400000 < i['closeTime'] and float(i['lastPrice']) > 0:
                    data_binance.append({'symbol':i['symbol'], 'price':i['lastPrice']})

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
                    data_bybit.append({'symbol':i['symbol'], 'price':i['lastPrice']})

            txt = 'RESULT:\n'

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
                            txt = txt + f"<code>{bin['symbol']}</code>:  {z}% \n⚡️<u>Binance:</u> <b>{bin['price']}</b> SPOT \n⚡️<u>ByBit:</u> <b>{by['price']}</b> FUTURES\n\n"
            if txt == 'RESULT:\n':
                txt = '🤷‍♂️'
            bot.send_message(message.chat.id, txt, parse_mode='HTML')

            bot.send_message(message.chat.id, 'Введите %:')
            bot.register_next_step_handler(message, By_F_Bi_S)
        except:
            bot.send_message(message.chat.id, 'ERROR')
            bot.send_message(message.chat.id, 'Введите %:')
            bot.register_next_step_handler(message, By_F_Bi_S)
    else:
        start(message)


def By_S_Bi_F(message):
    if message.text != 'Главное меню':
        try:
            pr = float(message.text)

            bot.send_message(message.chat.id, '💬')

            data_binance = []
            data_bybit = []

            url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
            response = requests.get(url)
            data_many_f = response.json()

            for coin in data_many_f:
                symbol = coin['symbol']
                price = coin['lastPrice']
                timestamp = coin['closeTime']
                print(f"{symbol}: {price}, Last Update: {timestamp}")

            url = "https://fapi.binance.com/fapi/v1/time"
            response = requests.get(url)
            data_t_f = response.json()

            server_time_f = data_t_f['serverTime']

            for i in data_many_f:
                if server_time_f - 86400000 < i['closeTime'] and float(i['lastPrice']) > 0:
                    data_binance.append({'symbol':i['symbol'], 'price':i['lastPrice']})

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
                    data_bybit.append({'symbol':i['symbol'], 'price':i['lastPrice']})

            txt = 'RESULT:\n'

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
                            txt = txt + f"<code>{bin['symbol']}</code>:  {z}% \n⚡️<u>Binance:</u> <b>{bin['price']}</b> FUTURES \n⚡️<u>ByBit:</u> <b>{by['price']}</b> SPOT\n\n"
            if txt == 'RESULT:\n':
                txt = '🤷‍♂️'
            bot.send_message(message.chat.id, txt, parse_mode='HTML')

            bot.send_message(message.chat.id, 'Введите %:')
            bot.register_next_step_handler(message, By_S_Bi_F)
        except:
            bot.send_message(message.chat.id, 'ERROR')
            bot.send_message(message.chat.id, 'Введите %:')
            bot.register_next_step_handler(message, By_S_Bi_F)
    else:
        start(message)
def By_S_Bi_S(message):
    if message.text != 'Главное меню':
        try:
            proc = float(message.text)

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

            txt = 'RESULT:\n\n'

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

                        if x >= proc and x <= 20:
                            if i['name'] in bl:
                                pass
                            else:
                                txt = txt + (f"✅ {x}%\n"
                                             f"📍 {i['ticker']} : {i['name']}👉{i['price']}\n"
                                             f"📍 {P['ticker']} : {P['name']}👉{P['price']}\n\n")
            if txt == 'RESULT:\n\n':
                txt = '🤷‍♂️'
            bot.send_message(message.chat.id, txt, parse_mode='HTML')

            bot.send_message(message.chat.id, 'Введите %:')
            bot.register_next_step_handler(message, By_S_Bi_S)
        except:
            bot.send_message(message.chat.id, 'ERROR')
            bot.send_message(message.chat.id, 'Введите %:')
            bot.register_next_step_handler(message, By_S_Bi_S)
    else:
        start(message)




if __name__ == '__main__':
    thread = threading.Thread(target=G0)
    thread.start()
    bot.polling(none_stop=True, timeout=123)

