from profiles.models import Profile

def get_profile(user):
    try:
        return Profile.all().filter("user = ", user)[0]
    except IndexError:
        profile = Profile(user=user, notification=5)
        profile.save()
        return profile