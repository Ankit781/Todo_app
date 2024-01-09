import json
from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from todo.models import Task, Tag


class TaskModelTestCase(TestCase):
    def setUp(self):
        # Create a sample Task instance for testing
        # Set a due date one day from now
        self.due_date = timezone.now()
        task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            status="OPEN",
            due_date=self.due_date,
        )
        priority_tag, _ = Tag.objects.get_or_create(name="priority")
        task.tags.set([priority_tag])

    def test_task_model(self):
        task = Task.objects.get(title="Test Task")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.status, "OPEN")
        self.assertEqual(task.due_date, self.due_date)
        self.assertTrue(task.tags.filter(name="priority").exists())


class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.due_date = timezone.now()
        task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            status="OPEN",
            due_date=self.due_date,
        )
        priority_tag, _ = Tag.objects.get_or_create(name="priority")
        task.tags.set([priority_tag])
        self.priority_tag = priority_tag

    def test_create_task(self):
        data = {
            "title": "New Task",
            "description": "New Description",
            "status": "OPEN",
            "due_date": timezone.now(),
            "tags": [{"name": "priority"}],
        }
        response = self.client.post("/tasks/create", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_read_one_task(self):
        task = Task.objects.get(title="Test Task")
        response = self.client.get(f"/tasks/{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Task")
        self.assertEqual(response.data["description"], "Test Description")
        self.assertEqual(response.data["status"], "OPEN")
        self.assertTrue(response.data["due_date"])
        self.assertEqual(response.data["tags"], [{"id": 1, "name": "priority"}])

    def test_update_task(self):
        new_date = timezone.now()
        task = Task.objects.get(title="Test Task")
        data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "status": "DONE",
            "due_date": new_date,
            "tags": [{"name": "Imp"}],
        }
        response = self.client.put(f"/tasks/{task.id}/update/", data, format="json")
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=task.id).title, "Updated Task")
        self.assertEqual(Task.objects.get(id=task.id).status, "DONE")
        self.assertTrue(response_data["data"]["due_date"])
        self.assertEqual(
            response_data["data"]["tags"],
            [{"id": 1, "name": "priority"}, {"id": 2, "name": "Imp"}],
        )

    def test_read_all_tasks(self):
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task(self):
        task = Task.objects.get(title="Test Task")
        response = self.client.delete(f"/tasks/{task.id}/delete/")
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
