from django.shortcuts import render
from account.models import Athlete, Sport, City
from django.db.models import Q

def all_athletes(request):
    athletes = Athlete.objects.filter(isPrivate=False)
    sports = Sport.objects.all()
    cities = City.objects.all()

    q = request.GET.get("q", "")
    sport_id = request.GET.get("sport")
    city_id = request.GET.get("city")
    gender = request.GET.get("gender")

    if q:
        athletes = athletes.filter(
            Q(user__first_name__icontains=q) |
            Q(user__username__icontains=q)
        )
    if sport_id:
        athletes = athletes.filter(sport__id=sport_id)
    if city_id:
        athletes = athletes.filter(city__id=city_id)
    if gender:
        athletes = athletes.filter(gender=gender)

    context = {
        "athletes": athletes,
        "sports": sports,
        "cities": cities
    }
    return render(request, 'athlete/all_athletes.html', context)
