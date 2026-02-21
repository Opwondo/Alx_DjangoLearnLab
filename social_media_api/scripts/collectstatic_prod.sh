#!/bin/bash
# scripts/collectstatic_prod.sh
# Use this for production static file collection

echo "====================================="
echo "Collecting static files for PRODUCTION"
echo "====================================="

# Set to production settings
export DJANGO_SETTINGS_MODULE=social_media_api.settings_render

# Run collectstatic
python manage.py collectstatic --noinput --clear

if [ $? -eq 0 ]; then
    echo "✅ Production static files collected successfully!"
else
    echo "❌ Failed to collect static files"
    exit 1
fi
