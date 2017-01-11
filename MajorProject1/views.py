from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from MajorProject1.forms import ParentRegistrationForm


def register_user(request):
    if request.method=='POST':
        form = ParentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    args = {}
    args.update(csrf(request))
    args['form'] = ParentRegistrationForm()
    print args
    return render(request, 'registration/register.html', args)