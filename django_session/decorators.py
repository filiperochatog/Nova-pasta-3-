# meuapp/decorators.py
from functools import wraps
from django.shortcuts import redirect

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('logado'):
            return redirect('/auth/login/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
