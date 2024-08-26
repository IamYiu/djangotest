from django.urls import path
from .views import add_number_to_user_list
from django.contrib.auth.views import LoginView
from .views import GameListView, GameDetailView, GameListCreateAPIView, GameRetrieveUpdateDestroyAPIView, \
    DeleteAllGamesAPIView, NumberListAPIView, LatestGameAPIView, MoneyListCreateAPIView, MoneyByIdAPIView

urlpatterns = [
    path('add-number/<int:new_number>/', add_number_to_user_list, name='add_number_to_user_list'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('games/', GameListView.as_view(), name='game_list'),
    path('games/<int:pk>/', GameDetailView.as_view(), name='game_detail'),
    path('api/games/', GameListCreateAPIView.as_view(), name='game-list-create'),
    path('api/games/<int:pk>/', GameRetrieveUpdateDestroyAPIView.as_view(), name='game-detail'),
    path('api/games/delete_all/', DeleteAllGamesAPIView.as_view(), name='delete-all-games'),
    path('api/games/latest/', LatestGameAPIView.as_view(), name='latest-game'),
    path('api/list/', NumberListAPIView.as_view(), name='list-detail'),
    path('api/money/', MoneyListCreateAPIView.as_view(), name='money-list-create'),
    path('api/money/get/', MoneyByIdAPIView.as_view(), name='get-bet'),
]
