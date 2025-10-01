from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser

class JWTAuthMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate GraphQL requests using the JWT token.
    """

    def process_request(self, request):
        # Extract the token from the Authorization header
        auth = JWTAuthentication()
        header = auth.get_header(request)
        if header is None:
            request.user = getattr(request, "user", AnonymousUser())
            return
        try:
           validated_token = auth.get_validated_token(auth.get_raw_token(header))
           user = auth.get_user(validated_token)
           request.user = user
        except Exception:
            # If token invalid, leave as anonymous (resolvers should enforce auth)
             request.user = getattr(request, "user", AnonymousUser())