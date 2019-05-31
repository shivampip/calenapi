import os 
from threading import Thread

def launch(name):
    os.system("start /wait cmd /c python {}".format(name))


t0= Thread(target= launch, args=("manage.py runserver",))
t1= Thread(target= launch, args=("NLPLayer/as.py",))
t2= Thread(target= launch, args=("NLPLayer/bot.py",))

t0.start()
t1.start()
t2.start()

print("Both Launched")