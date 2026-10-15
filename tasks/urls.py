from django.urls import path
from .views import TaskDetailUpdateDeleteGenericView, TaskListCreateGenericView, CategoryListCreateView, CategoryDetailUpdateDeleteView

urlpatterns = [
     
    path("tasks/", TaskListCreateGenericView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailUpdateDeleteGenericView.as_view(), name="task-detail"),
    
    path("tasks/categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("tasks/categories/<int:pk>/", CategoryDetailUpdateDeleteView.as_view(), name="category-detail"),
] 