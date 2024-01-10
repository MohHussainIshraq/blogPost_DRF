from django.urls import path

from post import views

urlpatterns = [
    path('list/', views.PostListView.as_view(), name='post_list_view'),
    path('create/', views.PostCreateView.as_view(), name='post_create_view'),
    path('detail/<int:pk>', views.PostDetailView.as_view(), name='post_detail_view'),
    path('search/', views.PostSearch.as_view(), name='post_search_view'),

]

