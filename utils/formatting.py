import json

from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer


def pretty_json(json_data, truncate=None):
    """Function to display pretty version of our data"""

    # Convert the data to sorted, indented JSON
    response = json.dumps(json_data, sort_keys=True, indent=2)

    # Truncate the data. Alter as needed
    response = response[:truncate]

    # Get the Pygments formatter
    formatter = HtmlFormatter(style='colorful')

    # Highlight the data
    response = highlight(response, JsonLexer(), formatter)

    # Get the stylesheet
    style = "<style>" + formatter.get_style_defs() + "</style><br>"

    # Safe the output
    return mark_safe(style + response)
