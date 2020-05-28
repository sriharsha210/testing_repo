from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from amadeus import Client, ResponseError
import datetime
import time
import pprint


def flight_inspiration(origin, destination,start_date, end_date, no_of_travelers):
    amadeus = Client(
        client_id='pcPPeMPWjPgD5KwA9fKEr1AVecR0ImYL',
        client_secret='HGl8qfUAsFifnhy8'
    )
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=datetime.datetime.strptime(start_date, "%m/%d/%Y").strftime("%Y-%m-%d"),
            adults=no_of_travelers,
            children=2)
        print("response")
        pprint.pprint(response.status_code)
        print(" ")
        return flights_response_parser(response.result)
    except ResponseError as error:
        print("Erroring")
        print(error)


def flights_response_parser(response):
    flight_parsed_list = []
    count = 0
    print('id', 'oneway', 'num of bookable seats', 'flight_total_duration', 'depart_info', 'ariv_info')
    for a in range(len(response["data"])):
        for b in range(len(response["data"][a]['itineraries'])):
            for c in range(len(response["data"][a]['itineraries'][b]['segments'])):
                count += 1
                response["data"][a]['itineraries'][b]['segments'][c]['departure'].setdefault("terminal", "NA")
                response["data"][a]['itineraries'][b]['segments'][c]['arrival'].setdefault("terminal", "NA")
                flight_parsed_list.append([
                    response["data"][a]["id"],
                    response["data"][a]["oneWay"],
                    response["data"][a]["numberOfBookableSeats"],
                    response["data"][a]['itineraries'][b]['duration'],
                    response["data"][a]['itineraries'][b]['segments'][c]['carrierCode'],
                    response["data"][a]['itineraries'][b]['segments'][c]['number'],
                    response["data"][a]['itineraries'][b]['segments'][c]['aircraft']['code'],
                    response["data"][a]['itineraries'][b]['segments'][c]['departure']['iataCode'],
                    response["data"][a]['itineraries'][b]['segments'][c]['departure']['terminal'],
                    response["data"][a]['itineraries'][b]['segments'][c]['departure']['at'],
                    response["data"][a]['itineraries'][b]['segments'][c]['arrival']['iataCode'],
                    response["data"][a]['itineraries'][b]['segments'][c]['arrival']['terminal'],
                    response["data"][a]['itineraries'][b]['segments'][c]['arrival']['at'],
                    response["data"][a]['itineraries'][b]['segments'][c]['duration'],
                    response["data"][a]['itineraries'][b]['segments'][c]['numberOfStops'],
                    response["data"][a]['price']['currency'],
                    response["data"][a]['price']['grandTotal']
                ]
                )

    print(" ")
    print(count)
    return flight_parsed_list

def createUser(request):
    print(request.method)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
        return redirect('users-login')
    else:
        form = UserCreationForm()

    return render(request, "users/register.html", {"form": form})



def home(request):
    return render(request, "users/index.html")

def home2(request):
    print(request.method)
    print("hello world")
    if request.method == 'POST':
        origin = request.POST.get('from')
        destination=request.POST.get('to')
        start_date=request.POST.get('date_start')
        end_date=request.POST.get('date_end')
        no_of_travelers = request.POST.get('num_travs')
        print(no_of_travelers)
        print(origin,destination,start_date,end_date,no_of_travelers)
        print(type(start_date),type(end_date))
        flights_info_list=flight_inspiration(origin,destination,start_date,end_date,no_of_travelers)
        trav_data = origin + destination + start_date + no_of_travelers
        print(len(flights_info_list))
        if trav_data!=' ':
            print("Inside the If function",trav_data)
            context ={ 'flight_results':flights_info_list,
                       'num_resuls': flights_info_list[-1][0]}
            '''
            flights_context = { 'flights_info' : 
                [
                    data[flight1],
                    data[flight2]
                ]
            
            }            
            '''
            return render(request,'harsha_templates/places_extension.html',context)
        else:
            #print("somehow coming here")
            return render(request, "harsha_templates/search_extension.html")

    else:
        print("in else")
        return render(request, "harsha_templates/search_extension.html")

def places2(request):
    return render(request, "harsha_templates/places_extension.html")

