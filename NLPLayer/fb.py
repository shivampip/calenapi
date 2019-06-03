import os

#print("Starting Facebook Chat.....")
#os.system("python -m rasa_core.run -d models/dialogue -u models/current/nlu --port 5002 --credentials fb_credentials.yml")
#os.system("python -m rasa_core.run -d models/dialogue -u models/current/nlu --endpoints endpoints.yml")

from rasa_core.interpreter import RasaNLUInterpreter
#from rasa_telegram_connector import TelegramInput
from rasa_core.utils import EndpointConfig
from rasa_core.agent import Agent
from rasa_core.channels.facebook import FacebookInput

import logging
logging.basicConfig(level=logging.DEBUG)

nlu_interpreter = RasaNLUInterpreter("models/current/nlu")
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")


agent = Agent.load('models/dialogue', interpreter = nlu_interpreter, action_endpoint = action_endpoint)
#agent = Agent.load('models/dialogue', interpreter = nlu_interpreter)


input_channel = FacebookInput(
   fb_verify="veerybot",  # you need tell facebook this token, to confirm your URL
   fb_secret="94f428b6b33eb90375fa5e24793cbe0c",  # your app secret
   fb_access_token="EAAJF3RoBgeoBAHRbgeHuhHLSqJZBusGRfGo4eNAoFaAf4sVfpQ9vWXXDg9cbxHPlwHrm4sjwNlutRR8bYWbo7uWPDNmcGSFIi3rYLjrwGtLXjSP8NT8ZC6l7MnNNEZBrpcvCmTJ7vj6IfKC4aOYAZBwUbDdjsEcJ22BiijmCWwZDZD"   # token for the page you subscribed to
)


#RUN NGRO BY: ngrok http 5004
agent.handle_channels([input_channel], 5004, serve_forever=True)




# First Run Action Server by: python as.py
# Run fb.py
# Run Ngrok server by goint to ngrok upzipped dir and click on ngrok
# Type: ngrok http 5004 ( ./ngrok http 5004 )
# Copy Ngrok url and modify like this
# https://e7d3d4e6.ngrok.io/webhooks/facebook/webhook

# Go to https://developers.facebook.com/apps/639765879816682/messenger/settings/
# Either setup webhook or niche
# Paste it in Messanger settign OR Webhook >> Edit Subscription >> callback url
# Paste Veriy= veerybot
# Select events: messages, messaging_postbacks, message_deliveries
# ENJOY
