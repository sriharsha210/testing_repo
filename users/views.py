from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from amadeus import Client, ResponseError, Location
import datetime
import time
import pprint


def flight_inspiration(origin, destination,start_date, end_date, no_of_travelers,no_of_child_travelers):
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
            children=no_of_child_travelers,
            max=5)
        print("response")
        pprint.pprint(response.status_code)
        print(" ")
        return (complete_flights_parser(response.result,origin, destination))
    except ResponseError as error:
        print("Erroring")
        print(error)


def flights_new_response_parser(response,origin,destination):
  flights_basic_info=[]
  for a in range(len(response["data"])):
    flights_basic_info.append([[
                                response["data"][a]['id'],
                                response["data"][a]['price']['grandTotal'],
                                response["data"][a]['price']['currency'],
                                response["data"][a]["numberOfBookableSeats"],
                                response["data"][a]['itineraries'][0]['duration'].strip('PT'),
                                origin,
                                destination]])
  return flights_basic_info

def flights_new_response_itineraries_parser(response):
  flights_itineraries_list=[]
  for a in range(len(response["data"])):
    for b in range(len(response["data"][a]['itineraries'][0]['segments'])):
      flights_itineraries_list.append(
          [
        a+1,
        response["data"][a]['itineraries'][0]['segments'][b]['aircraft']['code'],
        response["data"][a]['itineraries'][0]['segments'][b]['carrierCode'],
        response["data"][a]['itineraries'][0]['segments'][b]['number'],
        response["data"][a]['itineraries'][0]['segments'][b]['departure']['at'].split("T")[0],
        response["data"][a]['itineraries'][0]['segments'][b]['departure']['at'].split("T")[1],
        response["data"][a]['itineraries'][0]['segments'][b]['departure']['iataCode'],
        response["data"][a]['itineraries'][0]['segments'][b]['arrival']['at'].split("T")[0],
        response["data"][a]['itineraries'][0]['segments'][b]['arrival']['at'].split("T")[1],
        response["data"][a]['itineraries'][0]['segments'][b]['arrival']['iataCode'],
        response["data"][a]['itineraries'][0]['segments'][b]['duration'].strip('PT')
          ]
  )
  return flights_itineraries_list


def flights_related_dictionaries(response):
    amadeus = Client(
        client_id='pcPPeMPWjPgD5KwA9fKEr1AVecR0ImYL',
        client_secret='HGl8qfUAsFifnhy8'
    )

    cities_iata_dict = {}
    for city_iata in list(response["dictionaries"]['locations'].keys()):
        try:
            '''
            Which cities or airports start with 'r'?
            '''
            cities_response = amadeus.reference_data.locations.get(keyword=city_iata,
                                                                   subType=Location.CITY,
                                                                   view='LIGHT')
            cities_iata_dict[city_iata] = (cities_response.result["data"][0]['address']['cityName'])

        except ResponseError as error:
            print("error")
            raise error
    # print(cities_iata_dict)
    return (cities_iata_dict)


def complete_flights_parser(response, origin, destination):
    flights_itineraries_complete = []
    flights_complete_list = []
    cities_iata_dict = {}
    aircraft_nums_dict = {}
    aircraft_names_dict = {}

    flights_basic_info = flights_new_response_parser(response, origin, destination)

    flights_itineraries_list = flights_new_response_itineraries_parser(response)

    cities_iata_dict = flights_related_dictionaries(response)

    aircraft_nums_dict = response["dictionaries"]['aircraft']

    aircraft_names_dict = response["dictionaries"]['carriers']

    previous_id = int(flights_itineraries_list[0][0])
    while previous_id <= int(flights_itineraries_list[-1][0]):
        temp_list_2 = []
        for i in range(len(flights_itineraries_list)):
            if int(flights_itineraries_list[i][0]) == previous_id:
                temp_list_2.insert(i, flights_itineraries_list[i])
        flights_itineraries_complete.append(temp_list_2)
        previous_id += 1

    if len(flights_basic_info) == len(flights_itineraries_complete):
        for a in range(len(flights_basic_info)):
            flights_complete_list.append(flights_basic_info[a] + flights_itineraries_complete[a])

    return (flights_complete_list, cities_iata_dict, aircraft_nums_dict, aircraft_names_dict)

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
        no_of_child_travelers=request.POST.get('num_child')
        print(no_of_child_travelers)
        print(origin,destination,start_date,end_date,no_of_travelers,no_of_child_travelers)
        print(type(start_date),type(end_date))
        flights_complete_list,cities_iata_dict,aircraft_nums_dict,aircraft_names_dict=flight_inspiration(origin,destination,start_date,end_date,no_of_travelers,no_of_child_travelers)
        trav_data = origin + destination + start_date + no_of_travelers + no_of_child_travelers
        print(len(flights_complete_list))
        if trav_data!=' ':
            print("Inside the If function",trav_data)
            context ={ 'flight_results':flights_complete_list,
                       'num_resuls': len(flights_complete_list),
                       'cities_iata_dict':cities_iata_dict,
                       'aircraft_nums_dict':aircraft_nums_dict,
                       'aircraft_names_dict':aircraft_names_dict
                       }
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

