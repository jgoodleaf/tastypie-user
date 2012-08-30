#coding:utf8
import datetime
import threading
from django.template.loader import get_template,TemplateDoesNotExist
from django.template import Context
from django.core.mail import EmailMessage
import importlib
from django.conf import settings


TASTYPIE_USER_TEMPLATE_FOLDER = getattr(settings,'TASTYPIE_USER_TEMPLATE_FOLDER', 'tastypie-user')


try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now

def lazy_import(name):
    if not name or type(name) not in (str,unicode):
        return name
    else:
        module_name, model_name = name.rsplit('.',1)
        module = importlib.import_module(module_name)
        try:
            return getattr(module, model_name)
        except AttributeError:
            return importlib.import_module(name)


def send_email(subject, message, from_email, to_email, content_subtype='html'):#just one mail not a addressed list
    msg = EmailMessage(subject, message, from_email, [to_email])
    msg.content_subtype = content_subtype
    print subject,message

    thread_job = threading.Thread(target=msg.send, args=())
    thread_job.setDaemon(True)
    thread_job.start()


def load_email_content(action_type, ctx_dict):
    templates_folder = '%s/emails'%TASTYPIE_USER_TEMPLATE_FOLDER
    try:
        template = get_template('%s/%s.txt'%(templates_folder, action_type))
        content_subtype = 'plain'
    except TemplateDoesNotExist:
        template = get_template('%s/%s.html'%(templates_folder, action_type))
        content_subtype = 'html'

    try:
        subject = get_template('%s/%s_subject.txt'%(templates_folder,action_type)).render(Context(ctx_dict))
    except:
        subject = action_type.replace('_',' ').title()
    message = template.render(Context(ctx_dict))

    return subject, message, content_subtype