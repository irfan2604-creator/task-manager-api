from rest_framework import generics
from .models import Task , Category
from .serializers import TaskSerializer , CategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
    
#generic class-based views for Task API endpoints

class TaskListCreateGenericView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    parser_classes = [MultiPartParser,FormParser,JSONParser]

    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        category = self.request.query_params.get('category')
        due_before = self.request.query_params.get('due_before')
        due_after = self.request.query_params.get('due_after')
        
        if due_before:
            queryset = queryset.filter(due_date__lte=due_before)
        if due_after:
            queryset = queryset.filter(due_date__gte=due_after)
        if status:
            queryset = queryset.filter(status=status)
        if priority :
            queryset = queryset.filter(priority=priority)
        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetailUpdateDeleteGenericView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    serializer_class = TaskSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user) 