from authenticate.models import *



def identify_farmer(user):
    profile= Profile.objects.get(user_m=user)
    if profile.is_framer:
        return True
    else:
        return False