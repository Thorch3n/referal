from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.utils.crypto import get_random_string
from time import sleep


class AuthAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Номер телефона обязателен.'}, status=status.HTTP_400_BAD_REQUEST)

        request.session['phone_number'] = phone_number
        request.session['auth_code'] = 1234
        request.session.modified = True

        sleep(2)  # Имитация отправки кода

        return Response({'message': 'Код отправлен на указанный номер телефона.'})


class VerifyCodeAPIView(APIView):
    def post(self, request):
        code = request.data.get('code')
        phone_number = request.session.get('phone_number')

        if not phone_number:
            return Response({'error': 'Номер телефона отсутствует в сессии.'}, status=status.HTTP_400_BAD_REQUEST)

        if str(code) != str(request.session.get('auth_code')):
            return Response({'error': 'Неверный код.'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            user.invite_code = get_random_string(6, allowed_chars='0123456789ABCDEF')
            user.save()

        request.session['user_id'] = user.id
        request.session.modified = True

        return Response({'message': 'Успешная верификация.'})


class ProfileAPIView(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'error': 'Не авторизован.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)

        referrals = user.referrals.all()
        referrals_data = [{'phone_number': r.phone_number} for r in referrals]

        return Response({
            'phone_number': user.phone_number,
            'invite_code': user.invite_code,
            'referrals': referrals_data
        })
