#!/usr/bin/env python3
"""
HTTPS Configuration Test Script
Tests the Django security settings and HTTPS configuration
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.conf import settings

def test_security_settings():
    """Test that all security settings are properly configured."""
    
    print("🔐 Testing Django Security Settings")
    print("=" * 50)
    
    # List of security settings to check
    security_settings = {
        'DEBUG': (False, 'Debug mode should be False in production'),
        'SECURE_SSL_REDIRECT': (True, 'Should redirect HTTP to HTTPS'),
        'SECURE_HSTS_SECONDS': (31536000, 'HSTS should be set to 1 year'),
        'SESSION_COOKIE_SECURE': (True, 'Session cookies should be secure'),
        'CSRF_COOKIE_SECURE': (True, 'CSRF cookies should be secure'),
        'X_FRAME_OPTIONS': ('DENY', 'Should deny framing'),
        'SECURE_CONTENT_TYPE_NOSNIFF': (True, 'Should prevent MIME sniffing'),
        'SECURE_BROWSER_XSS_FILTER': (True, 'Should enable XSS filter'),
    }
    
    all_passed = True
    
    for setting, (expected_value, description) in security_settings.items():
        actual_value = getattr(settings, setting, None)
        if actual_value == expected_value:
            print(f"✅ {setting}: {actual_value} - {description}")
        else:
            print(f"❌ {setting}: Expected {expected_value}, got {actual_value}")
            print(f"   {description}")
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 All security settings are correctly configured for PRODUCTION!")
    else:
        print(f"⚠️  Some security settings need adjustment (DEBUG={settings.DEBUG})")
    
    return all_passed

def check_development_overrides():
    """Check if development overrides are in place."""
    print("\n🛠️  Checking Development Mode")
    print("=" * 50)
    
    if settings.DEBUG:
        print(f"📱 DEBUG mode is {settings.DEBUG}")
        print("Expected development overrides:")
        
        # Check development overrides
        dev_checks = [
            ('SECURE_SSL_REDIRECT', False, 'HTTPS redirect disabled'),
            ('SESSION_COOKIE_SECURE', False, 'Secure cookies disabled'),
            ('CSRF_COOKIE_SECURE', False, 'Secure CSRF disabled'),
            ('SECURE_HSTS_SECONDS', 0, 'HSTS disabled'),
        ]
        
        for setting, expected, description in dev_checks:
            actual = getattr(settings, setting, None)
            if actual == expected:
                print(f"✅ {setting}: {actual} - {description}")
            else:
                print(f"❌ {setting}: Expected {expected}, got {actual}")
    else:
        print(f"🚀 PRODUCTION mode (DEBUG={settings.DEBUG})")
        print("All security settings should be enabled")

if __name__ == '__main__':
    print("Django HTTPS Security Test")
    print("=" * 50)
    
    test_security_settings()
    check_development_overrides()
    
    print("\n📋 Summary:")
    print("- Current DEBUG mode:", settings.DEBUG)
    print("- Run 'python manage.py check --deploy' for Django deployment checks")
    print("- For production: Set DEBUG = False in settings.py")
    print("- Test HTTPS configuration with SSL Labs: https://www.ssllabs.com/ssltest/")
