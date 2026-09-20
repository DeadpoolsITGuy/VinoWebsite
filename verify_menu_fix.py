#!/usr/bin/env python3
"""
Bug Fix Verification: Menu Default Data
Verifies that GET /api/menu returns the full DEFAULT_MENU after DB cleanup
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')
load_dotenv('/app/backend/.env')

BASE_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://vino-tonino.preview.emergentagent.com')
API_URL = f"{BASE_URL}/api"
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'vino2025')

print("=" * 80)
print("BUG FIX VERIFICATION: Menu Default Data")
print("=" * 80)
print(f"Testing API at: {API_URL}")
print()

# Expected minimum counts from DEFAULT_MENU
EXPECTED_COUNTS = {
    "fizz": 5,
    "white": 9,
    "orange": 1,
    "rose": 3,
    "red": 11
}

# Expected first items in each category
EXPECTED_FIRST_ITEMS = {
    "fizz": "Prosecco Extra Dry, Canal Grando, Italy",
    "white": "Blanc de Blanc, Château Oumsiyat, Lebanon",
    "orange": "Orange, No es Pituko, Chile",
    "rose": "Castelão Rosé, Cintila, Portugal",
    "red": "Rioja Alavesa, Mayela, Bideona, Spain"
}

def verify_menu_defaults():
    """Verify GET /api/menu returns full default wine list"""
    print("[VERIFICATION] GET /api/menu - Full Default Wine List")
    print("-" * 80)
    
    try:
        response = requests.get(f"{API_URL}/menu", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        menu = response.json()
        print(f"\nResponse Structure: {list(menu.keys())}")
        
        # Check all categories exist
        all_pass = True
        print("\n" + "=" * 80)
        print("CATEGORY VERIFICATION")
        print("=" * 80)
        
        for category in ['fizz', 'white', 'orange', 'rose', 'red']:
            if category not in menu:
                print(f"❌ {category.upper()}: MISSING")
                all_pass = False
                continue
            
            actual_count = len(menu[category])
            expected_count = EXPECTED_COUNTS[category]
            
            print(f"\n{category.upper()}:")
            print(f"  Expected: {expected_count} items")
            print(f"  Actual:   {actual_count} items")
            
            if actual_count < expected_count:
                print(f"  ❌ FAIL: Only {actual_count} items (expected at least {expected_count})")
                all_pass = False
            elif actual_count == 1:
                # Check if it's a placeholder
                first_item = menu[category][0].get('name', '')
                if 'placeholder' in first_item.lower() or 'test' in first_item.lower():
                    print(f"  ❌ FAIL: Appears to be placeholder data: '{first_item}'")
                    all_pass = False
                else:
                    print(f"  ⚠️  WARNING: Only 1 item, but not obviously a placeholder")
                    print(f"     First item: {first_item}")
            else:
                print(f"  ✅ PASS: {actual_count} items found")
            
            # Check first item name
            if actual_count > 0:
                first_item_name = menu[category][0].get('name', '')
                expected_first = EXPECTED_FIRST_ITEMS[category]
                
                print(f"  First item: {first_item_name}")
                
                if first_item_name == expected_first:
                    print(f"  ✅ First item matches expected default")
                else:
                    print(f"  ⚠️  First item differs from expected:")
                    print(f"     Expected: {expected_first}")
                    print(f"     Actual:   {first_item_name}")
                
                # Show price
                price = menu[category][0].get('price', 'N/A')
                print(f"  Price: {price}")
        
        print("\n" + "=" * 80)
        print("FULL MENU DETAILS")
        print("=" * 80)
        
        for category in ['fizz', 'white', 'orange', 'rose', 'red']:
            if category in menu and len(menu[category]) > 0:
                print(f"\n{category.upper()} ({len(menu[category])} items):")
                for i, item in enumerate(menu[category], 1):
                    print(f"  {i}. {item.get('name', 'N/A')} - {item.get('price', 'N/A')}")
        
        print("\n" + "=" * 80)
        if all_pass:
            print("✅ VERIFICATION PASSED: Full default menu is being returned")
            print("   The bug has been fixed - no placeholder data detected")
        else:
            print("❌ VERIFICATION FAILED: Menu does not contain full defaults")
            print("   The bug may still be present - check if DB doc was deleted")
        print("=" * 80)
        
        return all_pass
        
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def verify_admin_login():
    """Quick test of admin login to ensure it still works"""
    print("\n[VERIFICATION] POST /api/admin/login")
    print("-" * 80)
    
    try:
        payload = {"password": ADMIN_PASSWORD}
        response = requests.post(f"{API_URL}/admin/login", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data:
                token = data['token']
                print(f"Token received: {token[:20]}...")
                print("✅ PASS: Admin login functional")
                return True, token
            else:
                print(f"❌ FAIL: Response missing 'token' field")
                return False, None
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False, None
    except Exception as e:
        print(f"❌ FAIL: Exception - {str(e)}")
        return False, None


def verify_put_menu_functional(token):
    """Verify PUT /api/admin/menu is still functional (without corrupting DB)"""
    print("\n[VERIFICATION] PUT /api/admin/menu - Functional Check")
    print("-" * 80)
    print("NOTE: Skipping mutation test to avoid corrupting DB with test data")
    print("      The review request recommends skipping this to keep defaults in place")
    print("✅ SKIPPED: As per instructions to preserve default menu state")
    return True


def main():
    print("\n")
    
    # Step 1: Verify menu returns full defaults
    menu_pass = verify_menu_defaults()
    
    # Step 2: Verify admin login still works
    login_pass, token = verify_admin_login()
    
    # Step 3: Skip PUT test to avoid corrupting DB
    put_pass = verify_put_menu_functional(token)
    
    # Summary
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    print(f"1. Menu Default Data:     {'✅ PASS' if menu_pass else '❌ FAIL'}")
    print(f"2. Admin Login:           {'✅ PASS' if login_pass else '❌ FAIL'}")
    print(f"3. PUT /api/admin/menu:   {'✅ SKIPPED' if put_pass else '❌ FAIL'}")
    print("=" * 80)
    
    if menu_pass and login_pass:
        print("\n✅ BUG FIX VERIFIED: The menu now returns full default wine list")
        print("   All categories have the expected number of items")
        print("   No placeholder data detected")
        return True
    else:
        print("\n❌ BUG FIX NOT VERIFIED: Issues detected")
        if not menu_pass:
            print("   - Menu does not return full defaults")
        if not login_pass:
            print("   - Admin login not working")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
