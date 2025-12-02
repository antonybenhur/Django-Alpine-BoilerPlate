import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.users.models import User

email = 'admin@example.com'
username = 'admin'
password = 'admin123'

user, created = User.objects.get_or_create(
    email=email,
    defaults={
        'username': username,
        'is_staff': True,
        'is_superuser': True
    }
)
user.set_password(password)
user.save()

if created:
    print(f"User created successfully!")
else:
    print(f"User already exists, password updated!")

print(f"\nCredentials:")
print(f"  Email: {email}")
print(f"  Password: {password}")

