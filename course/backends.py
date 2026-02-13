from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class FirstTimeLoginBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)

            # لو اليوزر ده اتكريت بس لسه ملوش باسورد (يعني أول مرة يدخل)
            if not user.has_usable_password() and password:
                # هناخد الباسورد اللي كتبه دلوقتي ونسيفهوله للأبد
                user.set_password(password)
                user.save()
                return user

            # لو هو أصلاً ليه باسورد، نتأكد إنه بيكتب الباسورد الصح بتاعه
            elif user.check_password(password):
                return user

        except User.DoesNotExist:
            return None

        return None