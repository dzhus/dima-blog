# coding: utf-8
import time, datetime

from django import forms
from django.template import loader, RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import ObjectPaginator, InvalidPage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.comments.models import FreeComment, Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

from blog.models import Entry, Tag
import settings

import captcha
from md5 import md5 as md5hash
from random import shuffle

def entry_list(request, paginate_by=5, page=-1,
        allow_empty=True, template_name="entry_list.xhtml", template_loader=loader,
        extra_context=None, template_object_name='entry', mimetype=None,
        tag=None, search_string=None):
 
    if extra_context is None: extra_context = {}
    
    try:
        if tag:
            queryset = Tag.objects.get(value=tag).entry_set.all()
        else:
            queryset = Entry.objects.all()
        queryset = queryset._clone()
    except:
        queryset = None

    # Hide private entries
    if not request.user.is_authenticated():
        queryset = queryset.filter(private=0)

    if paginate_by and queryset is not None:
        paginator = ObjectPaginator(queryset, paginate_by)
        if page == -1:
            page = request.GET.get('page', paginator.pages)
        try:
            page = int(page)
            object_list = paginator.get_page(paginator.pages - page)
        except (InvalidPage, ValueError):
            if page == paginator.pages and allow_empty:
                object_list = []
            else:
                raise Http404
        c = RequestContext(request, {
            '%s_list' % template_object_name: object_list,
            'is_paginated': paginator.pages > 1,
            'results_per_page': paginate_by,
            'has_next': paginator.has_next_page(page - 1),
            'has_previous': paginator.has_previous_page(page - 1),
            'page': page,
            'next': page + 1,
            'previous': page - 1,
            'pages': paginator.pages,
            'hits' : paginator.hits,
            'tag' : tag,
            'search_string' : search_string,
            'current_date' : datetime.datetime.now()
            })
    else:
        c = RequestContext(request, {
            '%s_list' % template_object_name: queryset,
            'is_paginated': False,
            'current_year' : time.strftime("%Y")
            })
        if not allow_empty and len(queryset) == 0:
            raise Http404
    print page
    if not template_name:
        model = queryset.model
        template_name = "%s/%s_list.html" % (model._meta.app_label, model._meta.object_name.lower())

    t = template_loader.get_template(template_name)
    return HttpResponse(t.render(c), mimetype=mimetype)

def entry_detail(request, entry_id=None, entry_slug=None,
                 template_name="entry_detail.xhtml"):

    try:
        if entry_slug:
            EntryObject = Entry.objects.get(slug=entry_slug)
        else:
            EntryObject = Entry.objects.get(pk=entry_id)
    except ObjectDoesNotExist:
        raise Http404
        
    # Check if current user has right to view this item
    if EntryObject.private and not request.user.is_authenticated():
        raise Http404

    # @todo DRY VIOLATION follows

    try:
        if request.user.is_authenticated():
            prev_entry = EntryObject.get_previous_by_add_date()
        else:
            prev_entry = EntryObject.get_previous_by_add_date(private=0)
    except:
        prev_entry = None

    
    try:
        if request.user.is_authenticated():
            next_entry = EntryObject.get_next_by_add_date()
        else:
            next_entry = EntryObject.get_next_by_add_date(private=0)
    except:
        next_entry = None

    

    # Get content-type for entries (to use in FreeComment)
    EntryContent = ContentType.objects.get_for_model(Entry).id

    # All comments for this entry
    comments = FreeComment.objects.filter(object_id=EntryObject.id, content_type=EntryContent).order_by('submit_date') 

    # Manipulator for adding comments
    comment_manipulator = FreeComment.AddManipulator()

    message = ""
    error = ""

    if not request.POST:
        if request.GET and request.GET['delete_comment']:
            # Deleting comment?
            try:
                comment_to_delete = FreeComment.objects.get(content_type=EntryContent, pk=request.GET['delete_comment'])
                # Check for superuser and entry id matching
                if request.user.is_authenticated() and request.user.is_superuser and comment_to_delete.object_id == EntryObject.id:
                    comment_to_delete.delete()
                    # Decrease comment count for related Entry
                    EntryObject.comments = int(EntryObject.comments) - 1 
                    EntryObject.save()
                    message = u"Комментарий удалён."
                else:
                    message = u"Попытка взлома!"
            except ObjectDoesNotExist:
                # Error if attempted to delete non-existing comment
                error = u"Объект не найден!"

        validation_errors = new_data = {}
    else:
        # Posting a new comment?
        new_data = request.POST.copy()

        comment_manipulator.do_html2python(new_data)

        # Fill service data
        new_data['ip_address']          = request.META['REMOTE_ADDR']
        new_data['object_id']           = str(EntryObject.id)
        new_data['content_type']        = EntryContent
        new_data['site']                = settings.SITE_ID
        new_data['approved']            = False

        validation_errors = comment_manipulator.get_validation_errors(new_data)

        if not validation_errors:
            # Flood control
            last_commented_time = request.session.get("last_comment", 0)
            if time.time() - last_commented_time < 60.0:
                # Some bulk non-false thing
                error = "Можно отправлять не более одного комментария в минуту."
            else:
                # CAPTCHA
                if not md5hash(request.POST['captcha_result']).hexdigest() == request.POST['captcha_hash']:
                    error = "Не удалось идентифицировать форму жизни."
                else:
                    # Save comment, everything's ok!
                    comment = comment_manipulator.save(new_data)
                    # Put a session thingie to avoid spam
                    request.session['last_comment'] = time.time()
                    # Increase comment count for related Entry
                    if EntryObject.comments is None:
                        EntryObject.comments = 1
                    else:
                        EntryObject.comments = int(EntryObject.comments) + 1 
                    EntryObject.save()
                    # Set a message
                    message = "Комментарий добавлен."
                    # Make sure clear form appears
                    new_data = {}
        else:
            error = "Обнаружены ошибки в заполнении формы."

    comment_form = forms.FormWrapper(comment_manipulator, new_data, validation_errors)

    # Show entry page at last :)
    context = { 
        'entry' : EntryObject,
        'prev_entry' : prev_entry,
        'next_entry' : next_entry,
        'comment_form' : comment_form, 
        'captcha' : captcha.Captcha(),
        'comments' : comments, 
        'message' : message,
        'error' : error,
        'current_year' : time.strftime("%Y")
        }
    context = RequestContext(request, context) 
    return render_to_response(template_name, context)

def tag_list(request, queryset, stages=5, sort=True,
             allow_empty=True, template_name="entry_list.xhtml", 
             template_loader=loader):

    max_count = min_count = 0
    tag_list = []

    # sort tags by occurence
    for tag in list(queryset.all()):
        count = tag.entry_set.count()
        tag_list.append({'tag' : tag, 'count' : count})
        if count > max_count:
            max_count = count
        if count < min_count:
            min_count = count
    
    if sort:
        tag_list.sort(key=lambda t: t['count'], reverse=True)
    else:
        shuffle(tag_list)

    def get_weight(count, max, min):
        return int(((count - min) * 1. / (max - min)) / ((stages + 1) * 1. / (max - min))) + 1

    for tag in tag_list:
        tag['weight'] = get_weight(tag['count'], 
                                   max_count, min_count)

    context = {
        'tag_list' : tag_list,
        'max_count' : max_count,
        'min_count' : min_count
        }    

    context = RequestContext(request, context) 
    return render_to_response(template_name, context)

