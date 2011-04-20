from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import logout as logout_user
from django.contrib.auth.views import login as login_view
from django.contrib.messages.api import info
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from app.paginator import Paginator, get_page
from app.utils import redirect

from users.forms import CreateForm, EditForm, LoginForm, PasswordForm


@user_passes_test(lambda u: u.is_staff)
def user_list(request):
    queryset = User.objects.all()
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
    form = EditForm(request.POST or None, instance=User.objects.get(pk=pk))
    if form.is_valid():
        form.save()
        info(request, 'User details changed.')
        return HttpResponseRedirect(reverse("user-list"))
    return direct_to_template(request, "user_edit.html", extra_context={
        "form": form,
        "nav": {"selected": "users",},
    })


def user_create(request):
    form = CreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        info(request, _('Account added, please wait for an admin to verify.'))
        return HttpResponseRedirect(reverse("index"))
    return direct_to_template(request, "user_create.html", extra_context={
        "form": form,
    })
 

@user_passes_test(lambda u: u.is_staff)
def user_password(request):
    form = PasswordForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        info(request, 'Password changed.')
        return HttpResponseRedirect(reverse("user-edit",
                                            args=[request.user.pk]))
    return direct_to_template(request, "user_password.html", extra_context={
        "form": form,
    })
    
    
def logout(request):
    logout_user(request)
    return redirect('index')


def login(request):
    return login_view(request, 'user_login.html', authentication_form=LoginForm)