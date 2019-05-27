import os
import json

class Bot:
    def trainNlu(self):
        #os.system("python -m rasa_nlu.train -c mrasa/nlu_config.yml --data mrasa/data/nlu.md -o mrasa/models --fixed_model_name nlu --project current --verbose")
        os.system("python -m rasa_nlu.train -c nlu_config.yml --data data/nlu.md -o models --fixed_model_name nlu --project current --verbose")
        print("\nNLU TRAINED\n")

    def trainCore(self):
        #os.system("python -m rasa_core.train -d mrasa/data/domain.yml -s mrasa/data/stories.md -o mrasa/models/dialogue")
        os.system("python -m rasa_core.train -d data/domain.yml -s data/stories.md -o models/dialogue")
        print("\nCORE TRAINED")

    def runCore(self):
        #os.system("python -m rasa_core.run -d mrasa/models/dialogue")
        os.system("python -m rasa_core.run -d models/dialogue")

    def runActionServer(self):
        #os.system("python -m rasa_core_sdk.endpoint --actions mrasa.actions")
        os.system("python -m rasa_core_sdk.endpoint --actions actions")

    def runBoth(self):
        #os.system("python -m rasa_core.run -d mrasa/models/dialogue -u mrasa/models/current/nlu --endpoints mrasa/data/endpoints.yml")
        os.system("python -m rasa_core.run -d models/dialogue -u models/current/nlu --endpoints endpoints.yml")

    def runAll(self):
        #self.runActionServer()
        self.trainNlu()
        self.trainCore()
        self.runBoth()



from rasa_nlu.model import Metadata, Interpreter
from rasa_nlu.config import RasaNLUModelConfig
#from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter

class MyBot:
    def initNlu(self):
        #self.interpreter= Interpreter.load("hinlp/models/current/nlu")
        self.interpreter= Interpreter.load("models/current/nlu")

    def initIn(self):
        #self.interpreter= Interpreter.load("hinlp/models/current/nlu")
        self.interpreter= Interpreter.load("models/current/nlu")
        #self.agent = Agent.load('models/dialogue')

    def initAll(self):
        #self.interpreter= RasaNLUInterpreter("hinlp/models/current/nlu")
        self.interpreter= RasaNLUInterpreter("models/current/nlu")
        #self.agent= Agent.load("models/dialogue", interpreter= self.interpreter)

    def runNlu(self, msg):
        return self.interpreter.parse(msg)

    def runCore(self, msg):
        pass
        #return self.agent.handle_message(msg)

    def runBoth(self, msg):
        pass
        #return self.agent.handle_message(msg)


bot= Bot()
bot.trainNlu()

'''
bot.trainCore()
bot.runBoth()
exit()

'''
mb= MyBot()
mb.initNlu()
#mb.initIn()
#mb.initAll()
#util.clear_screen()
while(True):
    msg= input("You:- ")
    out= mb.runNlu(msg)
    out= json.dumps(out, indent=4)
    print("\n\n\n\nBot:- ",out)

        