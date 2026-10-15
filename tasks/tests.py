from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase
import tempfile
from .models import Task


class TaskAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!"
        )

        self.token = str(RefreshToken.for_user(self.user).access_token)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

    def test_authenticated_user_can_list_tasks(self):
        response = self.client.get("/api/tasks/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_list_tasks(self):
        self.client.credentials()

        response = self.client.get("/api/tasks/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_authenticated_user_can_create_task(self):
        response = self.client.post(
            "/api/tasks/",
            {
                "title": "Learn Django Testing",
                "description": "Practice automated API testing",
                "priority": "HIGH",
                "status": "PENDING",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().owner, self.user)

    def test_authenticated_user_can_retrieve_own_task(self):
        task = Task.objects.create(
            title="Learn Django Testing",
            description="Practice automated API testing",
            owner=self.user,
        )

        response = self.client.get(f"/api/tasks/{task.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], task.title)

    def test_authenticated_user_can_update_own_task(self):
        task = Task.objects.create(
            title="Learn Django Testing",
            description="Practice automated API testing",
            owner=self.user,
        )

        response = self.client.patch(
            f"/api/tasks/{task.id}/",
            {"priority": "HIGH"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task.refresh_from_db()
        self.assertEqual(task.priority, "HIGH")

    def test_authenticated_user_can_delete_own_task(self):
        task = Task.objects.create(
            title="Learn Django Testing",
            description="Practice automated API testing",
            owner=self.user,
        )

        response = self.client.delete(f"/api/tasks/{task.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())
        
    def test_user_cannot_retrieve_another_users_task(self):
        another_user = User.objects.create_user(
            username="anotheruser",
            password="TestPassword123!"
        )

        task = Task.objects.create(
            title="Another Users Task",
            description="This task belongs to another user",
            owner=another_user,
        )

        response = self.client.get(f"/api/tasks/{task.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_update_another_users_task(self):
        another_user = User.objects.create_user(
            username="anotheruser",
            password="TestPassword123!"
        )

        task = Task.objects.create(
            title="Another Users Task",
            description="This task belongs to another user",
            owner=another_user,
        )

        response = self.client.patch(
            f"/api/tasks/{task.id}/",
            {"title": "Hacked Task Title"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        task.refresh_from_db()
        self.assertEqual(task.title, "Another Users Task")

    def test_user_cannot_delete_another_users_task(self):
        another_user = User.objects.create_user(
            username="anotheruser",
            password="TestPassword123!"
        )

        task = Task.objects.create(
            title="Another Users Task",
            description="This task belongs to another user",
            owner=another_user,
        )

        response = self.client.delete(f"/api/tasks/{task.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(Task.objects.filter(id=task.id).exists())

    def test_authenticated_user_can_upload_task_attachment(self):
        with tempfile.TemporaryDirectory() as temp_media:
            with override_settings(MEDIA_ROOT=temp_media):
                uploaded_file = SimpleUploadedFile(
                    "task_notes.txt",
                    b"Complete the Django Task Manager project.",
                    content_type="text/plain",
                )

                response = self.client.post(
                    "/api/tasks/",
                    {
                        "title": "Complete Django Project",
                        "description": "Finish the portfolio project",
                        "priority": "HIGH",
                        "status": "PENDING",
                        "attachment": uploaded_file,
                    },
                    format="multipart",
                )

                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertTrue(response.data["attachment"])