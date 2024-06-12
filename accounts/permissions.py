from rest_framework.permissions import IsAuthenticated
from accounts.models import User


class IsAuthenticatedAndHaveAccessToTasksCreating(IsAuthenticated):
    message = "You don't have access to this endpoint"

    def has_permission(self, request, view):
        return (
                super().has_permission(request, view) and
                (
                        request.user.is_can_create_tasks or
                        request.user.role == User.Roles.customer
                )
        )


class IsAuthenticatedWorker(IsAuthenticated):
    message = "You don't have access to this endpoint"

    def has_permission(self, request, view):
        return (
                super().has_permission(request, view) and request.user.role == User.Roles.worker
        )

