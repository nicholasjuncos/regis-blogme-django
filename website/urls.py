"""training URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views import defaults as default_views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import status
from rest_framework.response import Response
import requests


from . import router


def get_auth_token():
    credentials = {
        'username': 'njuncos@genesisrg.com',
        'password': 'evidscienceplatform'
    }
    auth = requests.post('http://localhost:5000/login/', json=credentials)
    try:
        print('hello')
        print(auth)
        if auth.status_code == 200:
            auth_json = auth.json()
            if 'token' in auth_json:
                return auth_json["token"]
    except:
        pass
    return False


def make_request(request_type, route, data=None):
    if request_type == 'POST':
        request_method = requests.post
    else:
        request_method = requests.get
    token = get_auth_token()
    if not token:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    headers = {"Authorization": "Bearer " + token}
    response = request_method(f'http://localhost:5000/{route}', headers=headers, json=data)
    try:
        return response.json()
    except:
        return None


def health_check(request):
    return Response(status=status.HTTP_200_OK)

urlpatterns = [
                  # path('', TemplateView.as_view(template_name='home.html'), name='home'),
                  path('admin/', admin.site.urls),
                  # authentication
                  # path('accounts/', include('allauth.urls')),
                  path('api/', include(router)),
                  path('api/auth-token/', obtain_auth_token, name='obtain-auth-token'),
                  path('api/auth/', include('dj_rest_auth.urls')),
                  path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
                  path('api/health-check/', health_check),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            '400/',
            default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')},
        ),
        path(
            '403/',
            default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')},
        ),
        path(
            '404/',
            default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')},
        ),
        path('500/', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
