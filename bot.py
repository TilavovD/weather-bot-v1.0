import requests
from datetime import datetime
import pytz

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import Filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TZ = pytz.timezone("Asia/Tashkent")


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def echo(update: Update, context) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def today(update: Update, context) -> None:
    response = requests.get(
        "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Yangiyer?unitGroup"
        "=metric&key=74EU933EXL9R9L477YD9QUHHX&contentType=json")
    data = response.json()
    curr = data["currentConditions"]

    sunrise = curr["sunrise"]
    sunset = curr["sunset"]
    address = data["address"]
    desc = data["description"]

    today = data["days"][0]

    date = today["datetime"]
    tempmax = today["tempmax"]
    tempmin = today["tempmin"]
    humidity = today["humidity"]
    wind_speed = today["windspeed"]

    today_text = f"""Today: {date}
    
    Address: {address}
    
    Max temp: {tempmax}
    Min temp: {tempmin}
    
    Description: {desc}
    
    Humidity: {humidity}
    Wind speed: {wind_speed}

    Sunrise: {sunrise}
    Sunset: {sunset}
    """
    update.message.reply_text(today_text)


def now(update: Update, context):
    response = requests.get(
        "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Yangiyer?unitGroup"
        "=metric&key=74EU933EXL9R9L477YD9QUHHX&contentType=json")
    data = response.json()
    curr = data["currentConditions"]

    time = curr["datetime"]
    curr_temp = curr["temp"]
    curr_feels_like = curr["feelslike"]
    curr_conditions = curr["conditions"]

    current_text = f"""Time as for: {time}
    
Time: {datetime.now(TZ).strftime("%H:%M:%S")}

Temperature: {curr_temp}
Feels like: {curr_feels_like}
Conditions: {curr_conditions}
"""
    update.message.reply_text(current_text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    updater = Updater("5421142600:AAEGGKAw8EjlT3tSR5as28W5943Nold4Pzc")
    application = updater.dispatcher

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("now", now))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Run the bot until the user presses Ctrl-C
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
