from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from random import randint
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, username, birth_date=None, password=None):
        if not username:
            raise ValueError('Dude, you must include username')
        if not birth_date:
            birth_date = datetime.today().date()
        user = self.model(
            username=username,
            birthDate=birth_date,
            number=randint(0, 100)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MiloUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True, db_index=True)
    birthDate = models.DateField()
    number = models.PositiveSmallIntegerField()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        name = '%s' % self.username
        return name.strip()

    def __str__(self):
        return '{}'.format(self.username)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


@receiver(pre_save, sender=MiloUser)
def pre_save_callback(sender, instance, *args, **kwargs):
    if not instance.number:
        instance.number = randint(0, 100)
