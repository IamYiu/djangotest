from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Register your models here.
from .models import GameResult, NumberList, MoneyBet

def generate_token(modeladmin, request, queryset):
    for user in queryset:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        # Display the tokens (this is just an example, you might want to log them or display them in another way)
        print(f'Access token for {user.username}: {access_token}')
        print(f'Refresh token for {user.username}: {refresh_token}')

generate_token.short_description = 'Generate JWT token for selected users'


class UserAdmin(admin.ModelAdmin):
    actions = [generate_token]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(GameResult)
admin.site.register(NumberList)
admin.site.register(MoneyBet)