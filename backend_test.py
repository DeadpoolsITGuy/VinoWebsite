#!/usr/bin/env python3
"""
Backend API Tests for Vino by Tonino
Tests all admin, menu, site-config, and upload endpoints
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

print(f"Testing API at: {API_URL}")
print(f"Admin password: {ADMIN_PASSWORD}")
print("=" * 80)

# Global token storage
auth_token = None

def test_get_menu():
    """Test GET /api/menu - public endpoint"""
    print("\n[TEST 1] GET /api/menu")
    try:
        response = requests.get(f"{API_URL}/menu", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            
            # Check for required categories
            required_categories = ['fizz', 'white', 'orange', 'rose', 'red']
            for cat in required_categories:
                if cat not in data:
                    print(f"❌ FAIL: Missing category '{cat}'")
                    return False
                print(f"  - {cat}: {len(data[cat])} items")
            
            # Check structure of first item if available
            if data.get('fizz') and len(data['fizz']) > 0:
                first_item = data['fizz'][0]
                if 'name' in first_item and 'price' in first_item:
                    print(f"  Sample item: {first_item['name']} - {first_item['price']}")
                else:
                    print(f"❌ FAIL: Menu items missing 'name' or 'price' fields")
                    return False
            
            print("✅ PASS: GET /api/menu works correctly")
            return True
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_get_site_config():
    """Test GET /api/site-config - public endpoint"""
    print("\n[TEST 2] GET /api/site-config")
    try:
        response = requests.get(f"{API_URL}/site-config", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Check for expected fields
            expected_fields = ['hero_image_url', 'hero_tagline', 'since_year']
            for field in expected_fields:
                if field not in data:
                    print(f"❌ FAIL: Missing field '{field}'")
                    return False
            
            print("✅ PASS: GET /api/site-config works correctly")
            return True
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_admin_login_correct():
    """Test POST /api/admin/login with correct password"""
    print("\n[TEST 3] POST /api/admin/login (correct password)")
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
                print("✅ PASS: Admin login successful with correct password")
                return True
            else:
                print(f"❌ FAIL: Response missing 'token' field")
                print(f"Response: {data}")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_admin_login_incorrect():
    """Test POST /api/admin/login with incorrect password"""
    print("\n[TEST 4] POST /api/admin/login (incorrect password)")
    
    try:
        payload = {"password": "wrongpassword123"}
        response = requests.post(f"{API_URL}/admin/login", json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ PASS: Correctly rejected incorrect password with 401")
            return True
        else:
            print(f"❌ FAIL: Expected 401, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_admin_verify_with_token():
    """Test GET /api/admin/verify with valid token"""
    print("\n[TEST 5] GET /api/admin/verify (with valid token)")
    
    if not auth_token:
        print("❌ FAIL: No auth token available (login test must pass first)")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{API_URL}/admin/verify", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok') == True:
                print("✅ PASS: Token verification successful")
                return True
            else:
                print(f"❌ FAIL: Expected {{ok: true}}, got {data}")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_admin_verify_without_token():
    """Test GET /api/admin/verify without token"""
    print("\n[TEST 6] GET /api/admin/verify (without token)")
    
    try:
        response = requests.get(f"{API_URL}/admin/verify", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ PASS: Correctly rejected request without token (401)")
            return True
        else:
            print(f"❌ FAIL: Expected 401, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_admin_verify_invalid_token():
    """Test GET /api/admin/verify with invalid token"""
    print("\n[TEST 7] GET /api/admin/verify (with invalid token)")
    
    try:
        headers = {"Authorization": "Bearer invalid_token_12345"}
        response = requests.get(f"{API_URL}/admin/verify", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ PASS: Correctly rejected invalid token (401)")
            return True
        else:
            print(f"❌ FAIL: Expected 401, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_update_menu():
    """Test PUT /api/admin/menu - protected endpoint"""
    print("\n[TEST 8] PUT /api/admin/menu")
    
    if not auth_token:
        print("❌ FAIL: No auth token available")
        return False
    
    try:
        # Create test menu data
        test_menu = {
            "fizz": [
                {"name": "Test Prosecco", "price": "30 / 6"},
                {"name": "Test Champagne", "price": "50 / 10"}
            ],
            "white": [
                {"name": "Test Chardonnay", "price": "35 / 8"}
            ],
            "orange": [
                {"name": "Test Orange Wine", "price": "32 / 7"}
            ],
            "rose": [
                {"name": "Test Rosé", "price": "28 / 6.5"}
            ],
            "red": [
                {"name": "Test Merlot", "price": "40 / 9"},
                {"name": "Test Cabernet", "price": "45 / 10"}
            ]
        }
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.put(f"{API_URL}/admin/menu", json=test_menu, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            
            # Verify the menu was saved by fetching it again
            print("  Verifying saved menu...")
            get_response = requests.get(f"{API_URL}/menu", timeout=10)
            if get_response.status_code == 200:
                saved_menu = get_response.json()
                
                # Check if our test data was saved
                if saved_menu.get('fizz', [{}])[0].get('name') == "Test Prosecco":
                    print("  ✓ Menu data persisted correctly")
                    print("✅ PASS: PUT /api/admin/menu works correctly")
                    return True
                else:
                    print(f"  ❌ FAIL: Menu data not persisted correctly")
                    print(f"  Expected first fizz: 'Test Prosecco', got: {saved_menu.get('fizz', [{}])[0].get('name')}")
                    return False
            else:
                print(f"  ❌ FAIL: Could not verify saved menu (GET returned {get_response.status_code})")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_update_menu_unauthorized():
    """Test PUT /api/admin/menu without token"""
    print("\n[TEST 9] PUT /api/admin/menu (unauthorized)")
    
    try:
        test_menu = {
            "fizz": [],
            "white": [],
            "orange": [],
            "rose": [],
            "red": []
        }
        
        response = requests.put(f"{API_URL}/admin/menu", json=test_menu, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ PASS: Correctly rejected unauthorized request (401)")
            return True
        else:
            print(f"❌ FAIL: Expected 401, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_update_site_config():
    """Test PUT /api/admin/site-config - protected endpoint"""
    print("\n[TEST 10] PUT /api/admin/site-config")
    
    if not auth_token:
        print("❌ FAIL: No auth token available")
        return False
    
    try:
        # Create test site config
        test_config = {
            "hero_image_url": "https://example.com/test-image.jpg",
            "hero_tagline": "Test Tagline by Tonino",
            "since_year": "MMXXVI"
        }
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.put(f"{API_URL}/admin/site-config", json=test_config, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Verify the config was saved by fetching it again
            print("  Verifying saved config...")
            get_response = requests.get(f"{API_URL}/site-config", timeout=10)
            if get_response.status_code == 200:
                saved_config = get_response.json()
                
                # Check if our test data was saved
                if (saved_config.get('hero_tagline') == "Test Tagline by Tonino" and
                    saved_config.get('since_year') == "MMXXVI"):
                    print("  ✓ Site config persisted correctly")
                    print("✅ PASS: PUT /api/admin/site-config works correctly")
                    return True
                else:
                    print(f"  ❌ FAIL: Site config not persisted correctly")
                    print(f"  Saved config: {saved_config}")
                    return False
            else:
                print(f"  ❌ FAIL: Could not verify saved config (GET returned {get_response.status_code})")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_update_site_config_unauthorized():
    """Test PUT /api/admin/site-config without token"""
    print("\n[TEST 11] PUT /api/admin/site-config (unauthorized)")
    
    try:
        test_config = {
            "hero_tagline": "Unauthorized Test"
        }
        
        response = requests.put(f"{API_URL}/admin/site-config", json=test_config, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ PASS: Correctly rejected unauthorized request (401)")
            return True
        else:
            print(f"❌ FAIL: Expected 401, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_upload_image_valid():
    """Test POST /api/admin/upload with valid image"""
    print("\n[TEST 12] POST /api/admin/upload (valid JPEG)")
    
    if not auth_token:
        print("❌ FAIL: No auth token available")
        return False
    
    try:
        # Create a minimal valid JPEG (1x1 pixel red square)
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
        
        files = {'file': ('test_image.jpg', BytesIO(jpeg_data), 'image/jpeg')}
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = requests.post(f"{API_URL}/admin/upload", files=files, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if 'url' in data and 'filename' in data:
                uploaded_url = data['url']
                print(f"  Uploaded URL: {uploaded_url}")
                
                # Verify the uploaded file is accessible
                print("  Verifying uploaded file is accessible...")
                file_url = f"{BASE_URL}{uploaded_url}"
                get_response = requests.get(file_url, timeout=10)
                
                if get_response.status_code == 200:
                    print(f"  ✓ File accessible at {file_url}")
                    print("✅ PASS: POST /api/admin/upload works correctly")
                    return True
                else:
                    print(f"  ❌ FAIL: Uploaded file not accessible (status {get_response.status_code})")
                    return False
            else:
                print(f"❌ FAIL: Response missing 'url' or 'filename' field")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_upload_image_invalid_type():
    """Test POST /api/admin/upload with invalid file type"""
    print("\n[TEST 13] POST /api/admin/upload (invalid file type)")
    
    if not auth_token:
        print("❌ FAIL: No auth token available")
        return False
    
    try:
        # Create a text file
        text_data = b"This is not an image"
        files = {'file': ('test.txt', BytesIO(text_data), 'text/plain')}
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = requests.post(f"{API_URL}/admin/upload", files=files, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ PASS: Correctly rejected invalid file type (400)")
            return True
        else:
            print(f"❌ FAIL: Expected 400, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def test_upload_image_unauthorized():
    """Test POST /api/admin/upload without token"""
    print("\n[TEST 14] POST /api/admin/upload (unauthorized)")
    
    try:
        jpeg_data = b"\xFF\xD8\xFF\xE0\x00\x10JFIF"
        files = {'file': ('test.jpg', BytesIO(jpeg_data), 'image/jpeg')}
        
        response = requests.post(f"{API_URL}/admin/upload", files=files, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ PASS: Correctly rejected unauthorized request (401)")
            return True
        else:
            print(f"❌ FAIL: Expected 401, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False


def check_db_state():
    """Check final state of database"""
    print("\n[DB STATE CHECK] Checking final database state")
    
    try:
        # Check menu
        menu_response = requests.get(f"{API_URL}/menu", timeout=10)
        if menu_response.status_code == 200:
            menu = menu_response.json()
            print(f"\nFinal Menu State:")
            for category in ['fizz', 'white', 'orange', 'rose', 'red']:
                count = len(menu.get(category, []))
                print(f"  - {category}: {count} items")
                if count > 0:
                    print(f"    First item: {menu[category][0].get('name', 'N/A')}")
        
        # Check site config
        config_response = requests.get(f"{API_URL}/site-config", timeout=10)
        if config_response.status_code == 200:
            config = config_response.json()
            print(f"\nFinal Site Config State:")
            print(f"  - hero_tagline: {config.get('hero_tagline')}")
            print(f"  - since_year: {config.get('since_year')}")
            print(f"  - hero_image_url: {config.get('hero_image_url', 'N/A')[:60]}...")
        
        return True
    except Exception as e:
        print(f"Error checking DB state: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("VINO BY TONINO - BACKEND API TEST SUITE")
    print("=" * 80)
    
    results = []
    
    # Public endpoints
    results.append(("GET /api/menu", test_get_menu()))
    results.append(("GET /api/site-config", test_get_site_config()))
    
    # Admin login
    results.append(("POST /api/admin/login (correct)", test_admin_login_correct()))
    results.append(("POST /api/admin/login (incorrect)", test_admin_login_incorrect()))
    
    # Admin verify
    results.append(("GET /api/admin/verify (valid token)", test_admin_verify_with_token()))
    results.append(("GET /api/admin/verify (no token)", test_admin_verify_without_token()))
    results.append(("GET /api/admin/verify (invalid token)", test_admin_verify_invalid_token()))
    
    # Menu management
    results.append(("PUT /api/admin/menu (authorized)", test_update_menu()))
    results.append(("PUT /api/admin/menu (unauthorized)", test_update_menu_unauthorized()))
    
    # Site config management
    results.append(("PUT /api/admin/site-config (authorized)", test_update_site_config()))
    results.append(("PUT /api/admin/site-config (unauthorized)", test_update_site_config_unauthorized()))
    
    # File upload
    results.append(("POST /api/admin/upload (valid image)", test_upload_image_valid()))
    results.append(("POST /api/admin/upload (invalid type)", test_upload_image_invalid_type()))
    results.append(("POST /api/admin/upload (unauthorized)", test_upload_image_unauthorized()))
    
    # DB state check
    check_db_state()
    
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
