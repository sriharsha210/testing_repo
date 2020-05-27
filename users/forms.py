from django import forms

def get_travel_data(request):
    origin = request.POST.get("from")
    print(origin)






