from django.shortcuts import render
from account.models import Club, Sport, City
from django.db.models import Q

def all_clubs(request):
    clubs = Club.objects.all()
    sports = Sport.objects.all()
    cities = City.objects.all()

    q = request.GET.get("q", "")
    sport_id = request.GET.get("sport")
    city_id = request.GET.get("city")

    if q:
        clubs = clubs.filter(
            Q(clubName__icontains=q) |
            Q(user__username__icontains=q)
        )
    if sport_id:
        clubs = clubs.filter(sport__id=sport_id)
    if city_id:
        clubs = clubs.filter(city__id=city_id)

    context = {
        "clubs": clubs,
        "sports": sports,
        "cities": cities
    }
    return render(request, 'clubs/all_clubs.html', context)


