import babel
import dateutil.parser

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

def setup(app):
    @app.template_filter('type')
    def type_filter(value):
        return type(value).__name__

    @app.template_filter('datetime')
    def datetime_filter(value, format):
        return format_datetime(value, format)
