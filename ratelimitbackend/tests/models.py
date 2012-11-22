from django.db import models

try:
    from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
    from django.utils import timezone
except ImportError:
    pass
else:
    class UserManager(BaseUserManager):
        def create_user(self, email, password=None, **extra_fields):
            now = timezone.now()
            if not email:
                raise ValueError('The email must be set.')
            email = UserManager.normalize_email(email)
            user = self.model(email=email, last_login=now, date_joined=now,
                              **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

        def create_superuser(self, email, password, **extra_fields):
            user = self.create_user(email, password, **extra_fields)
            user.is_staff = True
            user.is_active = True
            user.is_superuser = True
            user.save(using=self._db, update_fields=['is_staff', 'is_active',
                                                     'is_superuser'])
            return user

    class User(AbstractBaseUser):
        """A user with email as identifier"""
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []
        email = models.EmailField(max_length=255, unique=True, db_index=True)
        is_staff = models.BooleanField(default=False)
        is_active = models.BooleanField(default=False)
        is_superuser = models.BooleanField(default=False)
        date_joined = models.DateTimeField(default=timezone.now)

        objects = UserManager()
