from django.urls import path

from .views import TextCreateView, TextDetailView, TextUpdateView, text_delete_view, download_txt, \
    UploadFormView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('new/', TextCreateView.as_view(), name='txt-create'),
    path('<int:pk>/', TextDetailView.as_view(), name='txt-detail'),
    path('change/<int:pk>', TextUpdateView.as_view(), name='txt-update'),
    path('delete/<int:pk>', text_delete_view, name='txt-delete'),
    path('download/<int:pk>', download_txt, name='txt-download'),
    path('upload/', UploadFormView.as_view(), name='txt-upload')
]
