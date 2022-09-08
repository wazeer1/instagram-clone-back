import json

from django.contrib.auth.decorators import user_passes_test
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from main.models import Mode


def group_required(group_names):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs) :
            if request.user.is_authenticated:
                if not bool(request.user.groups.filter(name__in=group_names)) | request.user.is_superuser:
                    if request.is_ajax():
                        response_data = {}
                        response_data['status'] = 'false'
                        response_data['stable'] = 'true'
                        response_data['title'] = 'Permission Denied'
                        response_data['message'] = "You have no permission to do this action."
                        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                    else:
                        context = {
                            "title" : "Permission Denied"
                        }
                        return HttpResponse('<h1>Permission Denied</h1>')

            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper


def check_mode(function):
    def wrap(request, *args, **kwargs):
        mode, created = Mode.objects.get_or_create(id=1)
        readonly = mode.readonly
        maintenance = mode.maintenance
        down = mode.down

        if down:
            if request.is_ajax():
                response_data = {}
                response_data['status'] = 'false'
                response_data['message'] = "Application currently down. Please try again later."
                response_data['static_message'] = "true"
                return HttpResponse(json.dumps(response_data), content_type='application/javascript')
            else:
                return HttpResponseRedirect(reverse('api_v1_general:down'))
        elif readonly:
            if request.is_ajax():
                response_data = {}
                response_data['status'] = 'false'
                response_data['message'] = "Application now readonly mode. please try again later."
                response_data['static_message'] = "true"
                return HttpResponse(json.dumps(response_data), content_type='application/javascript')
            else:
                return HttpResponseRedirect(reverse('api_v1_general:read_only'))

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
