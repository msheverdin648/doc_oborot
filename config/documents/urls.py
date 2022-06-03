from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('incoming/', views.DocumentsIncoming.as_view(), name='incoming'),
    path('outcoming/', views.DocumentsOutcoming.as_view(), name='outcoming'),
    path('add/', views.DocumetnsAdd.as_view(), name='add'),
    path('archive/', views.DocumentsArchive.as_view(), name='archive'),
    path('submit/<int:pk>/', views.DocumentsSubmit.as_view(), name='submit'),
    path('terminate/<int:pk>/', views.DocumentsTerminate.as_view(), name='terminate'),
    path('to_archive/<int:pk>/', views.DocumentsToArchive.as_view(), name='to_archive'),
    path('read/<int:pk>/', views.DocumentsRead.as_view(), name='read'),
    path('delete/<int:pk>/', views.DocumentsDelete.as_view(), name='delete'),
    path('filter/', views.DocumentsFilter.as_view(), name='filter'),
    path('archive_filter/', views.ArchiveFilter.as_view(), name='archive_filter'),
    path('description/', views.DescriptionView.as_view(), name='description'),
    path('sort/', views.DocumentsSort.as_view(), name='sort'),
    path('archive_sort/', views.ArchiveSort.as_view(), name='archive_sort'),
    path('report/', views.CreateReport.as_view(), name='report'),

]