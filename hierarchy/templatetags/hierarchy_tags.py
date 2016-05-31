from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
from django.template.loader import get_template
from django.utils.safestring import mark_safe
register = template.Library()
from django.conf import  settings
from pdb import set_trace as debug
import os


import logging
logging.basicConfig()
log = logging.getLogger(__name__)

from django.core.urlresolvers import reverse


#map bootstrap level to glyphicon
glyphicons = {"success":"check", "warning":"warning-sign", "primary":"asterisk", "danger":"warning-sign", "default":"info-sign", "info":"info-sign"}
#map django messaages level to bootstrap level
levels = {"debug":"default", "info":"info", "success":"success", "warning":"warning", "error":"danger"}

messageTemplate = u"""<div class="alert alert-{0} alert-dismissable">
          <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
          <h4><span class="glyphicon glyphicon-{1} text-large"> </span> <small>&nbsp; {2}</small></h4>
        </div>"""

@register.simple_tag()
def bootstrapalert(message):
    alertclass = levels[message.tags]
    glyphicon = glyphicons[alertclass]
    html = messageTemplate.format(alertclass, glyphicon, message.message)
    return(mark_safe(html))

@register.simple_tag()
def editable_document(htmlfilename):
    templatepath = os.path.join(settings.BASE_DIR, "hierarchy", "templates", "hierarchy", "editable", htmlfilename)
    try:
        html = open(templatepath, "rb").decode("utf-8")
    except IOError:
        html = u""
    id = slugify(htmlfilename)
    template = get_template("hierarchy/editable.html")
    renderedhtml = template.render(locals())
    safehtml = mark_safe(renderedhtml)
    return(safehtml)
