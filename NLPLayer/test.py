import os 
from threading import Thread

def launch(name):
    os.system("start /wait cmd /c python {}".format(name))


t1= Thread(target= launch, args=("as.py",))
t2= Thread(target= launch, args=("bot.py",))

t1.start()
t2.start()

print("Both Launched")