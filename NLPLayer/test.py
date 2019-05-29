from datetime import timedelta, datetime 
from mylog import log
from duckling import DucklingWrapper
from dateutil.parser import parse
from pprint import pprint


dw= DucklingWrapper()

while(True):
    data= str(input("Enter here:- "))   
    out={}
    data= dw.parse_time(data)
    log.info("IN DUCK Raw data:")
    pprint(data)
    mdiff,obj= 0, None 
    for dd in data:
        diff= dd['end']- dd['start']
        if(diff>mdiff):
            mdiff= diff
            obj= dd 
    log.info("Choosen is:")
    pprint(obj)

    value= obj['value']
    in_value= value['value']
    if('grain' not in value):
        out['to']= in_value['to']
        out['from']= in_value['from']
    else:
        grain= value['grain']
        out['from']= in_value 
        if(grain=='day'):
            log.info('Before converting: {}'.format(in_value))
            #out_from= datetime.strptime(in_value, "%Y-%m-%dT%H:%M")
            #out_from= datetime.strptime(in_value, "YYYY-MM-DDTHH:MM:SS.mmmmmm")
            # yyyy'-'MM'-'dd'T'HH':'mm':'ss'.'fffffffzz
            out_from= parse(in_value)
            log.info('After converting: {}'.format(out_from))
            #log.info('Type: {}'.format(type(out_from)))
            out['to']= out_from + timedelta(days=1) 
            ooo= out['to'].strftime("%Y-%m-%dT%H:%M")
            log.info('Final to: {}'.format(ooo))
    log.info("OUT IS:")
    pprint(out)