#!/usr/bin/env python3
"""
Syroce CRM Backend API Test Suite
Tests section-presets (Block Library) endpoints for the hotel website builder.
"""

import sys
import json
import httpx
import asyncio
from typing import Dict, Any, Optional

# Use the frontend environment variable for backend URL
BACKEND_URL = "https://crm-lead-scoring.preview.emergentagent.com/api"

class SectionPresetsBackendTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results = {}
        self.created_presets = []  # Track created presets for cleanup
    
    async def close(self):
        await self.client.aclose()
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        print(f"{'✅' if success else '❌'} {test_name}: {details}")
        self.test_results[test_name] = {
            "success": success,
            "details": details
        }
    
    async def test_get_empty_section_presets(self):
        """Test 1: GET /api/section-presets - Should return empty list initially"""
        try:
            response = await self.client.get(f"{self.base_url}/section-presets")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    if len(data) == 0:
                        self.log_test("GET Empty Section Presets", True, "✅ Returns empty list initially")
                        return True
                    else:
                        # Clear existing presets first
                        for preset in data:
                            await self.client.delete(f"{self.base_url}/section-presets/{preset['id']}")
                        self.log_test("GET Empty Section Presets", True, f"✅ Cleaned {len(data)} existing presets, ready for testing")
                        return True
                else:
                    self.log_test("GET Empty Section Presets", False, f"❌ Expected list, got {type(data)}")
            else:
                self.log_test("GET Empty Section Presets", False, f"❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("GET Empty Section Presets", False, f"❌ Exception: {str(e)}")
        return False
    
    async def test_create_hero_preset(self):
        """Test 2: POST /api/section-presets - Create hero preset"""
        try:
            hero_preset_data = {
                "name": "Luks Hero Banner",
                "category": "hero",
                "section_type": "hero",
                "props": {
                    "title": "Test Hero",
                    "subtitle": "Test Subtitle"
                }
            }
            response = await self.client.post(f"{self.base_url}/section-presets", json=hero_preset_data)
            if response.status_code == 200:
                data = response.json()
                if all(key in data for key in ["id", "name", "category", "section_type", "props"]):
                    if (data["name"] == "Luks Hero Banner" and 
                        data["category"] == "hero" and
                        data["section_type"] == "hero" and
                        data["props"]["title"] == "Test Hero"):
                        self.created_presets.append(data["id"])
                        self.log_test("POST Hero Preset", True, f"✅ Created hero preset with ID: {data['id']}")
                        return data["id"]
                    else:
                        self.log_test("POST Hero Preset", False, "❌ Created preset has incorrect data")
                else:
                    self.log_test("POST Hero Preset", False, "❌ Response missing required fields")
            else:
                self.log_test("POST Hero Preset", False, f"❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("POST Hero Preset", False, f"❌ Exception: {str(e)}")
        return None
    
    async def test_create_contact_preset(self):
        """Test 4: POST /api/section-presets - Create contact preset"""
        try:
            contact_preset_data = {
                "name": "Standart Iletisim",
                "category": "iletisim",
                "section_type": "contact",
                "props": {
                    "title": "Bize Ulasin",
                    "phone": "+90 555 123"
                }
            }
            response = await self.client.post(f"{self.base_url}/section-presets", json=contact_preset_data)
            if response.status_code == 200:
                data = response.json()
                if all(key in data for key in ["id", "name", "category", "section_type", "props"]):
                    if (data["name"] == "Standart Iletisim" and 
                        data["category"] == "iletisim" and
                        data["section_type"] == "contact" and
                        data["props"]["title"] == "Bize Ulasin"):
                        self.created_presets.append(data["id"])
                        self.log_test("POST Contact Preset", True, f"✅ Created contact preset with ID: {data['id']}")
                        return data["id"]
                    else:
                        self.log_test("POST Contact Preset", False, "❌ Created preset has incorrect data")
                else:
                    self.log_test("POST Contact Preset", False, "❌ Response missing required fields")
            else:
                self.log_test("POST Contact Preset", False, f"❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("POST Contact Preset", False, f"❌ Exception: {str(e)}")
        return None
    
    async def test_get_all_presets(self):
        """Test 3: GET /api/section-presets - Should return both created presets"""
        try:
            response = await self.client.get(f"{self.base_url}/section-presets")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    if len(data) >= 2:
                        # Check if both presets exist
                        preset_names = [preset["name"] for preset in data]
                        if "Luks Hero Banner" in preset_names and "Standart Iletisim" in preset_names:
                            self.log_test("GET All Presets", True, f"✅ Returns {len(data)} presets including both created ones")
                            return True
                        else:
                            self.log_test("GET All Presets", False, f"❌ Missing expected presets. Found: {preset_names}")
                    else:
                        self.log_test("GET All Presets", False, f"❌ Expected at least 2 presets, got {len(data)}")
                else:
                    self.log_test("GET All Presets", False, f"❌ Expected list, got {type(data)}")
            else:
                self.log_test("GET All Presets", False, f"❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("GET All Presets", False, f"❌ Exception: {str(e)}")
        return False
    
    async def test_get_presets_by_category_hero(self):
        """Test 5: GET /api/section-presets?category=hero - Should return only hero preset"""
        try:
            response = await self.client.get(f"{self.base_url}/section-presets?category=hero")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    if len(data) >= 1:
                        # Check if only hero presets are returned
                        hero_presets = [preset for preset in data if preset["category"] == "hero"]
                        if len(hero_presets) == len(data):
                            hero_preset = next((p for p in data if p["name"] == "Luks Hero Banner"), None)
                            if hero_preset:
                                self.log_test("GET Hero Category Filter", True, f"✅ Returns {len(data)} hero preset(s), including 'Luks Hero Banner'")
                                return True
                            else:
                                self.log_test("GET Hero Category Filter", False, "❌ 'Luks Hero Banner' preset not found in hero category")
                        else:
                            self.log_test("GET Hero Category Filter", False, f"❌ Non-hero presets found in hero category filter")
                    else:
                        self.log_test("GET Hero Category Filter", False, f"❌ Expected at least 1 hero preset, got {len(data)}")
                else:
                    self.log_test("GET Hero Category Filter", False, f"❌ Expected list, got {type(data)}")
            else:
                self.log_test("GET Hero Category Filter", False, f"❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("GET Hero Category Filter", False, f"❌ Exception: {str(e)}")
        return False
    
    async def test_get_presets_by_section_type_contact(self):
        """Test 6: GET /api/section-presets?section_type=contact - Should return only contact preset"""
        try:
            response = await self.client.get(f"{self.base_url}/section-presets?section_type=contact")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    if len(data) >= 1:
                        # Check if only contact section_type presets are returned
                        contact_presets = [preset for preset in data if preset["section_type"] == "contact"]
                        if len(contact_presets) == len(data):
                            contact_preset = next((p for p in data if p["name"] == "Standart Iletisim"), None)
                            if contact_preset:
                                self.log_test("GET Contact Section Type Filter", True, f"✅ Returns {len(data)} contact preset(s), including 'Standart Iletisim'")
                                return True
                            else:
                                self.log_test("GET Contact Section Type Filter", False, "❌ 'Standart Iletisim' preset not found in contact section_type")
                        else:
                            self.log_test("GET Contact Section Type Filter", False, f"❌ Non-contact presets found in contact section_type filter")
                    else:
                        self.log_test("GET Contact Section Type Filter", False, f"❌ Expected at least 1 contact preset, got {len(data)}")
                else:
                    self.log_test("GET Contact Section Type Filter", False, f"❌ Expected list, got {type(data)}")
            else:
                self.log_test("GET Contact Section Type Filter", False, f"❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("GET Contact Section Type Filter", False, f"❌ Exception: {str(e)}")
        return False
    
    async def test_delete_preset(self):
        """Test 7: DELETE /api/section-presets/{id} - Delete one preset and verify"""
        try:
            if not self.created_presets:
                self.log_test("DELETE Preset", False, "❌ No presets to delete")
                return False
            
            preset_id = self.created_presets[0]  # Delete the first created preset
            response = await self.client.delete(f"{self.base_url}/section-presets/{preset_id}")
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    # Verify preset is deleted by trying to get all presets
                    get_response = await self.client.get(f"{self.base_url}/section-presets")
                    if get_response.status_code == 200:
                        presets = get_response.json()
                        deleted_preset_exists = any(preset["id"] == preset_id for preset in presets)
                        if not deleted_preset_exists:
                            self.created_presets.remove(preset_id)  # Remove from tracking
                            self.log_test("DELETE Preset", True, f"✅ Successfully deleted preset {preset_id}")
                            return True
                        else:
                            self.log_test("DELETE Preset", False, "❌ Preset still exists after delete")
                    else:
                        self.log_test("DELETE Preset", False, f"❌ Could not verify deletion: HTTP {get_response.status_code}")
                else:
                    self.log_test("DELETE Preset", False, "❌ Delete response missing message")
            else:
                self.log_test("DELETE Preset", False, f"❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("DELETE Preset", False, f"❌ Exception: {str(e)}")
        return False
    
    async def cleanup_remaining_presets(self):
        """Clean up any remaining test presets"""
        for preset_id in self.created_presets[:]:
            try:
                await self.client.delete(f"{self.base_url}/section-presets/{preset_id}")
                self.created_presets.remove(preset_id)
            except:
                pass
    
    async def run_section_presets_tests(self):
        """Run section presets tests in sequence"""
        print(f"🧪 Starting Section Presets (Block Library) Backend API Tests")
        print(f"🎯 Backend URL: {self.base_url}")
        print("=" * 60)
        
        try:
            # Test 1: GET empty list
            await self.test_get_empty_section_presets()
            
            # Test 2: Create hero preset
            hero_preset_id = await self.test_create_hero_preset()
            
            # Test 3: Get all presets (should have 1)
            if hero_preset_id:
                response = await self.client.get(f"{self.base_url}/section-presets")
                if response.status_code == 200:
                    data = response.json()
                    if len(data) == 1 and data[0]["name"] == "Luks Hero Banner":
                        self.log_test("GET After Hero Creation", True, "✅ Successfully returns hero preset after creation")
            
            # Test 4: Create contact preset
            contact_preset_id = await self.test_create_contact_preset()
            
            # Test 5: Get all presets (should have 2)
            await self.test_get_all_presets()
            
            # Test 6: Filter by category=hero
            await self.test_get_presets_by_category_hero()
            
            # Test 7: Filter by section_type=contact
            await self.test_get_presets_by_section_type_contact()
            
            # Test 8: Delete one preset
            await self.test_delete_preset()
            
            # Final verification: Should have 1 preset remaining
            final_response = await self.client.get(f"{self.base_url}/section-presets")
            if final_response.status_code == 200:
                final_data = final_response.json()
                if len(final_data) == 1:
                    self.log_test("Final Verification", True, f"✅ Correctly shows {len(final_data)} remaining preset after deletion")
                else:
                    self.log_test("Final Verification", False, f"❌ Expected 1 remaining preset, got {len(final_data)}")
            
            # Cleanup remaining presets
            await self.cleanup_remaining_presets()
            
        except Exception as e:
            print(f"❌ Fatal error in section presets test suite: {str(e)}")
        
        finally:
            await self.close()
        
        # Summary
        print("\n" + "=" * 60)
        print("🏁 SECTION PRESETS TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for test_name, result in self.test_results.items():
                if not result["success"]:
                    print(f"  • {test_name}: {result['details']}")
        
        return failed_tests == 0


async def main():
    """Main test runner"""
    tester = SectionPresetsBackendTester(BACKEND_URL)
    success = await tester.run_section_presets_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())