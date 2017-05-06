import threading

from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse

from InfoSystem.forms import DocumentForm, ResultsForm
from InfoSystem.models import Document, ExamInfo
from insert_info import insert_info
from insert_results import insert_results1, insert_results2


def display_links(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('admin:login'))
    return render(request, 'links.html')


def upload_info(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('admin:login'))
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_doc = Document(docfile=request.FILES['docfile'])
            new_doc.save()
            # book = xlrd.open_workbook(new_doc.docfile.name)
            sheets = int(form.cleaned_data['sheets'])
            start = int(form.cleaned_data['start'])-1
            # insert_info(new_doc, sheets, start)
            thread = threading.Thread(target=insert_info, args=(new_doc, sheets, start), kwargs={})
            thread.setDaemon(True)
            thread.start()
            return HttpResponseRedirect(reverse('links'))
    else:
        form = DocumentForm()

    return render(request, 'stud_par_info.html', {'form': form})

def upload_results(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('admin:login'))
    if request.method == 'POST':
        form = ResultsForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            ei = ExamInfo()
            ei.year_of_pursue = int(cd['year_of_pursue'])
            ei.year_of_pursue_roman = cd['year_of_pursue_roman']
            ei.month_of_year = cd['month_of_year']
            ei.year_of_calendar = int(cd['year_of_calendar'])
            ei.semester_roman = cd['semester_roman']
            ei.semester = int(cd['semester'])
            cd['is_supple'] = cd['is_supple'].strip()
            if cd['is_supple'] == '0':
                ei.supple = False
            else:
                ei.supple = True
            # ei.save()

            new_doc = Document(docfile=request.FILES['docfile'])
            new_doc.save()
            sheets = int(form.cleaned_data['sheets'])
            start = int(form.cleaned_data['start'])-1
            batch = int(form.cleaned_data['batch'])

            # insert_results(new_doc, ei, sheets, start, batch)
            # book = xlrd.open_workbook(new_doc.docfile.name)
            if batch == 0:
                insert_results = insert_results1
            else:
                insert_results = insert_results2
            thread = threading.Thread(target=insert_results, args=(new_doc, ei, sheets, start), kwargs={})
            thread.setDaemon(True)
            thread.start()
            return HttpResponseRedirect(reverse('links'))
    else:
        form = ResultsForm()

    return render(request, 'results_upload.html', {'form': form})