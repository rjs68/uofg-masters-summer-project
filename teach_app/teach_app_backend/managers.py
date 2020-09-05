from django.contrib.auth.base_user import BaseUserManager


class TeachUserManager(BaseUserManager):
    """
    Custom user model manager using email as identifier and requiring
    name and password fields
    """
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email, first_name, last_name, password, **extra_fields)
