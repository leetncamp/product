from django import template
from django.utils.safestring import mark_safe
register = template.Library()

from pdb import set_trace as debug


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
