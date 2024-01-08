from django.contrib import admin
from .models import Task,Tag
# Register your models here.


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    actions = ['delete_selected']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'due_date', 'status', 'timestamp')
    list_filter = ('status', 'due_date', 'tags')
    search_fields = ('title', 'description')

    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description', 'due_date', 'status', 'tags'),
        }),
        ('Timestamp Information', {
            'fields': ('timestamp',),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('timestamp',)

    def save_model(self, request, obj, form, change):
        # Additional validation checks before saving the model
        if change:
            # Disallow editing of timestamp
            obj.timestamp = Task.objects.get(pk=obj.pk).timestamp
        obj.save()
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags':
            # Limit the tags to those associated with the current task
            task_id = request.resolver_match.kwargs.get('object_id')
            if task_id:
                task = Task.objects.get(pk=task_id)
                kwargs['queryset'] = task.tags.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)
