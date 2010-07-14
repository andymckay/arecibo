from django.contrib.auth.decorators import user_passes_test
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from appengine_django.auth.models import User
from app.paginator import Paginator, get_page

from users.forms import UserForm

@user_passes_test(lambda u: u.is_staff)
def user_list(request):
    queryset = User.all()
    # this number doesn't need to be high and its quite an expensive
    # page to generate
    paginated = Paginator(queryset, 10)
    page = get_page(request, paginated)
    return direct_to_template(request, "user_list.html", extra_context={
        "page": page,
        "nav": {"selected": "setup"}
        })

@user_passes_test(lambda u: u.is_staff)
def user_edit(request, pk):
    form = UserForm(request.POST or None, instance=User.get(pk))
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect(reverse("user-list"))
    return direct_to_template(request, "user_edit.html", extra_context={
        "form": form,
        "nav": {"selected": "users",},
    })

