import jwt
from django.http import JsonResponse

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed before view is called

        if request.path != "/backend/login" and request.path != "/backend/register" and request.path != "/backend/logout":

            token = request.COOKIES.get('jwt')

            if not token:
                msg = ("Unauthenticated!")
                return JsonResponse(data=msg, status=403, safe=False)

            try:
                payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            except jwt.ExpiredSignatureError:
                # raise AuthenticationFailed('Unauthenticated!')
                msg = ("Unauthenticated!")
                return JsonResponse(data=msg, status=403, safe=False)

        response = self.get_response(request)

        # Code to be executed after view is called

        return response