"""
Internal utils for search.
"""
import sys

if sys.version_info > (3, 0):
    from django.utils.encoding import force_str
else:
    from django.utils.encoding import force_text as force_str
from django.utils.html import strip_tags
from future.utils import string_types


def get_search_field_values(contentitem):
    """
    Extract the search fields from the model.
    """
    plugin = contentitem.plugin
    values = []
    for field_name in plugin.search_fields:
        value = getattr(contentitem, field_name)

        # Just assume all strings may contain HTML.
        # Not checking for just the PluginHtmlField here.
        if value and isinstance(value, string_types):
            value = get_cleaned_string(value)

        values.append(value)

    return values


def get_search_text(contentitem):
    bits = get_search_field_values(contentitem)
    return clean_join(u" ", bits)


def get_cleaned_string(data):
    """
    Cleanup a string/HTML output to consist of words only.
    """
    return strip_tags(force_str(data))


def clean_join(separator, iterable):
    """
    Filters out iterable to only join non empty items.
    """
    return separator.join(filter(None, iterable))


# def get_cleaned_bits(data):
#    return smart_split(get_cleaned_bits(data))
