import jinja2
import flask

filters = flask.Blueprint('filters', __name__)

@jinja2.contextfilter
@filters.app_template_filter()
def field_has_errors(context, value):
    if len(value) > 0:
        return 'visible-error'
    return ""
    



