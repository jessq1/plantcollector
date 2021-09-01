from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('plants/', views.plants_index, name='plants_index'),
    path('plants/<int:plant_id>/', views.plants_detail, name='plants_detail'),
    path('plants/create/', views.PlantCreate.as_view(), name='plants_create'),
    path('plants/<int:pk>/update/', views.PlantUpdate.as_view(), name='plants_update'),
    path('plants/<int:pk>/delete/', views.PlantDelete.as_view(), name='plants_delete'),
    path('plants/<int:plant_id>/add_water/', views.add_water, name='add_water'),
    path('pots/create/', views.PotCreate.as_view(), name='pots_create'),
    path('pots/<int:pk>/', views.PotDetail.as_view(), name='pots_detail'),
    path('pots/', views.PotList.as_view(), name='pots_index'),
    path('pots/<int:pk>/update/', views.PotUpdate.as_view(), name='pots_update'),
    path('pots/<int:pk>/delete/', views.PotDelete.as_view(), name='pots_delete'),
    path('pots/<int:plant_id>/assoc_pot/<int:pot_id>/', views.assoc_pot, name='assoc_pot'),
]