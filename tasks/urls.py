from django.urls import path
from src.custom_router import CustomRouter
from tasks.views import TasksView, ManageTaskView, UpdateTasksView

router = CustomRouter()

urlpatterns = [
    path('tasks/', TasksView.as_view({'get': 'list', 'post': 'create'}), name='tasks'),
    path('tasks/<int:pk>/', UpdateTasksView.as_view({'put': 'update'}), name='tasks'),
    path('tasks/assign/', ManageTaskView.as_view({'post': 'assign'}), name='tasks'),
    path('tasks/mark_as_completed/', ManageTaskView.as_view({'post': 'mark_as_completed'}), name='tasks'),
] + router.urls
