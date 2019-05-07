from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import generics

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse

from .models import Event, PendingEvent, Invite, BusySlot, AASlot, Notification
from .serializers import EventSerializer, UserSerializer, PendingEventSerializer, InviteSerializer, BusySlotSerializer, AASlotSerializer, NotificationSerializer

from dateutil.parser import parse
from datetime import timedelta

from .hiutil import username_to_id
import json 

from .mylog import log 



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

    def notify(self, user, msg):
        log.info("Notifying "+user) 
        noti= Notification(user= user, text= msg, seen= False)   
        noti.save() 
        log.info("Notified") 

    def send_invite(self, pe, members, cuser, start_dt, end_dt):
        log.info("Sending invite of "+str(pe))
        for member in members:
            user= User.objects.get(username= member)
            if(user==cuser):
                invite= Invite(pe= pe, ref= user, accepted= True)
            else:
                ##Check for auto approve####################

                start_tm= start_dt.time()        
                end_tim= end_dt.time()            
                week_day= start_dt.weekday()   
                aas= AASlot.objects.filter(author= user, week_day= week_day, start_time__lte= start_tm, end_time__gte= end_tim)
                if(len(ass)>0):
                    pass 
                    # Auto aprove
                else: 
                    pass                     
                    # Can't auto aprove
                ############################################
                invite= Invite(pe= pe, ref= user, accepted= False)
                self.notify(user, "{} sent you a meeting invitation".format(cuser))
            invite.save()
            log.info("Invite sent to "+str(user.username))

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
        out= ""
        for pe in pes:
            out+= "<h4>"+str(pe)+"</h4>"
            out+= "<table border= '1px solid black'>"
            invs= pe.invite_set.all()
            total= len(invs)
            accepted= 0
            for inv in invs:
                if(inv.accepted):
                    accepted+=1
                    out+= "<tr><td>"+str(inv.ref)+"</td><td>Accepted</td></tr>"
                else:
                    out+= "<tr><td>"+str(inv.ref)+"</td><td>Not accepted</td></tr>"
            out+= "</table>"
            out+= "<br><b>"+str(accepted)+" invites have been accepted out of "+str(total)+"</b>"
        if(out==""):
            return HttpResponse("No event")
        return HttpResponse(out)

class ShowInvites(APIView):
    def get(self, request):
        user= request.user
        invites= user.invite_set.all()
        serializer= InviteSerializer(invites, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
        if(len(invites)<=0):
            return HttpResponse("No Invite")
        res= ""
        for invite in invites:
            res+= "<br>Your invite is "+str(invite)
        return HttpResponse(res)


class AcceptInvite(APIView):
    def get(self, request):
        user= request.user
        id= request.GET['id']
        invite = Invite.objects.get(id= id)
        if(invite.ref==user):
            invite.accepted= True   
            invite.save()
            return HttpResponse(str(invite)+" successfully accepted")
        else:
            return HttpResponse("Unauthenticated try")


from datetime import datetime
#from pytz import timezone 

class AvailableSlots(APIView):

    def post(self, request):
        start_date= request.data.get("start_date")
        end_date= request.data.get("end_date")
        duration= request.data.get("duration")
        duration= int(duration)

        user= request.user
        
        evs1= Event.objects.filter(author= user, date_start__range= (start_date, end_date))
        evs2= Event.objects.filter(author= user, date_start__range= (start_date, end_date))

        el1= [ev for ev in evs1]
        el2= [ev for ev in evs2]
        el= list(set(el1) | (set(el2)))

        na_slots= []
        for ev in el:
            ds= datetime.timestamp(ev.date_start)
            ct= datetime.fromtimestamp(ds)
            #new_ct= ct.astimezone(timezone('utc'))

            de= datetime.timestamp(ev.date_end)
            na_slots.append((ds, de))


        start_dt= datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        end_dt= datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
        
        out= ""
        out+= "<h3>Required slot</h3>"
        out+= "Start: {}".format(str(start_dt))+"<br>"
        out+= "End  : {}".format(str(end_dt))+"<br><br>"
        out+= "Duration :{}".format(str(duration))+"<br>"
        out+= "<h3>Not available slots</h3>"

        for ds, de in na_slots:
            dsn= datetime.fromtimestamp(ds)
            den= datetime.fromtimestamp(de)            
            out+= "From "+str(dsn)+" to "+str(den)+"<br>"

        na_slots.append((0 , datetime.timestamp(start_dt)))
        na_slots.append((datetime.timestamp(end_dt), 0))
        na_slots.sort()

        out+= "<h3>Available slots</h3>"
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
                    out+= "From "+str(dsn)+" to "+str(den)+"<br>"
                    result.append({"from": dsn, "to": den})
            #out+= "<br>"

        # Readable response
        #return HttpResponse(out, status= status.HTTP_200_OK)

        astatus= ""
        if(len(result)<=0):
            astatus= "no slot available"
        else:
            astatus= "success"

        output= {"status": astatus, "data": result}
        return JsonResponse(output, status= status.HTTP_200_OK)

