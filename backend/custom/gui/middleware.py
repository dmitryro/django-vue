from django.contrib.auth import logout

class ForceLogoutMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated() and request.user.force_logout_date and \
           request.session['LAST_LOGIN_DATE'] < request.user.force_logout_date:
            logout(request)
