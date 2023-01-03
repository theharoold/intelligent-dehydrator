import hashlib
import RPi.GPIO as GPIO
import dht
import machine
import telepot
from telepot.loop import MessageLoop
import time

# Bot link:
# t.me/DehydratorControllerBot

# Broj pina za kontrolu dehidratora
DEHYDRATOR_PIN = 17

# Broj pina za DHT22 senzor
TEMP_SENSOR_PIN = 16

# Postaviti temperaturu i vreme za dehidraciju
TARGET_TEMPERATURE = 60  # stepeni Farenhajta
TARGET_HUMIDITY = 30  # procenata
DEHYDRATION_TIME = 10 * 60  # u sekundama

# Broj citanja za uzimanje prosecne temperature
NUM_READINGS = 10

# Postaviti GPIO pinove za Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(DEHYDRATOR_PIN, GPIO.OUT)

# Dostupne komande
availableCommands = ['/start', '/stop']

authorizedUsers = []

# Funkcija za čitanje trenutne temperature i vlaznosti vazduha iz dehidratorovog senzora
def read_temperature():
    # Inicijalizacija senzora
    sensor = dht.DHT22(machine.Pin(TEMP_SENSOR_PIN))

    # Citanje temperature i vlaznosti vazduha
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()

    return temperature, humidity

# Funkcija za uključivanje i isključivanje dehidratora
def set_dehydrator(state):
    if state:
        # Uključiti dehidrator
        GPIO.output(DEHYDRATOR_PIN, GPIO.HIGH)
    else:
        # Isključiti dehidrator
        GPIO.output(DEHYDRATOR_PIN, GPIO.LOW)

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

# Funkcija za rukovanje porukama sa Telegrama
def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if not authenticateUser(chat_id):
      return

    if content_type == "text":
       # Rukovanje tekstualnim porukama
      text = msg["text"]

      if validate(text, chat_id):
        if text == "/start":
            startDehydration(chat_id)
        elif text == "/stop":
            stopDehydration(chat_id)

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


# Citanje tokena iz datoteke
f = open("token.txt", "r")
BOT_TOKEN = f.readline().strip()
f.close()

def startDehydration(chat_id):
    # Počni s dehidracijom
    bot.sendMessage(chat_id, "Starting dehydration process...")
    start_time = time.time()
    while time.time() - start_time < DEHYDRATION_TIME:
        # Pročitaj trenutnu temperaturu
        temperature, humidity = read_temperature()

        # U zavisnosti od trenutne temperature, dehidrator se
        # ili uključuje ili isključuje
        if temperature > TARGET_TEMPERATURE or humidity > TARGET_HUMIDITY:
            set_dehydrator(True)
        else:
            set_dehydrator(False)

        # Sačekaj nekoliko sekundi, pa proveri temperaturu opet
        time.sleep(5)

    # Isključi dehidrator kada istekne vreme za dehidraciju
    set_dehydrator(False)
    bot.sendMessage(chat_id, "Dehydration process complete!")


def stopDehydration(chat_id):
    # Prekini sa dehidracijom
    bot.sendMessage(chat_id, "Stopping dehydration process...")
    set_dehydrator(False)
    bot.sendMessage(chat_id, "Dehydration process stopped.")


# Kreiraj instancu telegram bota
bot = telepot.Bot(BOT_TOKEN)

# Počni s osluškivanjem poruka
MessageLoop(bot, handle_message).run_as_thread()

# Drži program uključenim dok korisnik ne pošalje signal za prekid
while 1:
    time.sleep(10)

# Izvrši proces čišćenja Raspberry Pi-jevih GPIO pinova kada je program prekinut
GPIO.cleanup()
