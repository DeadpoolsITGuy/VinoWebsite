#!/usr/bin/env python3
"""
Backend API Tests for Vino by Tonino - REFACTORED VERSION
Tests the refactored backend with MongoDB image storage and new site-config features
"""

import requests
import json
import os
from io import BytesIO
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv('/app/frontend/.env')
load_dotenv('/app/backend/.env')

BASE_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://vino-tonino.preview.emergentagent.com')
API_URL = f"{BASE_URL}/api"
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'vino2025')

print(f"Testing REFACTORED API at: {API_URL}")
print(f"Admin password: {ADMIN_PASSWORD}")
print("=" * 80)

# Global storage
auth_token = None
uploaded_image_ids = []


def test_site_config_default():
    """Test 1: GET /api/site-config returns default with hero_images array, rotate_seconds"""
    print("\n[TEST 1] GET /api/site-config - Default response structure")
    try:
        response = requests.get(f"{API_URL}/site-config", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Check for required fields
            required_fields = ['hero_images', 'rotate_seconds', 'hero_tagline', 'since_year']
            missing_fields = [f for f in required_fields if f not in data]
            
            if missing_fields:
                print(f"❌ FAIL: Missing required fields: {missing_fields}")
                return False
            
            # Verify hero_images is an array with at least 1 URL
            if not isinstance(data['hero_images'], list):
                print(f"❌ FAIL: hero_images should be an array, got {type(data['hero_images'])}")
                return False
            
            if len(data['hero_images']) < 1:
                print(f"❌ FAIL: hero_images should have at least 1 URL, got {len(data['hero_images'])}")
                return False
            
            # Verify rotate_seconds is present and is a number
            if not isinstance(data['rotate_seconds'], int):
                print(f"❌ FAIL: rotate_seconds should be an integer, got {type(data['rotate_seconds'])}")
                return False
            
            print(f"✓ hero_images: {len(data['hero_images'])} URL(s)")
            print(f"✓ rotate_seconds: {data['rotate_seconds']}")
            print(f"✓ hero_tagline: {data['hero_tagline']}")
            print(f"✓ since_year: {data['since_year']}")
            print("✅ PASS: Default site-config has correct structure")
            return True
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_admin_login_correct():
    """Test 2: POST /api/admin/login with correct password"""
    print("\n[TEST 2] POST /api/admin/login - Correct password")
    global auth_token
    
    try:
        payload = {"password": ADMIN_PASSWORD}
        response = requests.post(f"{API_URL}/admin/login", json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data:
                auth_token = data['token']
                print(f"Token received: {auth_token[:20]}...")
                print("✅ PASS: Login successful with correct password")
                return True
            else:
                print(f"❌ FAIL: Response missing 'token' field")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_admin_login_incorrect():
    """Test 3: POST /api/admin/login with wrong password"""
    print("\n[TEST 3] POST /api/admin/login - Wrong password")
    
    try:
        payload = {"password": "wrongpassword123"}
        response = requests.post(f"{API_URL}/admin/login", json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ PASS: Correctly rejected wrong password with 401")
            return True
        else:
            print(f"❌ FAIL: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_upload_image_jpeg():
    """Test 4: POST /api/admin/upload with JPEG - returns /api/images/{id}"""
    print("\n[TEST 4] POST /api/admin/upload - Valid JPEG")
    
    if not auth_token:
        print("❌ FAIL: No auth token available")
        return False
    
    try:
        # Create a minimal valid JPEG (1x1 pixel)
        jpeg_data = bytes([
            0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01,
            0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43,
            0x00, 0x08, 0x06, 0x06, 0x07, 0x06, 0x05, 0x08, 0x07, 0x07, 0x07, 0x09,
            0x09, 0x08, 0x0A, 0x0C, 0x14, 0x0D, 0x0C, 0x0B, 0x0B, 0x0C, 0x19, 0x12,
            0x13, 0x0F, 0x14, 0x1D, 0x1A, 0x1F, 0x1E, 0x1D, 0x1A, 0x1C, 0x1C, 0x20,
            0x24, 0x2E, 0x27, 0x20, 0x22, 0x2C, 0x23, 0x1C, 0x1C, 0x28, 0x37, 0x29,
            0x2C, 0x30, 0x31, 0x34, 0x34, 0x34, 0x1F, 0x27, 0x39, 0x3D, 0x38, 0x32,
            0x3C, 0x2E, 0x33, 0x34, 0x32, 0xFF, 0xC0, 0x00, 0x0B, 0x08, 0x00, 0x01,
            0x00, 0x01, 0x01, 0x01, 0x11, 0x00, 0xFF, 0xC4, 0x00, 0x14, 0x00, 0x01,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x03, 0xFF, 0xC4, 0x00, 0x14, 0x10, 0x01, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0xFF, 0xDA, 0x00, 0x08, 0x01, 0x01, 0x00, 0x00, 0x3F, 0x00,
            0x37, 0xFF, 0xD9
        ])
        
        files = {'file': ('test_wine_photo.jpg', BytesIO(jpeg_data), 'image/jpeg')}
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = requests.post(f"{API_URL}/admin/upload", files=files, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if 'url' not in data or 'filename' not in data:
                print(f"❌ FAIL: Response missing 'url' or 'filename' field")
                return False
            
            # Verify URL format is /api/images/{id}
            url = data['url']
            if not url.startswith('/api/images/'):
                print(f"❌ FAIL: URL should start with '/api/images/', got: {url}")
                return False
            
            # Extract image ID
            image_id = url.split('/')[-1]
            uploaded_image_ids.append(image_id)
            print(f"✓ Image uploaded with ID: {image_id}")
            print(f"✓ URL format correct: {url}")
            print("✅ PASS: Image upload successful")
            return True
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_get_uploaded_image():
    """Test 5: GET /api/images/{id} returns image bytes with correct content-type"""
    print("\n[TEST 5] GET /api/images/{id} - Fetch uploaded image")
    
    if not uploaded_image_ids:
        print("❌ FAIL: No uploaded images to test")
        return False
    
    try:
        image_id = uploaded_image_ids[0]
        url = f"{API_URL}/images/{image_id}"
        
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"Content-Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            # Verify content-type is an image type
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                print(f"❌ FAIL: Expected image content-type, got: {content_type}")
                return False
            
            # Verify we got binary data
            if len(response.content) == 0:
                print(f"❌ FAIL: Image data is empty")
                return False
            
            print(f"✓ Content-Type is correct: {content_type}")
            print(f"✓ Image data received: {len(response.content)} bytes")
            print("✅ PASS: Image retrieval successful")
            return True
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_upload_invalid_content_type():
    """Test 6: POST /api/admin/upload with invalid content-type returns 400"""
    print("\n[TEST 6] POST /api/admin/upload - Invalid content-type (text/plain)")
    
    if not auth_token:
        print("❌ FAIL: No auth token available")
        return False
    
    try:
        text_data = b"This is not an image file"
        files = {'file': ('test.txt', BytesIO(text_data), 'text/plain')}
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = requests.post(f"{API_URL}/admin/upload", files=files, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ PASS: Correctly rejected invalid content-type with 400")
            return True
        else:
            print(f"❌ FAIL: Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_update_site_config_with_hero_images():
    """Test 7: PUT /api/admin/site-config with hero_images array and rotate_seconds"""
    print("\n[TEST 7] PUT /api/admin/site-config - With hero_images array and rotate_seconds")
    
    if not auth_token:
        print("❌ FAIL: No auth token available")
        return False
    
    try:
        test_config = {
            "hero_images": [
                "https://example.com/wine1.jpg",
                "https://example.com/wine2.jpg"
            ],
            "hero_tagline": "by tonino",
            "since_year": "MMXXV",
            "rotate_seconds": 8
        }
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.put(f"{API_URL}/admin/site-config", json=test_config, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Verify the config was persisted
            print("  Verifying persistence...")
            get_response = requests.get(f"{API_URL}/site-config", timeout=10)
            
            if get_response.status_code == 200:
                saved_config = get_response.json()
                
                # Check all fields
                checks = [
                    (saved_config.get('hero_tagline') == "by tonino", "hero_tagline"),
                    (saved_config.get('since_year') == "MMXXV", "since_year"),
                    (saved_config.get('rotate_seconds') == 8, "rotate_seconds"),
                    (isinstance(saved_config.get('hero_images'), list), "hero_images is array"),
                    (len(saved_config.get('hero_images', [])) == 2, "hero_images has 2 items"),
                ]
                
                failed_checks = [name for passed, name in checks if not passed]
                
                if failed_checks:
                    print(f"  ❌ FAIL: Failed checks: {failed_checks}")
                    print(f"  Saved config: {saved_config}")
                    return False
                
                print("  ✓ All fields persisted correctly")
                print("✅ PASS: Site config update with hero_images array successful")
                return True
            else:
                print(f"  ❌ FAIL: Could not verify (GET returned {get_response.status_code})")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_legacy_hero_image_url_backfill():
    """Test 8: Legacy support - if only hero_image_url saved, response backfills hero_images"""
    print("\n[TEST 8] Legacy backfill - hero_image_url to hero_images array")
    
    if not auth_token:
        print("❌ FAIL: No auth token available")
        return False
    
    try:
        # Save config with ONLY hero_image_url (legacy format)
        legacy_config = {
            "hero_image_url": "https://example.com/legacy-wine.jpg",
            "hero_tagline": "legacy test",
            "since_year": "MMXXIV"
        }
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.put(f"{API_URL}/admin/site-config", json=legacy_config, headers=headers, timeout=10)
        print(f"PUT Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ FAIL: Could not save legacy config")
            return False
        
        # Now GET and verify hero_images is backfilled
        print("  Verifying backfill...")
        get_response = requests.get(f"{API_URL}/site-config", timeout=10)
        
        if get_response.status_code == 200:
            saved_config = get_response.json()
            print(f"  Response: {json.dumps(saved_config, indent=2)}")
            
            # Verify hero_images array is populated from hero_image_url
            if 'hero_images' not in saved_config:
                print(f"  ❌ FAIL: hero_images not in response")
                return False
            
            if not isinstance(saved_config['hero_images'], list):
                print(f"  ❌ FAIL: hero_images is not an array")
                return False
            
            if len(saved_config['hero_images']) < 1:
                print(f"  ❌ FAIL: hero_images array is empty")
                return False
            
            # Check if hero_images[0] matches hero_image_url
            if saved_config['hero_images'][0] != saved_config.get('hero_image_url'):
                print(f"  ❌ FAIL: hero_images[0] doesn't match hero_image_url")
                print(f"  hero_images[0]: {saved_config['hero_images'][0]}")
                print(f"  hero_image_url: {saved_config.get('hero_image_url')}")
                return False
            
            print(f"  ✓ hero_images backfilled: {saved_config['hero_images']}")
            print("✅ PASS: Legacy backfill working correctly")
            return True
        else:
            print(f"  ❌ FAIL: GET returned {get_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_update_menu():
    """Test 9: PUT /api/admin/menu still works"""
    print("\n[TEST 9] PUT /api/admin/menu - Verify still working")
    
    if not auth_token:
        print("❌ FAIL: No auth token available")
        return False
    
    try:
        test_menu = {
            "fizz": [{"name": "Prosecco Superiore", "price": "32 / 7"}],
            "white": [{"name": "Pinot Grigio", "price": "28 / 6.5"}],
            "orange": [{"name": "Amber Wine", "price": "35 / 8"}],
            "rose": [{"name": "Provence Rosé", "price": "30 / 7"}],
            "red": [{"name": "Barolo", "price": "55 / 12"}]
        }
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.put(f"{API_URL}/admin/menu", json=test_menu, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            # Verify persistence
            get_response = requests.get(f"{API_URL}/menu", timeout=10)
            if get_response.status_code == 200:
                saved_menu = get_response.json()
                if saved_menu.get('fizz', [{}])[0].get('name') == "Prosecco Superiore":
                    print("  ✓ Menu persisted correctly")
                    print("✅ PASS: Menu update still working")
                    return True
                else:
                    print(f"  ❌ FAIL: Menu not persisted correctly")
                    return False
            else:
                print(f"  ❌ FAIL: Could not verify menu")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_delete_image_existing():
    """Test 10: DELETE /api/admin/images/{id} deletes an image"""
    print("\n[TEST 10] DELETE /api/admin/images/{id} - Delete existing image")
    
    if not auth_token:
        print("❌ FAIL: No auth token available")
        return False
    
    if not uploaded_image_ids:
        print("❌ FAIL: No uploaded images to delete")
        return False
    
    try:
        image_id = uploaded_image_ids[0]
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = requests.delete(f"{API_URL}/admin/images/{image_id}", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if data.get('deleted') == True:
                print(f"✓ Image {image_id} deleted successfully")
                
                # Verify image is no longer accessible
                get_response = requests.get(f"{API_URL}/images/{image_id}", timeout=10)
                if get_response.status_code == 404:
                    print("  ✓ Image no longer accessible (404)")
                    print("✅ PASS: Image deletion successful")
                    uploaded_image_ids.remove(image_id)
                    return True
                else:
                    print(f"  ❌ FAIL: Image still accessible (status {get_response.status_code})")
                    return False
            else:
                print(f"❌ FAIL: Expected {{deleted: true}}, got {data}")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_delete_image_nonexistent():
    """Test 11: DELETE /api/admin/images/{id} with non-existent id returns {deleted: false}"""
    print("\n[TEST 11] DELETE /api/admin/images/{id} - Non-existent image")
    
    if not auth_token:
        print("❌ FAIL: No auth token available")
        return False
    
    try:
        fake_id = "nonexistent123456789"
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = requests.delete(f"{API_URL}/admin/images/{fake_id}", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if data.get('deleted') == False:
                print("✅ PASS: Correctly returned {deleted: false} for non-existent image")
                return True
            else:
                print(f"❌ FAIL: Expected {{deleted: false}}, got {data}")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            print(f"  Note: Should not return 500 for non-existent ID")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_unauthorized_upload():
    """Test 12: POST /api/admin/upload without token returns 401"""
    print("\n[TEST 12] POST /api/admin/upload - Unauthorized (no token)")
    
    try:
        jpeg_data = b"\xFF\xD8\xFF\xE0\x00\x10JFIF"
        files = {'file': ('test.jpg', BytesIO(jpeg_data), 'image/jpeg')}
        
        response = requests.post(f"{API_URL}/admin/upload", files=files, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ PASS: Correctly rejected unauthorized upload (401)")
            return True
        else:
            print(f"❌ FAIL: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_unauthorized_delete():
    """Test 13: DELETE /api/admin/images/{id} without token returns 401"""
    print("\n[TEST 13] DELETE /api/admin/images/{id} - Unauthorized (no token)")
    
    try:
        fake_id = "test123"
        response = requests.delete(f"{API_URL}/admin/images/{fake_id}", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ PASS: Correctly rejected unauthorized delete (401)")
            return True
        else:
            print(f"❌ FAIL: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def cleanup_test_data():
    """Clean up any remaining test data"""
    print("\n[CLEANUP] Removing test data from database")
    
    if not auth_token:
        print("⚠ Warning: No auth token, cannot clean up")
        return
    
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Delete any remaining uploaded images
        for image_id in uploaded_image_ids[:]:
            response = requests.delete(f"{API_URL}/admin/images/{image_id}", headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"  ✓ Deleted image {image_id}")
                uploaded_image_ids.remove(image_id)
        
        # Reset site config to default
        default_config = {
            "hero_images": [
                "https://images.squarespace-cdn.com/content/v1/67f667faca6fd714aaa732b0/dcb76f8f-f576-4f2a-a31d-031d8d8a7698/uliana-kopanytsia-epHhP3H71sw-unsplash.jpg"
            ],
            "hero_tagline": "by tonino",
            "since_year": "MMXXV",
            "rotate_seconds": 6
        }
        response = requests.put(f"{API_URL}/admin/site-config", json=default_config, headers=headers, timeout=10)
        if response.status_code == 200:
            print("  ✓ Reset site config to default")
        
        print("✓ Cleanup complete")
    except Exception as e:
        print(f"⚠ Cleanup error: {str(e)}")


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("VINO BY TONINO - REFACTORED BACKEND TEST SUITE")
    print("=" * 80)
    
    results = []
    
    # Test 1: Default site-config structure
    results.append(("GET /api/site-config (default structure)", test_site_config_default()))
    
    # Test 2-3: Admin login
    results.append(("POST /api/admin/login (correct password)", test_admin_login_correct()))
    results.append(("POST /api/admin/login (wrong password)", test_admin_login_incorrect()))
    
    # Test 4-5: Image upload and retrieval
    results.append(("POST /api/admin/upload (JPEG)", test_upload_image_jpeg()))
    results.append(("GET /api/images/{id}", test_get_uploaded_image()))
    
    # Test 6: Invalid content-type
    results.append(("POST /api/admin/upload (invalid type)", test_upload_invalid_content_type()))
    
    # Test 7-8: Site config with new fields
    results.append(("PUT /api/admin/site-config (hero_images array)", test_update_site_config_with_hero_images()))
    results.append(("Legacy backfill (hero_image_url → hero_images)", test_legacy_hero_image_url_backfill()))
    
    # Test 9: Menu still works
    results.append(("PUT /api/admin/menu", test_update_menu()))
    
    # Test 10-11: Image deletion
    results.append(("DELETE /api/admin/images/{id} (existing)", test_delete_image_existing()))
    results.append(("DELETE /api/admin/images/{id} (non-existent)", test_delete_image_nonexistent()))
    
    # Test 12-13: Unauthorized requests
    results.append(("POST /api/admin/upload (unauthorized)", test_unauthorized_upload()))
    results.append(("DELETE /api/admin/images/{id} (unauthorized)", test_unauthorized_delete()))
    
    # Cleanup
    cleanup_test_data()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "=" * 80)
    print(f"TOTAL: {passed}/{total} tests passed ({100*passed//total}%)")
    print("=" * 80)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
