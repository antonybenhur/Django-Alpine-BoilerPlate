#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "$RUN_MIGRATIONS" = "true" ]; then
    # Apply database migrations
    echo "Applying database migrations..."
    python manage.py migrate

    # Create superuser if it doesn't exist (optional, can be done manually or via script)
    # echo "Creating superuser..."
    # python manage.py createsuperuser --noinput || true

    # Build Tailwind CSS
    echo "Building Tailwind CSS..."
    python manage.py tailwind build
fi

exec "$@"
