from xml.etree.ElementTree import Comment
from django.shortcuts import render
from django.shortcuts import render
from dashboard.doc_utils import create_doc
from dashboard.excel_utils import create_excel

from dashboard.models import WorkItem, Comment
from .utils import get_work_items, Details

from dateutil import parser
# Create your views here.


def home(request):
    work_items_list = WorkItem.objects.all()
    context = {
        'work_items_list': work_items_list,
    }
    return render(request, 'dashboard/index.html', context)


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


def create_comment(request, pk):
    work_item = WorkItem.objects.get(id=pk)
    if request.method == 'POST':
        comment = Comment.objects.create(
            work_item=work_item,
            body=request.POST.get('body')
        )

    return workitem(request, pk)


def update_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    work_item = comment.work_item
    if request.method == 'POST':
        comment.body = request.POST.get('body')
        comment.save()

    return workitem(request, work_item.id)


def delete_comment(request, pk):
    comment_query = Comment.objects.filter(id=pk)
    comment = comment_query.first()
    work_item = comment.work_item
    comment_query.delete()
    return workitem(request, work_item.id)



def create_IA(request, pk):
    work_item = WorkItem.objects.get(id=pk)
    work_item_comments = work_item.comment_set.all()
    message = create_doc(work_item)
    if message:
        work_item.has_IA = True
        work_item.save()
    print(message)
    context = {
        'work_item': work_item,
        'work_item_comments': work_item_comments,
        'message_ia': message
    }
    return render(request, 'dashboard/workitem.html', context)


def bulkcreate_IA(request):
    work_items = WorkItem.objects.filter(has_IA=False)
    for work_item in work_items:
        message = create_doc(work_item)
        if message:
            work_item.has_IA = True
            work_item.save()
        print(message)

    return home(request)


def create_CR(request, pk):
    work_item = WorkItem.objects.get(id=pk)
    work_item_comments = work_item.comment_set.all()
    message = create_excel(work_item)
    if message:
        work_item.has_CR = True
        work_item.save()
    print(message)
    context = {
        'work_item': work_item,
        'work_item_comments': work_item_comments,
        'message_cr': message
    }
    return render(request, 'dashboard/workitem.html', context)
