from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import generics

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse

from .models import Event, PendingEvent, Invite, BusySlot, AASlot, Notification, ShareableLink
from .serializers import EventSerializer, UserSerializer, PendingEventSerializer, InviteSerializer, BusySlotSerializer, AASlotSerializer, NotificationSerializer, ShareableLinkSerializer

from dateutil.parser import parse
from datetime import timedelta

from .hiutil import username_to_id
import json 

from .mylog import log 


############TODO########################################

# When converting PendingEvent to Event,
# Timezone information is lost.
# in PendingEvent 07:00
# in Event, it becomes 01:30






########################################################




class CreateAASlots(APIView):

    def check(self ,author, week_day, start_time, end_time):
        start_time+= timedelta(seconds= 1)
        busy_slots= BusySlot.objects.filter(author= author, week_day= week_day, start_time__range= (start_time, end_time))
        bsl= len(busy_slots)
        busy_slots= BusySlot.objects.filter(author= author, week_day= week_day, end_time__range= (start_time, end_time))
        bsl+= len(busy_slots)
        return bsl==0
    
    def post(self, request):
        author= request.user.id 
        title= request.data.get("title")
        week_days= request.data.get("week_day")
        start_time= request.data.get("start_time")
        end_time= request.data.get("end_time")
        
        start_tm= datetime.strptime(start_time,"%H:%M")
        end_tm= datetime.strptime(end_time,"%H:%M")

        week_days= [int(x) for x in week_days.split(',')]
        is_error= False 
        for day in week_days:
            if(not self.check(author, day, start_tm, end_tm)):
                return JsonResponse({"error": "Slot already filled with busy slot"}, status= status.HTTP_400_BAD_REQUEST)
            data= {
                "author": author,
                "title": title,
                "week_day": day,
                "start_time": start_time,
                "end_time": end_time
            }
            serializer= AASlotSerializer(data= data)
            if(serializer.is_valid()):
                event= serializer.save()
                #return Response(serializer.data, status= status.HTTP_201_CREATED)
            else:
                is_error= True 
                #return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        if(not is_error):
            return JsonResponse({"status": "success"}, status= status.HTTP_201_CREATED)
        else: 
            return JsonResponse({"status": "error"}, status= status.HTTP_400_BAD_REQUEST)


class GetAASlot(APIView):
    
    def get(self, request):
        user= request.user
        evs= AASlot.objects.filter(author= user)
        serializer= AASlotSerializer(evs, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)


class CreateBusySlots(APIView):
    
    def post(self, request):
        author= request.user.id 
        title= request.data.get("title")
        week_days= request.data.get("week_day")
        start_time= request.data.get("start_time")
        end_time= request.data.get("end_time")
        
        week_days= [int(x) for x in week_days.split(',')]
        is_error= False 
        for day in week_days:
            data= {
                "author": author,
                "title": title,
                "week_day": day,
                "start_time": start_time,
                "end_time": end_time
            }
            serializer= BusySlotSerializer(data= data)
            if(serializer.is_valid()):
                event= serializer.save()
            else:
                is_error= True 
        if(not is_error):
            return JsonResponse({"status": "success"}, status= status.HTTP_201_CREATED)
        else:
            return JsonResponse({"status": "error"}, status= status.HTTP_400_BAD_REQUEST)



class GetBusySlot(APIView):
    
    def get(self, request):
        user= request.user
        evs= BusySlot.objects.filter(author= user)
        serializer= BusySlotSerializer(evs, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)


class ListEvents(APIView):
    permission_classes= ()

    def get(self, request):
        user= request.user
        evs= Event.objects.filter(author= user)
        serializer= EventSerializer(evs, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)



class CreatePE(APIView):

    def check_busy_slots(self, author, date_start, date_end):
        # 2019-04-24T06:00:00Z
        start_dt= parse(date_start)
        end_dt= parse(date_end)
        start_dt= start_dt + timedelta(seconds= 1)

        week_day= start_dt.weekday() 
        start_time= start_dt.time()
        end_time= end_dt.time()
        bes= BusySlot.objects.filter(author= author, week_day= week_day, start_time__range= (start_time, end_time))
        bel= len(bes)
        bes= BusySlot.objects.filter(author= author, week_day= week_day, end_time__range= (start_time, end_time))
        bel+= len(bes)
        log.info("BusySlot len is {}".format(str(bel)))
        return bel==0 
    
    def check_pending_event(self, author, date_start, date_end):       
        start_dt= parse(date_start)
        end_dt= parse(date_end)
        start_dt= start_dt + timedelta(seconds= 1)

        pes= PendingEvent.objects.filter(author= author, date_start__range= (start_dt, end_dt))
        pel= len(pes)
        pes= PendingEvent.objects.filter(author= author, date_end__range= (start_dt, end_dt))
        pel+= len(pes)
        log.info("PendingEvent len is {}".format(str(pel)))
        return pel==0

    def check_event(self, author, date_start, date_end):       
        start_dt= parse(date_start)
        end_dt= parse(date_end)
        start_dt= start_dt + timedelta(seconds= 1)

        pes= Event.objects.filter(author= author, date_start__range= (start_dt, end_dt))
        pel= len(pes)
        pes= Event.objects.filter(author= author, date_end__range= (start_dt, end_dt))
        pel+= len(pes)
        log.info("Event len is {}".format(str(pel)))
        return pel==0

    def notify(self, user, msg):
        log.info("Notifying "+str(user)) 
        noti= Notification(user= user, text= msg, seen= False)   
        noti.save() 

    def send_invite(self, pe, members, cuser, start_dt, end_dt):
        log.info("Sending invite of "+str(pe))
        for member in members:
            user= User.objects.get(username= member)
            invite= Invite(pe= pe, ref= user, accepted= False)
            if(user==cuser):
                invite= Invite(pe= pe, ref= user, accepted= True)
            else:
                start_tm= start_dt.time()        
                end_tim= end_dt.time()            
                week_day= start_dt.weekday()   
                aas= AASlot.objects.filter(author= user, week_day= week_day, start_time__lte= start_tm, end_time__gte= end_tim)
                log.info("AAS is {}".format(str(aas)))
                if(len(aas)>0):
                    log.info("Auto approving for {}".format(user))
                    invite= Invite(pe= pe, ref= user, accepted= True)
                    self.notify(user, "Meeting invite sent by {} has been auto approved".format(cuser))
                else: 
                    invite= Invite(pe= pe, ref= user, accepted= False)
                    self.notify(user, "{} sent you a meeting invitation".format(cuser))
                    log.info("Invite sent to "+str(user.username))
            invite.save()



    def post(self, request):
        author= request.user.id 
        title= request.data.get("title")
        date_start= request.data.get("date_start")
        date_end= request.data.get("date_end")
        include_author= request.data.get("include_author")

        start_dt= datetime.strptime(date_start, "%Y-%m-%dT%H:%M")
        end_dt= datetime.strptime(date_end, "%Y-%m-%dT%H:%M")
        
        raw_members= request.data.get("members")
        members= raw_members.split()
        if(include_author):
            members.append(str(request.user))

        if(not self.check_busy_slots(author, date_start, date_end)):
            return JsonResponse({"error": "Slot not available: Busy Slot"})

        if(not self.check_pending_event(author, date_start, date_end)):
            return JsonResponse({"error": "Slot not available: Pending Event"})

        if(not self.check_event(author, date_start, date_end)):
            return JsonResponse({"error": "Slot not available: Event"})

        data= {
            "author": author,
            "title": title,
            "date_start": date_start,
            "date_end": date_end,
            "members": json.dumps(members)
        }
        serializer= PendingEventSerializer(data= data)
        if(serializer.is_valid()):
            pe= serializer.save()
            self.send_invite(pe, members, request.user, start_dt, end_dt)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class ShowPMSatus(APIView):
    def get(self, request):
        user= request.user
        pes= PendingEvent.objects.filter(author= user)

        data= []
        for pe in pes:
            out= {}
            out['id']= pe.id
            out['title']= pe.title 
            invs= pe.invite_set.all()
            out['total']= len(invs)  
            out['accepted']= 0
            accepted_members= []
            remaining_members= []
            for inv in invs:
                if(inv.accepted):
                    out['accepted']+= 1
                    accepted_members.append(str(inv.ref))
                else:
                    remaining_members.append(str(inv.ref))
            out['accepted_by']= accepted_members
            out['remaining_members']= remaining_members
            data.append(out)
        return JsonResponse({"pending_events": data})


class ShowInvites(APIView):
    def get(self, request):
        user= request.user
        invites= user.invite_set.all()
        data= []
        for invite in invites:
            if(invite.accepted):
                continue
            out= {}
            out['id']= invite.id 
            out['event_title']= invite.pe.title 
            out['invited_by']= invite.pe.author.username
            data.append(out) 
        return JsonResponse({"invites": data})


class AcceptInvite(APIView):

    def notify(self, user, msg):
        noti= Notification(user= user, text= msg, seen= False)   
        noti.save() 
        log.info("Notified: {}, Message: {}".format(str(user), msg))

    def delete_things(self, pe):
        #Delete Invites
        invs= pe.invite_set.all()
        invs.delete()   
        log.info("Invites Deleted")
        #Delete Pending event 
        pe.delete()
        log.info("Pending Event Deleted")

    def make_event(self, pe):
        log.info("Making permanent event of {}".format(str(pe)))
        data= {
            "author": pe.author.id,
            "title": pe.title,
            "date_start": pe.date_start.strftime("%Y-%m-%dT%H:%M"),
            "date_end": pe.date_end.strftime("%Y-%m-%dT%H:%M"),
            "members": pe.members 
        }
        log.info("Data is: {}".format(data))
        serializer= EventSerializer(data= data)
        if(serializer.is_valid()):
            ev= serializer.save()
            log.info("Event successfully created")
            self.notify(pe.author, "All members have accepted {} meeting invite.".format(pe.title))
            members= json.loads(pe.members) 
            log.info("Members is {}".format(str(members)))
            log.info("Type of members is {}".format(type(members)))
            log.info("Lenght is {}".format(len(members)))
            for member in members:
                user= User.objects.get(username= member)
                self.notify(user, "Meeting {} confirmed".format(pe.title))
            self.delete_things(pe)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)



    def check(self, pe):
        log.info("Checking pending event status")
        invs= pe.invite_set.all()
        total = len(invs)  
        accepted= 0
        for inv in invs:
            if(inv.accepted):
                accepted+= 1
        log.info("Total: {}, Accepted: {}".format(total, accepted))
        if(total== accepted):
            self.make_event(pe) 
            return True 
        else:
            return False 
        

    def get(self, request):
        user= request.user
        id= request.GET['id']
        invite = Invite.objects.get(id= id)
        if(invite.ref==user):
            invite.accepted= True   
            invite.save()
            log.info("Invite accepted by {}".format(str(user)))
            self.notify(invite.pe.author, "{} accepted {} meeting invite.".format(user, invite.pe.title))
            self.check(invite.pe)
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error"})


from datetime import datetime
#from pytz import timezone 


#TODO
#Currently checking only Event
#Add PendingEvent and BusySlots
class AvailableSlots(APIView):

    def get_events(self, user, start_date, end_date):
        evs1= Event.objects.filter(author= user, date_start__range= (start_date, end_date))
        evs2= Event.objects.filter(author= user, date_end__range= (start_date, end_date))

        el1= [ev for ev in evs1]
        el2= [ev for ev in evs2]
        el= list(set(el1) | (set(el2)))

        event_slots= []
        for ev in el:
            ds= datetime.timestamp(ev.date_start)
            #ct= datetime.fromtimestamp(ds)
            #new_ct= ct.astimezone(timezone('utc'))
            de= datetime.timestamp(ev.date_end)
            event_slots.append((ds, de))
        return event_slots

    def get_pending_events(self, user, start_date, end_date):
        evs1= PendingEvent.objects.filter(author= user, date_start__range= (start_date, end_date))
        evs2= PendingEvent.objects.filter(author= user, date_end__range= (start_date, end_date))

        el1= [ev for ev in evs1]
        el2= [ev for ev in evs2]
        el= list(set(el1) | (set(el2)))

        event_slots= []
        for ev in el:
            ds= datetime.timestamp(ev.date_start)
            #ct= datetime.fromtimestamp(ds)
            #new_ct= ct.astimezone(timezone('utc'))
            de= datetime.timestamp(ev.date_end)
            event_slots.append((ds, de))
        return event_slots

    #Implement it
    def get_busy_slots(self, user, start_date, end_date):
        pass 


    def post(self, request):
        start_date= request.data.get("start_date")
        end_date= request.data.get("end_date")
        duration= request.data.get("duration")
        duration= int(duration)

        user= request.user
        
        evs1= Event.objects.filter(author= user, date_start__range= (start_date, end_date))
        evs2= Event.objects.filter(author= user, date_end__range= (start_date, end_date))

        el1= [ev for ev in evs1]
        el2= [ev for ev in evs2]
        el= list(set(el1) | (set(el2)))

        na_slots= []
        for ev in el:
            ds= datetime.timestamp(ev.date_start)
            #ct= datetime.fromtimestamp(ds)
            #new_ct= ct.astimezone(timezone('utc'))
            de= datetime.timestamp(ev.date_end)
            na_slots.append((ds, de))


        start_dt= datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        end_dt= datetime.strptime(end_date, "%Y-%m-%dT%H:%M")

        na_slots.append((0 , datetime.timestamp(start_dt)))
        na_slots.append((datetime.timestamp(end_dt), 0))
        na_slots.sort()

        result= []

        for i in range(1, len(na_slots)):
            my_start= na_slots[i-1][1]
            my_end= na_slots[i][0]
            if((my_end- my_start)>=duration):
                while((my_end- my_start)>=duration):
                    s_start= my_start
                    e_end= my_start+duration
                    my_start= e_end
                    dsn= datetime.fromtimestamp(s_start)
                    den= datetime.fromtimestamp(e_end)            
                    result.append({"from": dsn, "to": den})

        astatus= ""
        if(len(result)<=0):
            astatus= "no slot available"
        else:
            astatus= "success"

        output= {"status": astatus, "data": result}
        return JsonResponse(output, status= status.HTTP_200_OK)


class GetBestAvailableSlot(APIView):

    def post(self, request):
        avs= AvailableSlots()
        response= avs.post(request) 
        out= json.loads(response.content)
        if(out['status']=='success'):
            data= out['data']
            if(len(data)==1):
                best_slot= data[0]
            else:
                mid= len(data)/2
                best_slot= data[int(mid)]
            output= {"status":"success", "data":best_slot}
            return JsonResponse(output, status= status.HTTP_200_OK) 
        return JsonResponse(out, status= status.HTTP_200_OK)



class DaySchedule(APIView):
    
    def post(self, request):
        dt= request.POST.get("dt")
        etype= request.POST.get("type")
        dt= datetime.strptime(dt, "%Y-%m-%dT%H:%M")

        dt_start= dt.date()
        dt_end= dt_start+ timedelta(days= 1)
        user= request.user
        
        data= {}
        
        if(etype in ['all','events']):
            evs= Event.objects.filter(author= user, date_start__gte= dt_start, date_end__lte= dt_end)
            evt_serializer= EventSerializer(evs, many= True)
            log.info("Events are {}".format(evt_serializer.data))
            data['events']= evt_serializer.data 

        if(etype in ['all', 'pending_events']):    
            pevs= PendingEvent.objects.filter(author= user, date_start__gte= dt_start, date_end__lte= dt_end)
            pevs_serializer= PendingEventSerializer(pevs, many= True) 
            log.info("Pending Events are {}".format(pevs_serializer.data))
            data['pending_events']= pevs_serializer.data 

        if(etype in ['all', 'busy_slots']):
            week_day= dt_start.weekday() 
            bss= BusySlot.objects.filter(author= user, week_day= week_day)
            bs_serializer= BusySlotSerializer(bss, many= True)              
            log.info("Busy slots are {}".format(bs_serializer.data))     
            data['busy_slots']= bs_serializer.data  

        return JsonResponse(data, status= status.HTTP_200_OK)




class GetShareableLink(APIView):
    
    def post(self, request):
        user= request.user                       
        title= request.POST.get("title") 
        description= request.POST.get("description")
        # Duration in seconds
        duration= request.POST.get('duration_sec')

        data= {
            "user": user.id, 
            "title": title, 
            "description": description,
            "duration": duration
        }

        serializer= ShareableLinkSerializer(data= data)
        if(serializer.is_valid()):
            event= serializer.save()
            out= serializer.data 
            id= out['id']
            link= 'http://localhost:8000/calen/browse?id={}'.format(id) 
            return JsonResponse({
                "status": "success",
                "link": link
            }, status= status.HTTP_200_OK)
        else:
            return JsonResponse({
                "status": "error",
                "error_msg": serializer.error_messages,
                "error": serializer.errors
            }, status= status.HTTP_400_BAD_REQUEST)



class BrowseLink(APIView):
    authentication_classes= ()
    permission_classes= ()

    def get_page(self, data):
        title= data['title']
        description= data['description']
        duration= data['duration']

        out= "<h2>{}</h2>".format(title)
        out+= "<h3>{}</h3>".format(description)
        out+= "Duration: <b>{}</b><br>".format(duration)
        timing= self.get_today_slots(duration)
        out+= "Start Time: {}<br>".format(timing['start_time'])
        out+= "End Time: {}<br>".format(timing['end_time'])
        return out 

    def get_today_slots(self, duration):
        start_time= datetime.now()   
        end_time= start_time.date() + timedelta(days= 1) 
        data={
            "start_time": str(start_time),
            "end_time": str(end_time)
        }
        return data 

    def get(self, request):
        id= request.GET.get('id') 
        log.info("ID is "+str(id))
        sl= ShareableLink.objects.get(id= id) 
        log.info("sl is {}".format(sl))
        serializer= ShareableLinkSerializer(sl) 
        log.info("serializer data is {}".format(serializer.data))

        #return JsonResponse(serializer.data, status= status.HTTP_200_OK) 
        return HttpResponse(self.get_page(serializer.data))



        