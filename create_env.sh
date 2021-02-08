#!/bin/bash
touch .env
echo 'REDIS_HOST=$(REDIS_HOST)' >> .env
