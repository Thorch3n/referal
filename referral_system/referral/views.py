from time import sleep

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views import View
from .models import User


class AuthView(View):
    def get(self, request):
        return render(request, 'referral/auth.html')

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        if not phone_number:
            return render(request, 'referral/auth.html', {'error': 'Номер телефона обязателен'})

        request.session['phone_number'] = phone_number
        request.session['auth_code'] = 1234
        request.session.modified = True

        # Имитация задержки для отправки кода
        sleep(2)

        return render(request, 'referral/auth.html', {
            'success': f'Код отправлен на номер {phone_number}.'
        })


class VerifyCodeView(View):
    def get(self, request):
        return render(request, 'referral/verify.html')

    def post(self, request):
        code = request.POST.get('code')
        phone_number = request.session.get('phone_number')

        if not phone_number:
            return redirect('auth_phone')

        if str(code) == str(request.session.get('auth_code')):
            user, created = User.objects.get_or_create(phone_number=phone_number)
            if created:
                user.invite_code = get_random_string(6, allowed_chars='0123456789ABCDEF')
                user.save()

            # Сохраняем user_id в сессии
            request.session['user_id'] = user.id
            request.session.save()  # Явное сохранение сессии
            return redirect('profile')

        return render(request, 'referral/verify.html', {'error': 'Неверный код'})


class ProfileView(View):
    def get(self, request):
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect('auth_phone')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            request.session.flush()  # Очистка сессии в случае ошибки
            return redirect('auth_phone')

        # Получаем рефералов пользователя
        referrals = user.referrals.all()

        return render(request, 'referral/profile.html',
                      {'user': user, 'referrals': referrals})

    def post(self, request):
        user_id = request.session.get('user_id')

        # Проверка наличия user_id в сессии
        if not user_id:
            return redirect('auth_phone')

        try:
            # Попытка извлечения пользователя
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            # Обработка ситуации, когда пользователь не найден
            request.session.flush()  # Очищаем сессию
            return redirect('auth_phone')

        invite_code = request.POST.get('invite_code')

        # Проверяем, активирован ли уже инвайт-код
        if user.referred_by:
            return render(request, 'referral/profile.html', {
                'user': user,
                'error': 'Вы уже активировали инвайт-код.'
            })

        # Проверяем существование инвайт-кода
        try:
            referred_user = User.objects.get(invite_code=invite_code)
            user.referred_by = referred_user
            user.save()
        except User.DoesNotExist:
            return render(request, 'referral/profile.html', {
                'user': user,
                'error': 'Неверный инвайт-код.'
            })

        return redirect('profile')
