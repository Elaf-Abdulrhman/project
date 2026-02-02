
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from .forms import OfferForm, ApplicationResponseForm
from .models import Offer, Application
from account.models import Club,Sport, Athlete,City

@login_required
def add_offer(request):
    if not hasattr(request.user, 'club'):
        return HttpResponseForbidden("Only clubs can add offers.")

    club = request.user.club

    if not club.is_premium:
        one_week_ago = timezone.now() - timedelta(days=7)
        offers_last_week = Offer.objects.filter(user=request.user, created_at__gte=one_week_ago).count()

        if offers_last_week >= 3:
            messages.error(request, "You can only post 3 offers per week. Upgrade your plan to post unlimited offers!","alert-danger")
            return redirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.save()
            messages.success(request, "Your offer has been successfully posted.", "alert-success")
            return redirect('offers:all_offers')
    else:
        form = OfferForm()

    return render(request, 'offers/add_offer.html', {'form': form})

def all_offers(request):
    offers = Offer.objects.all().order_by('-created_at')

    city_id = request.GET.get('city')
    sport_id = request.GET.get('sport')
    gender = request.GET.get('gender')

    if city_id:
        offers = offers.filter(user__club__city_id=city_id)
    if sport_id:
        offers = offers.filter(user__club__sport_id=sport_id)

    if gender:
        offers = offers.filter(gender__in=[gender, 'A'])

    cities = City.objects.all()
    sports = Sport.objects.all()

    # Pagination
    page = int(request.GET.get('page', 1))
    per_page = 6
    start = (page - 1) * per_page
    end = page * per_page
    filtered_offers = offers[start:end]

    # AJAX scroll
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        offers_data = [
            {
                'id': o.id,
                'title': o.title,
                'content': o.content,
                'author': o.user.username,
                'first_name': o.user.first_name,
                'last_name': o.user.last_name,
                'club_id': o.user.club.id,
                'club_photo_url': o.user.club.photo.url if o.user.club.photo else None,
                'photo_url': o.photo.url if o.photo else None,
                'created_at': o.created_at.strftime('%B %d, %Y'),
            }
            for o in filtered_offers
        ]
        return JsonResponse({'offers': offers_data})

    return render(request, 'offers/all_offers.html', {
        'offers': filtered_offers,
        'cities': cities,
        'sports': sports,
    })



def offer_details(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)

    has_applied = False
    if request.user.is_authenticated and hasattr(request.user, 'athlete'):
        has_applied = offer.applications.filter(athlete=request.user).exists()

    return render(request, 'offers/offer_details.html', {
        'offer': offer,
        'has_applied': has_applied
    })


@login_required
def delete_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        offer.delete()
        return redirect('offers:all_offers')
    return render(request, 'offers/delete_offer.html', {'offer': offer})

@login_required
def edit_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('offers:offer_details', offer_id=offer.pk)
    else:
        form = OfferForm(instance=offer)
    return render(request, 'offers/edit_offer.html', {'form': form, 'offer': offer})

@login_required
def my_offers(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    club_offers = Offer.objects.filter(user=club.user).order_by('-created_at')
    return render(request, 'offers/my_offers.html', {'offers': club_offers, 'club': club})

@login_required
def apply_to_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    if not hasattr(request.user, 'athlete'):
        return HttpResponseForbidden("Only athletes can apply.")

    existing_application = Application.objects.filter(offer=offer, athlete=request.user).first()
    if existing_application:
        return redirect('offers:offer_details', offer_id=offer.id)

    if request.method == 'POST':
        Application.objects.create(
            offer=offer,
            athlete=request.user
        )
        return redirect('offers:my_applications')

    return render(request, 'applications/apply.html', {'offer': offer})

@login_required
def offer_applicants(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    if request.user != offer.user:
        return HttpResponseForbidden("Not allowed.")
    applications = offer.applications.select_related('athlete').all()
    return render(request, 'applications/applicants.html', {'offer': offer, 'applications': applications})

@login_required
def respond_to_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    if request.user != application.offer.user:
        return HttpResponseForbidden("You can't do this.")

    if request.method == 'POST':
        form = ApplicationResponseForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('offers:offer_applicants', offer_id=application.offer.id)
    else:
        form = ApplicationResponseForm(instance=application)

    return render(request, 'applications/respond.html', {'form': form, 'application': application})

@login_required
def my_applications(request):
    applications = Application.objects.filter(athlete=request.user).select_related('offer').order_by('-created_at')
    return render(request, 'applications/my_applications.html', {'applications': applications})



@login_required
def application_detail(request, application_id):
    app = get_object_or_404(Application, id=application_id, athlete=request.user)
    return render(request, 'applications/application_detail.html', {'application': app})





@login_required
def application_response_detail(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    # Only allow the club that owns the offer to view it
    if request.user != application.offer.user:
        return HttpResponseForbidden("You are not allowed to view this response.")

    return render(request, 'applications/application_response_detail.html', {'application': application})
