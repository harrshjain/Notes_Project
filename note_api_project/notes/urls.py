from django.urls import path
from .views import NoteListCreateView, NoteDetailView, NoteShareView, NoteSearchView, SignUpView, LoginView, NoteDeleteView, NoteUpdateView

urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('notes/<int:pk>/share/', NoteShareView.as_view(), name='note-share'),
    path('search/', NoteSearchView.as_view(), name='note-search'),
    path('notes/<int:pk>/', NoteDeleteView.as_view(), name='note-delete'),
    path('notes/<int:pk>/', NoteUpdateView.as_view(), name='note-update'),
]