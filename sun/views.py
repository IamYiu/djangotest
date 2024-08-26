import time
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import GameResult, NumberList, MoneyBet


from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from rest_framework import generics
from .serializers import GameSerializer, NumberListSerializer, MoneyBetSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

def chunked_queryset(queryset, chunk_size=1000):
    for i in range(0, len(queryset), chunk_size):
        yield queryset[i:i + chunk_size]



# List view to show all games
class GameListView(LoginRequiredMixin, ListView):
    model = GameResult
    template_name = 'game_list.html'  # Specify your own template name/location
    context_object_name = 'games'
    login_url = '/login/'  # URL to redirect to if the user is not logged in


# Detail view to show a single game's details
class GameDetailView(LoginRequiredMixin, DetailView):
    model = GameResult
    template_name = 'game_detail.html'  # Specify your own template name/location
    context_object_name = 'game'
    login_url = '/login/'  # URL to redirect to if the user is not logged in


@login_required
def add_number_to_user_list(request, new_number):
    # Get the logged-in user
    user = request.user

    # Get or create the NumberList instance associated with the user
    number_list, created = NumberList.objects.get_or_create(user=user)

    # Append the new number to the existing list
    number_list.numbers.append(new_number)

    # Save the updated instance back to the database
    number_list.save()

    return HttpResponse(f"Added {new_number} to {user.username}'s number list.")


class GameListCreateAPIView(generics.ListCreateAPIView):
    queryset = GameResult.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Get the current user
        user = self.request.user

        # Get the latest game for the user
        latest_game = GameResult.objects.filter(user=user).order_by('-created_date_time').first()

        # Set the previous_game to the latest game if it exists
        previous_game = latest_game if latest_game else None

        # Save the new game with the reference to the previous game
        serializer.save(user=user, previous_game_result=previous_game)


class LatestGameAPIView(generics.RetrieveAPIView):
    queryset = GameResult.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        instance = GameResult.objects.filter(user=user).order_by('-id').first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class GameRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameResult.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]


class DeleteAllGamesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        last_pk = instance = GameResult.objects.filter(user=self.request.user).order_by('-id').first().id
        print(f"last pk {last_pk}")
        batch_size = 1000  # Define the batch size
        deleted_count = 0
        while True:
            # Get a batch of primary keys of games to delete
            games_to_delete = list(GameResult.objects.values_list('pk', flat=True)[:batch_size])
            if last_pk in games_to_delete:
                games_to_delete.remove(last_pk)
            if not games_to_delete:
                break
            # Delete the batch of games
            with transaction.atomic():
                GameResult.objects.filter(pk__in=games_to_delete).delete()


            deleted_count += len(games_to_delete)
            # Optional: sleep to reduce load on the database
            time.sleep(0.1)

        return Response({"message": f"All games deleted successfully. Total deleted: {deleted_count}"},
                        status=status.HTTP_204_NO_CONTENT)


class NumberListAPIView(generics.ListAPIView):
    queryset = NumberList.objects.all()
    serializer_class = NumberListSerializer
    permission_classes = [IsAuthenticated]

class MoneyListCreateAPIView(generics.ListCreateAPIView):
    queryset = MoneyBet.objects.all()
    serializer_class = MoneyBetSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class MoneyByIdAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        bet_sid = request.query_params.get('sid', None)
        if bet_sid is None:
            return Response({"error": "Sid parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bet = MoneyBet.objects.filter(user=user, sid=bet_sid).first()
            if not bet:
                return Response({"error": "Take this"}, status=status.HTTP_404_NOT_FOUND)
            serializer = MoneyBetSerializer(bet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MoneyBet.DoesNotExist:
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)

