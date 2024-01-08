from django.http.response import JsonResponse
from rest_framework import generics, status
from .models import Task
from .serializers import TaskSerializer
from django.forms.models import model_to_dict

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return model_to_dict(response)
        except Exception as e:
            return JsonResponse({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TaskReadOneView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            return response
        except Task.DoesNotExist:
            return JsonResponse({'detail': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'detail': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TaskReadAllView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return response
        except Exception as e:
            return JsonResponse({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TaskUpdateView(generics.UpdateAPIView):
    print("IN FUNCTION")
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    print("QUERYSET:")
    print(queryset)
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return response
        except Exception as e:
            return JsonResponse({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return JsonResponse({'detail': 'Task deleted successfully', 'data': TaskSerializer.data}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return JsonResponse({'detail': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
