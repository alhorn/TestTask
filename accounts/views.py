from rest_framework import generics, status, mixins, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.models import User, ImageFile
from accounts.permissions import IsAuthenticatedWorker
from accounts.serializers import RegisterSerializer, LoginSerializer, UserSerializer, CreateUserSerializer, \
    ImageFileSerializer
from rest_framework.response import Response


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        self.kwargs['pk'] = self.request.user.id
        return super().get_object()

    def filter_queryset(self, queryset):
        if self.action == UserViewSet.list.__name__:
            if self.request.user.role == User.Roles.customer and self.request.user.is_have_access_to_workers:
                return queryset.filter(role=User.Roles.worker)
            elif self.request.user.role == User.Roles.customer and not self.request.user.is_have_access_to_workers:
                raise ValidationError('Permission denied')
            else:
                return queryset.filter(role=User.Roles.customer)
        return queryset


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedWorker,)
    serializer_class = CreateUserSerializer


class ImageUploadView(generics.CreateAPIView):
    serializer_class = ImageFileSerializer
    queryset = ImageFile.objects.all()
