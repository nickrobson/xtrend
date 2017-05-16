from django.views import View

class SingletonView(View):

    @classmethod
    def as_view(cls):
        instance = cls()
        print('Initialised', cls.__name__)
        def _helper(request, *args, **kwargs):
            return instance.dispatch(request, *args, **kwargs)
        return _helper
