from glob import glob
import mimetypes
import os
from xml.etree.ElementTree import Comment
from django.shortcuts import redirect, render
from django.shortcuts import render
from dashboard.doc_utils import create_doc
from dashboard.excel_utils import create_excel

from dashboard.models import WorkItem, Comment
from .utils import get_work_items, Details
from django.http import HttpResponse, HttpResponseRedirect
from dateutil import parser
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from zipfile import ZipFile

# Create your views here.


def home(request):
    work_items_list = WorkItem.objects.all()
    context = {
        'work_items_list': work_items_list
    }
    return render(request, 'dashboard/index.html', context)

@csrf_exempt
def create_webhook(request):
    work_items = get_work_items(
        Details.PERSONAL_ACCESS_TOKEN,
        Details.ORGANIZATION_URL,
        Details.QUERY_ID
    )

    for work_item_id, work_item in work_items.items():
        try:
            work_item_object = WorkItem.objects.get(id=work_item_id)
            if work_item_object.title != work_item.fields['System.Title']:
                work_item_object.title = work_item.fields['System.Title']
                work_item_object.save()
            if work_item_object.state != work_item.fields['System.State']:
                work_item_object.state = work_item.fields['System.State']
                work_item_object.save()
            if work_item_object.description != work_item.fields['System.Description']:
                work_item_object.description = work_item.fields['System.Description']
                work_item_object.save()

        except WorkItem.DoesNotExist:
            datetime_string = work_item.fields['System.CreatedDate']
            datetime_object = parser.isoparse(datetime_string)
            work_item_object = WorkItem.objects.get_or_create(
                id=work_item_id,
                title=work_item.fields['System.Title'],
                state=work_item.fields['System.State'],
                created=datetime_object,
                description=work_item.fields['System.Description'],
                owner=work_item.fields['System.CreatedBy']['displayName']
            )

    return home(request)    


def load_work_items(request):
    work_items = get_work_items(
        Details.PERSONAL_ACCESS_TOKEN,
        Details.ORGANIZATION_URL,
        Details.QUERY_ID
    )

    for work_item_id, work_item in work_items.items():
        try:
            work_item_object = WorkItem.objects.get(id=work_item_id)
            if work_item_object.title != work_item.fields['System.Title']:
                work_item_object.title = work_item.fields['System.Title']
                work_item_object.save()
            if work_item_object.state != work_item.fields['System.State']:
                work_item_object.state = work_item.fields['System.State']
                work_item_object.save()
            if work_item_object.description != work_item.fields['System.Description']:
                work_item_object.description = work_item.fields['System.Description']
                work_item_object.save()

        except WorkItem.DoesNotExist:
            datetime_string = work_item.fields['System.CreatedDate']
            datetime_object = parser.isoparse(datetime_string)
            work_item_object = WorkItem.objects.get_or_create(
                id=work_item_id,
                title=work_item.fields['System.Title'],
                state=work_item.fields['System.State'],
                created=datetime_object,
                description=work_item.fields['System.Description'],
                owner=work_item.fields['System.CreatedBy']['displayName']
            )

    return home(request)


def workitem(request, pk):
    work_item = WorkItem.objects.get(id=pk)
    work_item_comments = work_item.comment_set.all()
    context = {
        'work_item': work_item,
        'work_item_comments': work_item_comments
    }
    return render(request, 'dashboard/workitem.html', context)


@csrf_exempt
def create_comment(request, pk):
    work_item = WorkItem.objects.get(id=pk)
    if request.method == 'POST':
        comment = Comment.objects.create(
            work_item=work_item,
            body=request.POST.get('body')
        )

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def update_comment(request, pk):
    comment_query = Comment.objects.filter(id=pk)
    comment = comment_query.first()
    if request.method == 'POST':
        comment.body = request.POST.get('body')
        comment.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def delete_comment(request, pk):
    comment_query = Comment.objects.filter(id=pk)
    comment = comment_query.first()
    work_item = comment.work_item
    comment_query.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_in_DM(request, pk):
    work_item = WorkItem.objects.get(id=pk)
    if request.method == 'POST':
        comment = Comment.objects.create(
            work_item=work_item,
            body=request.POST.get('body')
        )

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_hours(request, pk):
    work_item = WorkItem.objects.get(id=pk)
    if request.method == 'POST':
        work_item.hours = int(request.POST.get('hours'))
        work_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_ad_work_package(request, pk):
    work_item = WorkItem.objects.get(id=pk)
    if request.method == 'POST':
        comment = Comment.objects.create(
            work_item=work_item,
            body=request.POST.get('body')
        )

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def create_IA(request, pk):
    work_item = WorkItem.objects.get(id=pk)
    doc_details = create_doc(work_item)

    if doc_details['file_path'] is not None:
        work_item.has_IA = True
        work_item.save()

        filename = doc_details['file_name']
        filepath = doc_details['file_path']
        if os.path.exists(filepath):
            # !!Important read as binary!!
            with open(filepath, 'rb') as worddoc:
                content = worddoc.read()
                response = HttpResponse(
                    content,
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
                response['Content-Disposition'] = f'attachment; filename={filename}'
                response['Content-Length'] = len(content)
                return response
        else:
            work_item_comments = work_item.comment_set.all()
            context = {
                'work_item': work_item,
                'work_item_comments': work_item_comments,
                'message_ia': doc_details['message']
            }
            return render(request, 'dashboard/workitem.html', context)

    else:
        work_item_comments = work_item.comment_set.all()
        context = {
            'work_item': work_item,
            'work_item_comments': work_item_comments,
            'message_ia': doc_details['message']
        }
        return render(request, 'dashboard/workitem.html', context)


def bulkcreate_IA(request):
    work_items = WorkItem.objects.filter(has_IA=False)
    created_IA_docs = []
    for work_item in work_items:
        doc_details = create_doc(work_item)
        if doc_details['file_path']:
            created_IA_docs.append(doc_details['file_path'])
            work_item.has_IA = True
            work_item.save()
        print(doc_details['file_path'])

    if len(created_IA_docs) == 0:
        bulk_message = 'All IA Docs have already been generated'
        work_items_list = WorkItem.objects.all()
        context = {
            'work_items_list': work_items_list,
            'bulk_message': bulk_message
        }
        return render(request, 'dashboard/index.html', context)

    path = os.path.join(os.getcwd(), 'docs\\IA')
    zip_name = os.path.join(path, 'IA_Documents.zip')
    with ZipFile(zip_name, 'w') as zip_object:
        for IA_doc in created_IA_docs:
            zip_object.write(IA_doc)

    if os.path.exists(zip_name):
        # !!Important read as binary!!
        with open(zip_name, 'rb') as zip_file:
            content = zip_file.read()
            response = HttpResponse(
                content,
                content_type='application/zip'
            )
            response['Content-Disposition'] = f'attachment; filename=IA_Documents.zip'
            response['Content-Length'] = len(content)
            return response
    else:
        bulk_message = "Couldn't download zip file"
        work_items_list = WorkItem.objects.all()
        context = {
            'work_items_list': work_items_list,
            'bulk_message': bulk_message
        }
        return render(request, 'dashboard/index.html', context)


def create_CR(request, pk):
    work_item = WorkItem.objects.get(id=pk)
    doc_details = create_excel(work_item)
    if doc_details['file_path'] is not None:
        work_item.has_CR = True
        work_item.save()

        filename = doc_details['file_name']
        filepath = doc_details['file_path']
        if os.path.exists(filepath):
            with open(filepath, 'rb') as worddoc: # !!Important read as binary!!
                content = worddoc.read()
                response = HttpResponse(
                    content,
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = f'attachment; filename={filename}'
                response['Content-Length'] = len(content)
                return response
        else:
            work_item_comments = work_item.comment_set.all()
            context = {
                'work_item': work_item,
                'work_item_comments': work_item_comments,
                'message_cr': doc_details['message']
            }
            return render(request, 'dashboard/workitem.html', context)

    else:
        work_item_comments = work_item.comment_set.all()
        context = {
            'work_item': work_item,
            'work_item_comments': work_item_comments,
            'message_cr': doc_details['message']
        }
        return render(request, 'dashboard/workitem.html', context)


def download_ia(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = BASE_DIR + '/docs/IA/'
    files = os.listdir(path)
    print(files)
    context = {
        'files': files
    }
    return render(request, 'dashboard/ia_docs.html', context)


def download_cr(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = BASE_DIR + '/docs/CR/'
    files = os.listdir(path)
    print(files)
    context = {
        'files': files
    }
    return render(request, 'dashboard/cr_docs.html', context)


def download_doc(request, filename):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = BASE_DIR + '/docs/IA/'
    file_path = os.path.join(path, filename)

    if os.path.exists(file_path):
        # !!Important read as binary!!
        if filename.split('.')[-1] == 'zip':
            content_type = 'application/zip'
        else:
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        with open(file_path, 'rb') as worddoc:
            content = worddoc.read()
            response = HttpResponse(
                content,
                content_type=content_type
            )
            response['Content-Disposition'] = f'attachment; filename={filename}'
            response['Content-Length'] = len(content)
            return response
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def download_excel(request, filename):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = BASE_DIR + '/docs/CR/'
    file_path = os.path.join(path, filename)
    print(file_path)
    if os.path.exists(file_path):
        # !!Important read as binary!!
        with open(file_path, 'rb') as worddoc:
            content = worddoc.read()
            response = HttpResponse(
                content,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename={filename}'
            response['Content-Length'] = len(content)
            return response
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def reset_IA(request):
    work_items = WorkItem.objects.filter(has_IA=True)
    for work_item in work_items:
        work_item.has_IA = False
        work_item.save()
    return HttpResponseRedirect("/")
