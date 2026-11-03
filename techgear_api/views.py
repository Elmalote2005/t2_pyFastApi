from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from .serializers import UsuarioSerializer, CustomTokenSerializer


class RegistroUsuario(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"mensaje": "Usuario creado exitosamente"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class Login(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class CerrarSesion(APIView):
    @csrf_exempt
    def post(self, request):
        logout(request)
        return Response(
            {"mensaje": "Sesión cerrada correctamente"},
            status=status.HTTP_200_OK
        )