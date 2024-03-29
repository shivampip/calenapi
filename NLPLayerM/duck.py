from datetime import timedelta, datetime 
from dateutil.parser import parse 
from mylog import log
from duckling import DucklingWrapper
from pprint import pprint 

log.debug("DUCK")
dw= DucklingWrapper()

def make_std(dt):
    return parse(dt).strftime("%Y-%m-%dT%H:%M")


def get_now():
    return datetime.now()

def str_to_dt(text):
    return parse(text) 


def dt_to_date(dt):
    return dt.strftime("%d/%m/%Y")

def dt_to_time(dt):
    return dt.strftime("%H:%M")

def add_duration(dt, duration):
    return dt + timedelta(seconds= duration)

#Input- message
#Output- is_found, time
def get_time(data):
    out={}
    data= dw.parse_time(data)
    log.info("IN DUCK Raw data:")
    pprint(data)
    mdiff,obj= 2, None 
    for dd in data:
        diff= dd['end']- dd['start']
        if(diff>mdiff):
            mdiff= diff
            obj= dd 
    log.info("Choosen is:")
    pprint(obj)
    if(obj==None):
        return "{}"

    value= obj['value']
    in_value= value['value']
    if('grain' not in value):
        out['to']= make_std(in_value['to'])
        out['from']= make_std(in_value['from'])
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
            out['to']= out['to'].strftime("%Y-%m-%dT%H:%M")
            out['from']= make_std(out['from'])
            log.info("New From: {}".format(out['from']))
    log.info("OUT IS:")
    if('to' not in out):
        out['from']= make_std(out['from'])
    pprint(out) 
    return out 



#Input- message
#Output- is_found, duration
def get_duration(data):
    out= ""
    total= 0
    data= dw.parse_duration(data)
    for dd in data:
        out+= "Dimention: "+dd['dim']+"<br>"
        out+= "Text: "+dd['text']+"<br>"
        val= dd['value']
        tt= 0
        if(val['second'] is not None):
            tt+= timedelta(seconds= val['second']).total_seconds()
        elif(val['minute'] is not None):
            tt+= timedelta(minutes= val['minute']).total_seconds()
        elif(val['hour'] is not None):
            tt+= timedelta(hours= val['hour']).total_seconds()
        elif(val['day'] is not None):
            tt+= timedelta(days= val['day']).total_seconds()
        elif(val['month'] is not None):
            tt+= timedelta(months= val['month']).total_seconds()
        elif(val['year'] is not None):
            tt+= timedelta(years= val['year']).total_seconds()
        
        out+= "Duration in seconds: "+str(tt)+"<br>"
        total+= tt 
    out+= "<b>Total duration in seconds: "+str(total)+"</b><br>"
    return out, total 