from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .serializers import UserRegistrationSerializer, UserLoginSerializer, ChatSerializer
from .models import User, AuthToken, Chat 

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully", "tokens": 4000},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Create or retrieve token
            token = AuthToken.generate_token()
            AuthToken.objects.create(user=user, key=token)

            return Response(
                {
                    "message": "Login successful",
                    "token": token,
                    "tokens_left": user.tokens
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def authenticate_request(request):
    auth_header = request.headers.get('Authorization')
    token_key = None
    
    if auth_header and auth_header.startswith('Token '):
        token_key = auth_header.split(' ')[1]  # Get only the token string
    elif request.data.get('token'):  # fallback to body
        token_key = request.data.get('token')
    
    if not token_key:
        return None

    return AuthToken.objects.filter(key=token_key).first()

class ChatAPIView(APIView):
    def post(self, request):
        auth_token = authenticate_request(request)
        if not auth_token:
            return Response({"error": "Invalid or missing token"}, status=status.HTTP_401_UNAUTHORIZED)

        user = auth_token.user
        if user.tokens < 100:
            return Response({"error": "Insufficient tokens"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data['message']
            # Dummy AI response
            response_text = f"AI says: You said '{message}'"
            # Save to DB
            Chat.objects.create(user=user, message=message, response=response_text)
            # Deduct tokens
            user.tokens -= 100
            user.save()
            return Response({"message": message, "response": response_text, "tokens_left": user.tokens},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenBalanceAPIView(APIView):
    def get(self, request):
        auth_token = authenticate_request(request)
        if not auth_token:
            return Response({"error": "Invalid or missing token"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"tokens_left": auth_token.user.tokens}, status=status.HTTP_200_OK)
