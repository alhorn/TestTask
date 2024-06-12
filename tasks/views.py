from rest_framework import mixins, viewsets, generics, status
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from accounts.permissions import IsAuthenticatedAndHaveAccessToTasksCreating, IsAuthenticatedWorker
from tasks.models import Task
from tasks.serializers import TaskSerializer, AssignTaskSerializer, MarkAsCompletedSerializer
from django.db.models import Q
from rest_framework.response import Response


class TasksView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Task.objects.order_by('-id')
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.action in [TasksView.create.__name__, TasksView.update.__name__]:
            return [IsAuthenticatedAndHaveAccessToTasksCreating()]
        return super().get_permissions()

    def filter_queryset(self, queryset):
        user = self.request.user
        if user.role == User.Roles.customer:
            return queryset.filter(customer=user)
        else:
            if not user.is_have_access_to_tasks:
                queryset = queryset.filter(Q(worker=user) | Q(worker=None))

        return queryset


class UpdateTasksView(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Task.objects.order_by('-id')
    permission_classes = (IsAuthenticatedWorker,)
    serializer_class = TaskSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(worker=self.request.user)


class ManageTaskView(viewsets.GenericViewSet):
    queryset = Task.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action == ManageTaskView.assign.__name__:
            return AssignTaskSerializer(*args, **kwargs, context=self.get_serializer_context())
        else:
            return MarkAsCompletedSerializer(*args, **kwargs, context=self.get_serializer_context())

    serializer_class = AssignTaskSerializer
    permission_classes = [IsAuthenticatedWorker]

    def assign(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)

    def mark_as_completed(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
