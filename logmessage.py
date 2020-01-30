from datetime import datetime
import dawet
import chatbot
import sys

chat = chatbot.Chatbot()

getDateTimeNow = datetime.now()

data = []

data.append(getDateTimeNow.strftime("%d/%m/%Y %H:%M:%S"))
data.append(sys.argv[1])
data.append(sys.argv[2])

wetwet = dawet.Dawet("logmessage")

wetwet.setRowData(data)