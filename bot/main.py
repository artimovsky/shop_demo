import requests


def getBotToken():
    return '568160026:AAGVvONpyMwnH8efDAYAgSqn6jOur7VQfzU'


def getUpdates(limit=100, offset=0):

    params = {
        'limit': limit,
        'offset': offset,
    }

    response = requests.get(
        'https://api.telegram.org/bot' + getBotToken() + '/getUpdates', params)

    arrayJson = response.json()

    #print('>>> Количество непрочитанных сообщений: ' + str(len(arrayJson['result'])))

    return arrayJson['result']


def getDataFromMessage(arrayMessage):

    if 'message' in arrayMessage:
        return {
            'updateId': arrayMessage['update_id'],
            'chatId': arrayMessage['message']['chat']['id'],
            'text': arrayMessage['message']['text'],
        }
    elif 'edited_message' in arrayMessage:
        return {
            'updateId': arrayMessage['update_id'],
            'chatId': arrayMessage['edited_message']['chat']['id'],
            'text': arrayMessage['edited_message']['text'],
        }


def sendMessage(chatId, text):

    params = {
        'chat_id': chatId,
        'text': text,
    }

    response = requests.get(
        'https://api.telegram.org/bot' + getBotToken() + '/sendMessage', params)


def messageHandler(arrayData):

    if arrayData['text'] == '/start':
        text = "Бот курса валют приветствует вас!\nЯ могу проинформировать вас о курсах криптовалют.\nСписок команд:\n - /btc - получить информацию о курсе биткоина\n - /eth - получить информацию о курсе эфириума"
        sendMessage(arrayData['chatId'], text)
    elif arrayData['text'] == '/btc':
        rate = getExchangeRate('btc', 'rur')
        text = '1 биткоин = ' + rate + ' руб.'
        sendMessage(arrayData['chatId'], text)
    elif arrayData['text'] == '/eth':
        rate = getExchangeRate('eth', 'rur')
        text = '1 эфириум = ' + rate + ' руб.'
        sendMessage(arrayData['chatId'], text)


def getExchangeRate(curFrom, curTo):

    #print('>>> Отправка запроса курса')

    response = requests.get(
        'https://api.cryptonator.com/api/ticker/' + curFrom + '-' + curTo)

    #print('>>> Получен ответ: ' + response.text)

    arrayJson = response.json()

    return arrayJson['ticker']['price']



# получить непрочитанные сообщения
arrayMessages = getUpdates(10, 0)

# в offset будет храниться message_id с максимальным значением
offset = 0

for arrayMessage in arrayMessages:

    arrayData = getDataFromMessage(arrayMessage)
    #print('>>> Обработанный массив: ')
    #print(arrayData)

    if offset < arrayData['updateId']:
        offset = arrayData['updateId']

    messageHandler(arrayData)


offset = offset + 1

# пометить выбранные выше сообщения прочитанными
getUpdates(100, offset)
