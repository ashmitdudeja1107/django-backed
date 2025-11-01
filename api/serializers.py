from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Note
import os

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class TaskSerializer(serializers.ModelSerializer):
    notes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'completed', 
                  'created_at', 'updated_at', 'due_date', 'notes_count']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_notes_count(self, obj):
        return obj.notes.count()

class NoteSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    task_title = serializers.CharField(source='task.title', read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'task', 'task_title', 'file', 
                  'file_name', 'file_size', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_file_name(self, obj):
        if obj.file:
            return os.path.basename(obj.file.name)
        return None
    
    def get_file_size(self, obj):
        if obj.file:
            try:
                return obj.file.size
            except:
                return None
        return None
    
    def validate_file(self, value):
        if value:
            ext = os.path.splitext(value.name)[1].lower()
            valid_extensions = ['.pdf', '.txt', '.docx', '.doc']
            if ext not in valid_extensions:
                raise serializers.ValidationError(
                    f"Unsupported file extension. Allowed: {', '.join(valid_extensions)}"
                )
            if value.size > 10 * 1024 * 1024:  # 10MB limit
                raise serializers.ValidationError("File size must be less than 10MB")
        return value