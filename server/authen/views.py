from rest_framework.views import APIView
from rest_framework.response import Response
import logging
from .serializers import UserLoginSerializer, UserRegistrationSerializer
from .utils import get_token
from .models import User

# Create your views here.

logger = logging.getLogger(__name__)


class Login(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        if request.method != "POST":
            return

        data = request.data
        serializer = UserLoginSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            email = validated_data.get("email")
            user = User.objects.get(email=email)
            response = get_token(user)
            return Response(response, status=200)
        else:
            errors = serializer.errors
            return Response({"errors": errors}, status=400)


class Register(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        if request.method != "POST":
            return

        data = request.data
        serializer = UserRegistrationSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            serializer.create(validated_data)
            return Response({"message": "Successfully registered user!"}, status=201)
        else:
            errors = serializer.errors
            return Response({"errors": errors}, status=400)
