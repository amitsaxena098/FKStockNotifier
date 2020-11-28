import urllib.request as urllib2
import re
import time
import winsound
from configparser import RawConfigParser
from threading import *
import time
import telegram

CONFIG = RawConfigParser()
CONFIG.read('config.ini')
timer = int(CONFIG.get('TIMER','CHECK_AFTER'))
total_links = int(CONFIG.get('URL', 'LINKS'))
my_token = '' #Your telegram token here
my_chat_id =  #chat id here
def send(msg, chat_id, token=my_token):
		"""
		Send a mensage to a telegram user specified on chatId
		chat_id must be a number!
		"""
		bot = telegram.Bot(token=token)
		bot.sendMessage(chat_id=chat_id, text=msg)


class check_stock(Thread):
	url = ""
	
	
	def set_url(self, url):
		self.url = url
		
	def run(self):
		while True:
			ff = str(urllib2.urlopen(self.url).read())
			product = re.findall('This item is currently out of stock', ff)
			if len(product) == 0:
				t = time.localtime()
				current_time = time.strftime("%H:%M:%S", t)
				split_str = (self.url).split("/")
				s = " "
				print(" ".join(split_str[3].split("-")) + " in stock @" + str(current_time))
				send(" ".join(split_str[3].split("-")) + " in stock @" + str(current_time), my_chat_id, my_token)
				time.sleep(timer)




threads = []
for i in range(1, total_links+1):
	flipkart_url = CONFIG.get('URL','LINK'+ str(i))
	thread1 = check_stock()
	thread1.set_url(flipkart_url)
	thread1.start()
	threads.append(thread1)

