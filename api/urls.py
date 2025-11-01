from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, NoteViewSet, signup, login, logout, user_profile

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    path('auth/profile/', user_profile, name='profile'),
    path('', include(router.urls)),
]