import telepot
from telepot.loop import MessageLoop
import time
import hashlib

# Postaviti token za telegram bota
BOT_TOKEN = "5959331635:AAHLhtaCNZmo_FllKH2w8Jp4McqZ6GE0Z0M"  # api access token

availableCommands = ['/start', '/stop']

isFirstUsage = True

authorizedUsers = []

def getAuthorizedUsers():
    file = open("authorized_users.txt", "r")
    contents = file.read()
    authorizedUsers = contents.split("\n")
    file.close()
    return authorizedUsers

authorizedUsers = getAuthorizedUsers()

def authenticateUser(chat_id):
  global authorizedUsers

  currentChat = bot.getChat(chat_id)
  username = str(currentChat['username'])

  usernameHash = hashlib.sha256(username.encode()).hexdigest()

  if usernameHash in authorizedUsers:
    return True
  else:
    bot.sendMessage(
            chat_id,
            f'*Error*: You are not authorized',
            parse_mode='MarkdownV2')
    return False


def validate(input, chat_id):
    if not input in availableCommands:
        bot.sendMessage(
            chat_id,
            f'*Error*: Unknown command "{input}"\nSupported commands:\n\t• /start\n\t• /stop',
            parse_mode='MarkdownV2')
        return False
    else:
        bot.sendMessage(
            chat_id,
            f'*Info*: Command "{input}" received',
            parse_mode='MarkdownV2')
        return True


def handle_message(msg):
 
    content_type, chat_type, chat_id = telepot.glance(msg)

    if not authenticateUser(chat_id):
      return

    if content_type == "text":
        # Test
      text = msg["text"]

      if validate(text, chat_id):
        if text == "/start":
            print("Starting...")
        elif text == "/stop":
            print("Stopping...")


# Kreiraj instancu telegram bota
bot = telepot.Bot(BOT_TOKEN)

# Počni s osluškivanjem poruka
MessageLoop(bot, handle_message).run_as_thread()

# Drži program uključenim dok korisnik ne pošalje signal za prekid
while 1:
    time.sleep(10)
