from rest_framework import generics, status
from django.http.response import JsonResponse
from .models import Task
from .serializers import TaskSerializer


class TaskCreateView(generics.CreateAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            # Print the queryset and return a custom response
            return JsonResponse(
                {"detail": "Task created successfully", "data": response.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            # Print the queryset and return an error response
            print(e)
            return JsonResponse({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TaskReadOneView(generics.RetrieveAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            return response
        except self.queryset.model.DoesNotExist:
            return JsonResponse(
                {"detail": "Task Not found."}, status=status.HTTP_404_NOT_FOUND
            )


class TaskReadAllView(generics.ListAPIView):
    model = Task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return response
        except Exception as e:
            return JsonResponse(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            # You can remove the perform_update line and directly call serializer.save()
            serializer.save()
            response_data = {
                "detail": "Task updated successfully",
                "data": serializer.data,
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
        except self.queryset.model.DoesNotExist:
            print("does not")
            return JsonResponse(
                {"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(e)
            return JsonResponse({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    print()
    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return JsonResponse(
                {"detail": "Task deleted successfully", "data": response.data},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Task.DoesNotExist:
            return JsonResponse(
                {"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return JsonResponse(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
