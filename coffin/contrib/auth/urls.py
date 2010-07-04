import inspect

from django.contrib.auth import urls

exec inspect.getsource(urls)\
        .replace('django.contrib.auth.views', 'coffin.contrib.auth.views')
