# myapp/serializers.py
from rest_framework import serializers
from .models import GameResult, NumberList, MoneyBet

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameResult
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'previous_game_result': {'read_only': True},
        }

class NumberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberList
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }

class MoneyBetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyBet
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }