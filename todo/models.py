from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("WORKING", "Working"),
        ("DONE", "Done"),
        ("OVERDUE", "Overdue"),
    ]

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=1000, blank=False)
    due_date = models.DateTimeField(editable=True, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, through="todo_task_tags")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=False)

    def __str__(self):
        return self.title


class todo_task_tags(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE)


# removes the unnecessary tags if no further task is aasociated with it
@receiver(pre_delete, sender=Task)
def delete_tags(sender, instance, **kwargs):
    task_tag_id = Task.objects.filter(pk=instance.id)
    associated_tag = todo_task_tags.objects.filter(task__id=task_tag_id[0].id)
    all_associated_tags = todo_task_tags.objects.all()
    for all_associated_tag in all_associated_tags:
        if associated_tag[0].tags.id == all_associated_tag.tags_id:
            if todo_task_tags.objects.filter(tags=associated_tag[0].tags).count() == 1:
                tag = Tag.objects.filter(pk=associated_tag[0].tags.id)
                tag.delete()
                break
