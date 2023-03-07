from openedx.core.lib.api.view_utils import view_auth_classes
from rest_framework.views import APIView
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework.authentication import SessionAuthentication
from openedx.core.lib.api.authentication import BearerAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from openedx.core.djangoapps.oauth_dispatch.jwt import create_jwt_for_user
from edx_rest_api_client.auth import SuppliedJwtAuth
from django.contrib.auth.models import User
from .models import UserGreeting
import requests
from django.urls import reverse
from django.conf import settings
import logging
LOGGER = logging.getLogger(__name__)

@view_auth_classes(is_user=False, is_authenticated=True)
class ClientGreetingAPI(APIView):
        
    def get(self, request):
        greeting = self.request.query_params.get('greeting')
        if not greeting:
            raise ParseError('Greeting word must be specified')
        LOGGER.info('the user ' + str(request.user) + ' submit greeting ' + greeting)
        UserGreeting.objects.create(user=request.user, greeting_word=greeting)
        if greeting == 'hellow':
            user = User.objects.get(id=request.user.id)
            jwt = create_jwt_for_user(user)
            client = requests.Session()
            client.auth = SuppliedJwtAuth(jwt)
            url = settings.LMS_ROOT_URL + reverse('test_api:greet')
            response = client.get(url , params={'greeting':'goodbye'})
            return Response({
                "message": 'done',
            })
        

        return Response({
                "message": 'done',

            })

