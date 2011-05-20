from datetime import datetime, timedelta
import operator

from django import forms
from django.db.models import Q

from app.forms import Form, ModelForm
from app.utils import memoize, safe_int

from projects.models import ProjectURL
from error.models import Error, Group

read_choices = (("", "All"), ("True", 'Read only'), ("False", 'Unread only'))
priority_choices = [ (r, r) for r in range(1, 11)]
priority_choices.insert(0, ("", "All"))

status_choices = ['500', '404', '100', '101', '102', '200', '201', '202', '203',
'204', '205', '206', '207', '226', '300', '301', '302', '303', '304',
'305', '307', '400', '401', '402', '403', '405', '406', '407',
'408', '409', '410', '411', '412', '413', '414', '415', '416', '417',
'422', '423', '424', '426', '501', '502', '503', '504', '505',
'507', '510']
status_choices = [ (r, r) for r in status_choices ]
status_choices.insert(0, ("", "All"))


class Filter(Form):
    """ Base for the filters """
    inequality = ""

    def as_query(self, object):
        args = []
        for k, v in self.cleaned_data.items():
            if not v:
                continue

            lookup = getattr(self, "handle_%s" % k, None)
            if lookup:
                args.append(lookup(v))
            else:
                args.append(Q(**{k:v}))

        if args:
            return object.objects.filter(reduce(operator.and_, args))
        return object.objects.all()

    def clean(self):
        data = {}
        for k, v in self.cleaned_data.items():
            if not v: continue
            data[k] = v

        return data


@memoize(prefix='get-project-urls', time=120)
def get_project_urls():
    urls = [('', '')]
    urls.extend([k.pk, k.url] for k in ProjectURL.objects.all())
    return urls


class GroupForm(Filter):
    project_url = forms.ChoiceField(choices=[],
                                    widget=forms.Select, required=False)

    def __init__(self, *args, **kw):
        super(GroupForm, self).__init__(*args, **kw)
        self.fields['project_url'].choices = get_project_urls()

    def as_query(self):
        return super(GroupForm, self).as_query(Group)

    def handle_project_url(self, value):
        return Q(project_url=value)


@memoize(prefix='get-domains', time=120)
def get_domains():
    domains = [('','')]
    domains.extend([(d, d) for d in Error.objects.order_by().values_list('domain', flat=True).distinct()])
    return domains

period_choices = (['last_24', 'Last 24 hours'],
                  ['today', 'Today'],
                  ['yesterday', 'Yesterday'])

class GroupEditForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'count', 'timestamp']
        

class ErrorForm(Filter):
    priority = forms.ChoiceField(choices=priority_choices,
                                 widget=forms.Select, required=False)
    status = forms.ChoiceField(choices=status_choices,
                               widget=forms.Select, required=False)
    read = forms.ChoiceField(choices=read_choices,
                             widget=forms.Select, required=False)
    start = forms.DateField(required=False, label="Start date",
        widget=forms.DateInput(attrs={"class":"date",}))
    period = forms.ChoiceField(choices=period_choices,
                               widget=forms.Select, required=False)
    end = forms.DateField(required=False, label="End date",
        widget=forms.DateInput(attrs={"class":"date",}))
    query = forms.CharField(required=False, label="Path")
    domain = forms.ChoiceField(choices=[],
                               widget=forms.Select, required=False)
    uid = forms.CharField(required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.none(),
                                   widget=forms.Select, required=False)

    def __init__(self, *args, **kw):
        super(ErrorForm, self).__init__(*args, **kw)
        self.fields['group'].queryset = Group.objects.all()
        self.fields['domain'].choices = get_domains()

    def clean(self):
        data = {}
        for k, v in self.cleaned_data.items():
            if not v: continue
            data[k] = v

        return data

    def handle_period(self, period):
        if period == 'last_24':
           return Q(timestamp__gte=datetime.now() - timedelta(hours=24))
        elif period == 'today':
           return Q(timestamp__gte=datetime.today().date())
        elif period == 'yesterday':
           return Q(timestamp__gte=datetime.today().date() - timedelta(days=1),
                    timestamp__lt=datetime.today())
        else:
           raise NotImplementedError

    def handle_read(self, value):
        return Q(read={"False":False, "True":True}.get(value, None))

    def handle_start(self, value):
        return Q(timestamp__gte=value)

    def handle_end(self, value):
        return Q(timestamp__lte=value)

    def handle_priority(self, value):
        return Q(priority__lte=value)

    def as_query(self):
        return super(ErrorForm, self).as_query(Error)
