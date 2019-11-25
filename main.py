import chatbot

bot = chatbot.Chatbot("data_perhutani")

bot.openBrowser()

while True:
    bot.cekAndSendMessage()