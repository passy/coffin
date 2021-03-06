"""Replacement for ``django.template.loader`` that uses Jinja 2.

The module provides a generic way to load templates from an arbitrary
backend storage (e.g. filesystem, database).
"""

from coffin.template import Template as CoffinTemplate
from coffin.common import env
from jinja2 import TemplateNotFound
from django.template.loader import BaseLoader
from django.template import TemplateDoesNotExist
from django.conf import settings


def find_template_source(name, dirs=None):
    # This is Django's most basic loading function through which
    # all template retrievals go. Not sure if Jinja 2 publishes
    # an equivalent, but no matter, it mostly for internal use
    # anyway - developers will want to start with
    # ``get_template()`` or ``get_template_from_string`` anyway.
    raise NotImplementedError()


def get_template(template_name):
    # Jinja will handle this for us, and env also initializes
    # the loader backends the first time it is called.
    from coffin.common import env
    return env.get_template(template_name)


def get_template_from_string(source):
    """
    Does not support then ``name`` and ``origin`` parameters from
    the Django version.
    """
    from coffin.common import env
    return env.from_string(source)


def render_to_string(template_name, dictionary=None, context_instance=None):
    """Loads the given ``template_name`` and renders it with the given
    dictionary as context. The ``template_name`` may be a string to load
    a single template using ``get_template``, or it may be a tuple to use
    ``select_template`` to find one of the templates in the list.

    ``dictionary`` may also be Django ``Context`` object.

    Returns a string.
    """
    dictionary = dictionary or {}
    if isinstance(template_name, (list, tuple)):
        template = select_template(template_name)
    else:
        template = get_template(template_name)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = dictionary
    return template.render(context_instance)


def select_template(template_name_list):
    "Given a list of template names, returns the first that can be loaded."
    for template_name in template_name_list:
        try:
            return get_template(template_name)
        except TemplateNotFound:
            continue
    # If we get here, none of the templates could be loaded
    raise TemplateNotFound(', '.join(template_name_list))


class Jinja2Loader(BaseLoader):
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        """Load a jinja2 file if it ends with the specified ending."""
        jinja2_ending = getattr(settings, 'JINJA2_FILE_EXTENSION', '.jinja2')

        if template_name.endswith(jinja2_ending):
            template = env.get_template(template_name)
            return template, template.filename
        else:
            raise TemplateDoesNotExist(template_name)
