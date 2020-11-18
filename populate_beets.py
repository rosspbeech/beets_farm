import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beets_project.settings')


import django
django.setup()
from beets.models import Beet, Persona, UserProfile, User


def populate():
    #create a list of dictionaries containing beets
    #that we will add into each persona

    users = {'Ross': {'username': 'ross', 'email': 'ross@gmail.com', 'password': 'password'}}

    copper_beets = [
                    {'name': 'Eucharist Prayer',
                     'about': 'An electro take on a Christian Classic', 'sound_file': 'the_beets/eup.mp3'},
                    {'name': 'Ode to Billy Lewis',
                     'about': 'An ode to a great lad with some cracking lyrics', 'sound_file': 'the_beets/OdeToBillyLewis.mp3'}
                    ]

    exec_beets = [{'name': 'The Rise & Fall of McCauley Culkin',
                   'about': 'Two Hollywood execs find a fresh new talent and can see a bright future ahead', 'sound_file': 'the_beets/risenfall.mp3'},
                  {'name': 'Ode to Monty Don',
                   'about': 'A celebration of the nations favorite gardner', 'sound_file': 'the_beets/either_or.mp3'}
                  ]

    personas = {'Electric Copper': {'beets': copper_beets,
                                    'about': 'Electric Copper quite simply produce chart-topper after chart-topper.',
                                    'views': 1200,
                                    'owner': 'ross'},
                'The Execs': {'beets': exec_beets,
                              'about': 'Two Hollywood Executives who are constantly stargazing '
                                       'to bring you the brightest talent.',
                              'views': 200,
                              'owner': 'ross'}}



    #The code below goes through the personas dictionary and adds each persona
    #then the related tracks for each persona
    for username, user_data in users.items():
        user = add_user(username, user_data['email'], user_data['password'])
        user_profile = add_user_profile(user)
        user_profile.save()
        for persona, persona_data in personas.items():
            p = add_persona(persona, user_profile, persona_data['about'], persona_data['views'])
            for b in persona_data['beets']:
                add_beet(p, b['name'], b['about'], b['sound_file'])

    #print out the personas we have added
    for p in Persona.objects.all():
        for b in Beet.objects.filter(persona=p):
            print(f'- {p}: {b}')

def add_user(username, email, password):
    u = User.objects.get_or_create(username=username, email=email)[0]
    u.set_password(password)
    u.save()
    return u


def add_user_profile(user):
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    user_profile.save()
    return user_profile


def add_persona(name, owner, about, views):
    p = Persona.objects.get_or_create(name=name, owner = owner)[0]
    p.views = views
    p.about = about
    p.save()
    return p


def add_beet(persona, name, about, sound,plays=0):
    b = Beet.objects.get_or_create(persona=persona, name=name)[0]
    b.about = about
    b.sound_file = sound
    b.plays = plays
    b.save()
    return b





if __name__ == '__main__':
    print('Starting beets population script...')
    populate()