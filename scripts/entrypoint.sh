#!/bin/bash

echo "In entrypoint.sh."

/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT
/wait-for-it.sh $RABBITMQ_HOST:$RABBITMQ_PORT

if [ "$APPLY_DB_MIGRATIONS" = "true" ]
then
	echo "Apply database migrations."
	cd /app/
	python3 manage.py migrate
fi

# Run command
echo "Running: $@"
exec "$@"
