#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bzzz_core.settings')
    # Script temporar pentru crearea superuser-ului pe Render Free
    import django
    django.setup()
    from django.contrib.auth import get_user_model
    User = get_user_model()

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'iancuioan897@yahoo.ro', '08Andre_06@')
        print("=== Superuser 'admin' creat cu succes! ===")
    # End Script temporar pentru crearea superuser-ului pe Render Free
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
