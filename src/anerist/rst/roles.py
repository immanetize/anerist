from docutils import nodes
from docutils.parsers.rst import roles

def rhbz_role(role, rawtext, text, lineno, inliner, options={}, content=[]):

    """ Creates an inline link to a ticket at bugzilla.redhat.com

        Usage:
            :RHBZ: 1072410           


    """
    def get_bug_summary(bug):
        # this might want to do something more interesting someday
        summary = "RHBZ#%s" % bug
        return summary

    try:
        bz_ticket = int(text)
        if bz_num <=0:
            raise ValueError
    except ValueError:
        msg = inliner.reporter.error(
                "Unknown or invalid bug: %s" % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    bz_url = "https://bugzilla.redhat.com/show_bug.cgi?id=%s" % bz_ticket
    bz_link = "<a href='%s' class='bzlink'>%s</a> " % (bz_url, summary)
    set_classes(options)
    node = nodes.reference(rawtext, "RHBZ " + bz_ticket, refuri=bz_utl, **options)
    return [node], []

roles.register_local_role('rhbz_role', rhbz_role)


