#!/bin/bash
# scripts/collectstatic.sh

echo "====================================="
echo "Collecting static files for production"
echo "====================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found. Run this script from the project root."
    exit 1
fi

# Ensure STATIC_ROOT is set in settings
if ! grep -q "STATIC_ROOT" social_media_api/settings.py; then
    echo "Warning: STATIC_ROOT not found in settings.py"
    echo "Adding STATIC_ROOT to settings.py..."
    echo "" >> social_media_api/settings.py
    echo "# Production static files" >> social_media_api/settings.py
    echo "STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')" >> social_media_api/settings.py
fi

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Run collectstatic
echo "Running collectstatic..."
python manage.py collectstatic --noinput --clear

# Check if successful
if [ $? -eq 0 ]; then
    echo "✅ Static files collected successfully!"
    echo "Files collected in: $(pwd)/staticfiles/"
    echo "Total files: $(find staticfiles -type f | wc -l)"
else
    echo "❌ Failed to collect static files"
    exit 1
fi

echo "====================================="
