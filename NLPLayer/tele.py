from rasa_core.interpreter import RasaNLUInterpreter
#from rasa_telegram_connector import TelegramInput
from rasa_core.utils import EndpointConfig
from rasa_core.agent import Agent
from rasa_core.channels.telegram import TelegramInput

import logging
logging.basicConfig(level=logging.DEBUG)

nlu_interpreter = RasaNLUInterpreter("models/current/nlu")
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")


agent = Agent.load('models/dialogue', interpreter = nlu_interpreter, action_endpoint = action_endpoint)
#agent = Agent.load('models/dialogue', interpreter = nlu_interpreter)


input_channel = TelegramInput(
        # you get this when setting up a bot
        access_token="755208720:AAGhQ6UjO023Dphm7eZ2Lxp-bSHELHgAaVM",
        # this is your bots username
        verify="HiRashiBot",
        # the url your bot should listen for messages
        webhook_url="9b394b88.ngrok.io/webhooks/telegram/webhook")


#RUN NGRO BY: ngrok http 5004
agent.handle_channels([input_channel], 5004, serve_forever=True)

# First Run Action Server by: python as.py
# Run Ngrok server by goint to ngrok upzipped dir and click on ngrok
# Type: ngrok http 5004
# Copy Ngrok url and paste it in webhook_url
# Now run tele.py
# ENJOY