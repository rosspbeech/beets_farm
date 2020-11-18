from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from datetime import datetime
import random

from django.views import View

from beets.forms import BeetForm
from beets.forms import PersonaForm, UserForm, UserProfileForm
from beets.models import Persona, User, UserProfile
from beets.models import Beet



def index(request):
    # query database for a list of all personas
    # order by the views they have had
    # retrieve top 5 -- or all if less than 5
    # place list in context dict along with our boldmessage
    persona_list = Persona.objects.order_by('-views')[:5]
    beets_list = Beet.objects.order_by('-plays')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'These beets are: Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['personas'] = persona_list
    context_dict['beets'] = beets_list
    context_dict['visits'] = int(request.COOKIES.get('visits', '1'))
    response = render(request, 'beets/index.html', context=context_dict)
    visitor_cookie_handler(request, response)
    return response


def about(request):
    return render(request, 'beets/about.html')



def show_beet(request, beet_name_slug):
    context_dict = {}

    try:
        beet = Beet.objects.get(slug=beet_name_slug)
        context_dict['beet'] = beet

    except Beet.DoesNotExist:
        context_dict['beet'] = None

    return render(request, 'beets/beet.html', context = context_dict)


def personas(request):
    context_dict = {}
    personas = Persona.objects.all()
    context_dict['personas'] = personas
    return render(request, 'beets/talent.html', context = context_dict)



def show_persona(request, persona_name_slug):
    # create a context dictionary to pass to the template
    context_dict = {}

    try:
        # Can we find a persona name slug with the given name
        # if we cant then the .get() method raises DoesNotExist exception
        # the .get method returns one instance of a model or an exception

        persona = Persona.objects.get(slug=persona_name_slug)

        # retrieve all the associated beets with the persona
        # the filter will return a list of beet objects or an empty list
        beets = Beet.objects.filter(persona=persona)

        # add our results list to template context undername beets
        context_dict['beets'] = beets

        # we also add the persona object form the db to the context dict for verification
        context_dict['persona'] = persona
    except Persona.DoesNotExist:
        # we get here if we dont find the persona
        # dont do anything as the template will display 'no persona' msg for us
        context_dict['beets'] = None
        context_dict['persona'] = None

    return render(request, 'beets/persona.html', context=context_dict)


@login_required()
def add_persona(request):
    form = PersonaForm()

    # Is it a HTTP POST
    if request.method == 'POST':
        form = PersonaForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new persona to the db after associating current user
            persona = form.save(commit=False)
            persona.owner = request.user.profile
            persona.save()
            # Return the user to the homepage
            return redirect('/beets/')
        else:
            # The supplied form contained errors
            print(form.errors)
    return render(request, 'beets/add_persona.html', {'form': form})


@login_required()
def add_beet(request, persona_name_slug):
    try:
        persona = Persona.objects.get(slug=persona_name_slug)

    except Persona.DoesNotExist:
        persona = None

    if persona is None:
        return redirect('/beets/')

    form = BeetForm()

    if request.method == 'POST':
        form = BeetForm(request.POST, request.FILES)

        if form.is_valid():
            if persona:
                beet = form.save(commit=False)
                beet.sound_file = request.FILES['sound_file']
                beet.persona = persona
                beet.save()

                return redirect(reverse('beets:show_persona', kwargs={'persona_name_slug':persona_name_slug}))

        else:
            print(form.errors)

    context_dict = {'form':form, 'persona':persona}
    return render(request, 'beets/add_beet.html', context=context_dict)


@login_required()
def edit_persona(request, persona_name_slug):
    persona = Persona.objects.get(slug=persona_name_slug)

    pform = PersonaForm(instance=persona)

    if request.method == 'POST':
        pform = PersonaForm(request.POST, instance=persona)

        if pform.is_valid():
            p = pform.save(commit=False)
            p.owner = request.user.profile
            p.save()
            # Return the user to the homepage
            return redirect('/beets/userHub/')

    return render(request, 'beets/edit_persona.html', {'form': pform, 'persona': persona})

@login_required()
def edit_beet(request, beet_id):
    beet = Beet.objects.get(id=beet_id)

    bform = BeetForm(instance=beet)

    if request.method == 'POST':
        bform = BeetForm(request.POST, instance=beet)

        if bform.is_valid():
            p = bform.save(commit=False)
            p.save()
            # Return the user to the homepage
            return redirect('/beets/userHub/')

    return render(request, 'beets/edit_beet.html', {'form': bform, 'beet': beet})



def register(request):
    # Boolean value to let us know whether registration is successful
    registered = False

    # If it is a http post we want to process data
    if request.method == 'POST':
        # Attempt to grab the raw form info
        # This view uses both the UserForm and UserProfileForm
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # save users form data to the database
            user = user_form.save()

            # Set_password hashes the password for us, once we hash it we update the user model.
            user.set_password(user.password)
            user.save()

            # Now we deal with UserProfile
            # We set commit=False to delay saving the model until we are ready - to avoid integrity issues
            profile = profile_form.save(commit=False)
            profile.user = user


            # Did they upload a photo?
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']


            # now we save this instance of userprofile
            profile.save()

            # Update variable to reflect success in reg
            registered = True
        else:

            print(user_form.errors, profile_form.errors)

    else:
        # Not a POST so render instances of the forms for user to complete
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'beets/register.html', context = {'user_form': user_form,
                                                             'profile_form':profile_form,
                                                             'registered': registered})


def user_login(request):
    context_dict ={}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # find the user
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('beets:index'))
            else:
                return HttpResponse('Your account is disabled')
        else:
            print(f"Invalid login details: {username}, {password}")
            context_dict['error'] = "Invalid login details"
            return render(request, 'beets/login.html', context_dict)

    else:
        return render(request, 'beets/login.html')

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('beets:index'))


def visitor_cookie_handler(request, response):
    # Get number of visits to the site
    # Cookies.get obtains the visits cookie
    # If it exists, we cast it to an int
    # If it does not exist, default is 1
    visits = int(request.COOKIES.get('visit', '1'))

    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    #if its been more than a day since the last visit
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update last visit cookie
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        # set the last visit cooke
        response.set_cookie('last_visit', last_visit_cookie)

    # Update set the visits cookie
    response.set_cookie('visits', visits)


# Retrieves a random song from database
# Called from index page using ajax
class RandomSongView(View):
    def get(self, request):

        #get the previous beet played, if none then its preset is zero
        beetid = request.GET['beetid']
        # Convert this to an int
        bid = int(beetid)

        # Get the number of beets there are
        numberOfBeets = Beet.objects.all().count()
        # Choose a random number between 1 and the number of beets
        rand = random.randint(1,numberOfBeets)
        # if the previous random num is same as the new one then get another random num

        while rand == bid:
            rand = random.randint(1,numberOfBeets)

        # use random num to get a beet
        randBeet = Beet.objects.get(id=rand)

        s = randBeet.sound_file.url
        b = randBeet.name
        c = randBeet.persona.name
        data={}
        data['name'] = b
        data['src'] = s
        data['artist']= c
        data['bid'] = rand


        return JsonResponse(data, safe=False)

@login_required
def userHub(request):
    request.user
    userPersonas = Persona.objects.filter(owner=request.user.profile)
    context_dict = {}
    context_dict['personas'] = userPersonas

    return render(request, 'beets/hub.html', context=context_dict)