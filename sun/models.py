from django.db import models
from django.contrib.auth.models import User

class GameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=30, default='TaiXiu')
    result = models.CharField(max_length=3, default='000')
    result_data = models.CharField(max_length=1, default='')
    sid = models.CharField(max_length=50, default='')
    previous_game_result = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='next_game_result')
    counter_result = models.IntegerField(default=0)
    counter_11 = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.result_data:
            self.result_data = 'T' if sum(map(int, self.result)) > 10 else 'X'
        if self.previous_game_result and int(self.previous_game_result.sid)+1 != int(self.sid):
            self.previous_game_result = None
        if not self.previous_game_result:
            self.counter_result = 1
            self.counter_11 = 0
            user_list, created = NumberList.objects.get_or_create(user=self.user)
            user_list.numbers = []
            user_list.max_number = 0
            user_list.current_number = 1
            user_list.save()
        if self.previous_game_result:
            user_list, created = NumberList.objects.get_or_create(user=self.user)
            if self.result_data == self.previous_game_result.result_data:
                self.counter_result = self.previous_game_result.counter_result + 1
                self.counter_11 = 0
            else:
                user_list.numbers.append(self.previous_game_result.counter_result)
                self.counter_result = 1
                self.counter_11 = self.previous_game_result.counter_11 + 1
            user_list.current_number = self.counter_result
            user_list.save()
        super(GameResult, self).save(*args, **kwargs)

    def __str__(self):
        return f"the game {self.game_name} with session {self.sid} has result {self.result_data}"
class NumberList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numbers = models.JSONField(default=list)
    current_number = models.IntegerField(default=0)
    max_number = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.current_number > self.max_number:
            self.max_number = self.current_number
        super(NumberList, self).save(*args, **kwargs)

    def __str__(self):
        return f"{sum(self.numbers)} session, max = {self.max_number} of user {self.user.username}"

class MoneyBet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sid = models.CharField(max_length=50, default='')
    bet_amount = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"sid = {self.sid}, amount bet = {self.bet_amount}, timestamp = {self.created_date_time}"