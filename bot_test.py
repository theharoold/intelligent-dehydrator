import telepot
from telepot.loop import MessageLoop
import time

# Postaviti token za telegram bota
BOT_TOKEN = "5959331635:AAHLhtaCNZmo_FllKH2w8Jp4McqZ6GE0Z0M"

def handle_message(msg):
  content_type, chat_type, chat_id = telepot.glance(msg)
  if content_type == "text":
    # Rukovanje tekstualnim porukama
    text = msg["text"]
    print(text)

    bot.sendMessage(chat_id, '''Your message ${} has been received!'''.format(text))

# Kreiraj instancu telegram bota
bot = telepot.Bot(BOT_TOKEN)

# Počni s osluškivanjem poruka
MessageLoop(bot, handle_message).run_as_thread()

# Drži program uključenim dok korisnik ne pošalje signal za prekid
while 1:
  time.sleep(10)