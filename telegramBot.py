"""
@name TelegramBot
@file telegramBot.py
@author Martin Kubicka
@date 28.1.2022
"""

import requests
from bs4 import BeautifulSoup
import time

"""
@brief sending new message to own created group

@param token - telegram bot token
@param message - message which will be sent to own group
"""
def sendMessage(token, message):
    myGroup = "-1001647722965"
    params = [
        ("text", message)
    ]
    requests.post(("https://api.telegram.org/bot{}/sendMessage?chat_id={}").format(token, myGroup), data=params)

"""
@brief getting last messages in groups to know where bot ends

@param groupLinks - all links which needs to be scraped
"""
def getLastMessages(groupLinks):
    lastMessage = []
    for i in groupLinks:
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'html.parser')
        lm = soup.find_all("div", class_="tgme_widget_message_wrap js-widget_message_wrap")[-1].find("div").find("div", class_="tgme_widget_message_bubble").find("div", class_="tgme_widget_message_text js-message_text")
        if lm == None:
            lastMessage.append(None)
        else:
            lastMessage.append(lm.getText())
    return lastMessage

"""
@brief get new messages and right then sending to own group

@param grouLinks - all links which are checked
@param lastMessage - message where bot ended
@param token - telegram bot token
"""
def getMessages(groupLinks, lastMessage, token):
    sendMessagesList = []
    for i, j in zip(groupLinks, range(len(groupLinks))):
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'html.parser')
        count = 0
        for k in soup.find_all("div", class_="tgme_widget_message_wrap js-widget_message_wrap"):
            if k.find("div").find("div", class_="tgme_widget_message_bubble").find("div", class_="tgme_widget_message_text js-message_text") == None:
                continue
            if k.find("div").find("div", class_="tgme_widget_message_bubble").find("div", class_="tgme_widget_message_text js-message_text").getText() == lastMessage[j]:
                count += 1
            elif count != 0:
                msg = k.find("div").find("div", class_="tgme_widget_message_bubble").find("div", class_="tgme_widget_message_text js-message_text").getText()
                if "#" in msg:
                    sendMessagesList.append(msg)
                lastMessage[j] = msg

    for message in sendMessagesList:
        sendMessage(token, message)

    return lastMessage

"""
@brief In main token is set. 
There are all groupLinks which Bot is checking.
First time calling function getLastMessages for bot to know where to start.
Infinite while loop to get messages and then move on..
"""
def main():
    print("Successfully started!")
    token = "5245161899:AAGw7pS2JJ3BsVvmyp8Fu5viWGhh3lOz1BI"
    groupLinks = {"https://t.me/s/CryptoClasssssics", "https://t.me/s/AlphaTradeZone", "https://t.me/s/QualitySignalsChannel",
                  "https://t.me/s/cryptolabhub", "https://t.me/s/infocryptosignals", "https://t.me/s/tradingv2channel",
                  "https://t.me/s/FieryTradingChannel", "https://t.me/s/miladtrades", "https://t.me/s/AllthingsTA",
                  "https://t.me/s/TheCryptoWolf", "https://t.me/s/boozpremium_signals", "https://t.me/s/saudicrypto",
                  "https://t.me/s/highrollertrader", "https://t.me/s/BTCSri", "https://t.me/s/freetradingtip", "https://t.me/s/CAMPSIGNALS",
                  "https://t.me/s/Crypto2AF_Signals", "https://t.me/s/CryptoFuente", "https://t.me/s/tripleHtradesFree",
                  "https://t.me/s/elneit23journal", "https://t.me/s/MrPainEthMarginSignals", "https://t.me/s/SignalSemperCrypto",
                  "https://t.me/s/BraveNewCryptosResearch", "https://t.me/s/Thecryptolions", "https://t.me/s/cryptosignalsMaverick",
                  "https://t.me/s/sslevclub", "https://t.me/s/coinkingsfree", "https://t.me/s/robinhoodlabtrading",
                  "https://t.me/s/freemoonshots", "https://t.me/s/kh2fmk9snZ", "https://t.me/s/BinancesignalsAD",
                  "https://t.me/s/RGtrades", "https://t.me/s/CryptonaticA", "https://t.me/s/HiveCryptoPublic",
                  "https://t.me/s/GTC_Good_Trading_Calls", "https://t.me/s/bmeex", "https://t.me/s/bromadicclub",
                  "https://telegram.me/s/Cryptomoneymakerss", "https://t.me/s/chartscience", "https://t.me/s/Heisenberg_Signals",
                  "https://t.me/s/traderhyper", "https://t.me/s/GoldenTrades", "https://t.me/s/MySignalsapp"}

    lastMessage = getLastMessages(groupLinks)
    while True:
        lastMessage = getMessages(groupLinks, lastMessage, token)
        time.sleep(10)

if __name__ == "__main__":
    main()

# Problems in the future:
# Not scraping pictures.
# Not getting respond messages.
# Not getting special characters like \n..
