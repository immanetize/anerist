# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1426432301.19959
_enable_loop = True
_template_filename = u'/usr/lib/python2.7/site-packages/nikola/data/themes/base/templates/crumbs.tmpl'
_template_uri = u'crumbs.tmpl'
_source_encoding = 'utf-8'
_exports = ['bar']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bar(context,crumbs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n')
        if crumbs:
            __M_writer(u'<nav class="breadcrumbs">\n<ul class="breadcrumb">\n')
            for link, text in crumbs:
                __M_writer(u'        <li><a href="')
                __M_writer(unicode(link))
                __M_writer(u'">')
                __M_writer(unicode(text))
                __M_writer(u'</a></li>\n')
            __M_writer(u'</ul>\n</nav>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"32": 4, "33": 5, "34": 7, "35": 8, "36": 8, "37": 8, "38": 8, "39": 8, "40": 10, "46": 40, "15": 0, "20": 2, "21": 13, "27": 3, "31": 3}, "uri": "crumbs.tmpl", "filename": "/usr/lib/python2.7/site-packages/nikola/data/themes/base/templates/crumbs.tmpl"}
__M_END_METADATA
"""
