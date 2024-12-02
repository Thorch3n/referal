# Referral System API

## API Endpoints

### 1. Авторизация (Получение кода)
**POST /api/auth/**  
**Request Body:**
```json
{
  "phone_number": "+79123456789"
}
```
### Response:
``` 
{
  "message": "Код отправлен на указанный номер телефона."
}
```
---
### 2. Верификация кода
#### POST /api/verify/
#### Request Body:
``` 
{
  "code": "1234"
}
```
#### Response:
``` 
{
  "message": "Успешная верификация."
}
```
---
### 3. Профиль пользователя
#### GET /api/profile/
#### Response:
``` 
{
  "phone_number": "+79123456789",
  "invite_code": "A1B2C3",
  "referrals": [
    {"phone_number": "+79112223344"},
    {"phone_number": "+79115556677"}
  ]
}
```

---
