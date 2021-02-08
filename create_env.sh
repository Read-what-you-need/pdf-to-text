
#!/bin/bash
> .env
echo 'REDIS_HOST='$REDIS_HOST >> .env
echo 'REDIS_PORT='$REDIS_PORT >> .env
echo 'REDIS_PASSKEY='$REDIS_PASSKEY >> .env
echo 'AWS_ACCESS_KEY_ID='$AWS_ACCESS_KEY_ID >> .env
echo 'AWS_SECRET_ACCESS_KEY='$AWS_SECRET_ACCESS_KEY >> .env
echo 'AWS_REGION_NAME='$AWS_REGION_NAME >> .env
