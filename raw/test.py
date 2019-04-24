from datetime import datetime

dt= datetime.now()

print("## Start DT: {}".format(dt))
ds= datetime.timestamp(dt)
print("## Conve DT: {}".format(str(datetime.fromtimestamp(ds))))