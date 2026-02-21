#!/usr/bin/env python3
"""
Syroce CRM Backend API Test Suite
Tests section-presets (Block Library) endpoints for the hotel website builder.
"""

import sys
import json
import httpx
import asyncio
import zipfile
import io
from typing import Dict, Any, Optional

# Use the frontend environment variable for backend URL
BACKEND_URL = "https://static-web-builder.preview.emergentagent.com/api"

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
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.project_id = None
        self.template_id = None
        self.test_results = {}
    
    async def close(self):
        await self.client.aclose()
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        print(f"{'✅' if success else '❌'} {test_name}: {details}")
        self.test_results[test_name] = {
            "success": success,
            "details": details
        }
    
    async def test_languages_endpoint(self):
        """Test GET /api/languages - should return 10 languages"""
        try:
            response = await self.client.get(f"{self.base_url}/languages")
            if response.status_code == 200:
                data = response.json()
                expected_langs = ["tr", "en", "de", "fr", "es", "it", "ru", "ar", "ja", "zh"]
                
                if isinstance(data, dict):
                    available_langs = list(data.keys())
                    if len(available_langs) == 10 and all(lang in available_langs for lang in expected_langs):
                        # Check structure
                        sample_lang = data.get("tr", {})
                        if all(key in sample_lang for key in ["name", "native", "flag"]):
                            self.log_test("Languages Endpoint", True, f"✅ Returns all 10 languages with proper structure")
                            return True
                        else:
                            self.log_test("Languages Endpoint", False, f"❌ Missing required fields in language data")
                    else:
                        self.log_test("Languages Endpoint", False, f"❌ Expected 10 languages {expected_langs}, got {available_langs}")
                else:
                    self.log_test("Languages Endpoint", False, f"❌ Expected dict response, got {type(data)}")
            else:
                self.log_test("Languages Endpoint", False, f"❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Languages Endpoint", False, f"❌ Exception: {str(e)}")
        return False
    
    async def test_existing_endpoints(self):
        """Test existing endpoints to ensure they still work"""
        tests = [
            ("GET /templates", "/templates"),
            ("GET /dashboard/stats", "/dashboard/stats"),
            ("GET /auth/check", "/auth/check")
        ]
        
        all_passed = True
        for test_name, endpoint in tests:
            try:
                response = await self.client.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    self.log_test(f"Existing Endpoint: {test_name}", True, f"✅ Status 200")
                else:
                    self.log_test(f"Existing Endpoint: {test_name}", False, f"❌ HTTP {response.status_code}")
                    all_passed = False
            except Exception as e:
                self.log_test(f"Existing Endpoint: {test_name}", False, f"❌ Exception: {str(e)}")
                all_passed = False
        
        return all_passed
    
    async def get_template_id(self) -> Optional[str]:
        """Get a template ID from the templates endpoint"""
        try:
            response = await self.client.get(f"{self.base_url}/templates")
            if response.status_code == 200:
                templates = response.json()
                if templates and len(templates) > 0:
                    template_id = templates[0]["id"]
                    self.log_test("Get Template ID", True, f"✅ Found template: {template_id}")
                    return template_id
                else:
                    self.log_test("Get Template ID", False, "❌ No templates available")
            else:
                self.log_test("Get Template ID", False, f"❌ HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Get Template ID", False, f"❌ Exception: {str(e)}")
        return None
    
    async def create_test_project(self, template_id: str) -> Optional[str]:
        """Create a test project for testing"""
        try:
            project_data = {
                "name": "Hotel Paradise Test",
                "template_id": template_id
            }
            response = await self.client.post(f"{self.base_url}/projects", json=project_data)
            
            if response.status_code == 200:
                project = response.json()
                project_id = project["id"]
                self.log_test("Create Test Project", True, f"✅ Created project: {project_id}")
                return project_id
            else:
                self.log_test("Create Test Project", False, f"❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Create Test Project", False, f"❌ Exception: {str(e)}")
        return None
    
    async def test_publish_unpublish(self, project_id: str):
        """Test publish/unpublish functionality"""
        try:
            # Test publish
            response = await self.client.post(f"{self.base_url}/projects/{project_id}/publish")
            if response.status_code == 200:
                data = response.json()
                if data.get("published") == True and "live_url" in data:
                    self.log_test("Publish Project", True, f"✅ Project published with live URL: {data['live_url']}")
                    
                    # Test hosted endpoint - should return HTML
                    hosted_response = await self.client.get(f"{self.base_url}/hosted/{project_id}")
                    if hosted_response.status_code == 200:
                        html_content = hosted_response.text
                        if "<!DOCTYPE html>" in html_content and "<html" in html_content:
                            self.log_test("Hosted Endpoint (Published)", True, f"✅ Returns valid HTML content ({len(html_content)} chars)")
                        else:
                            self.log_test("Hosted Endpoint (Published)", False, "❌ Invalid HTML response")
                            return False
                    else:
                        self.log_test("Hosted Endpoint (Published)", False, f"❌ HTTP {hosted_response.status_code}")
                        return False
                    
                    # Test unpublish
                    unpublish_response = await self.client.post(f"{self.base_url}/projects/{project_id}/unpublish")
                    if unpublish_response.status_code == 200:
                        unpublish_data = unpublish_response.json()
                        if unpublish_data.get("published") == False:
                            self.log_test("Unpublish Project", True, "✅ Project unpublished successfully")
                            
                            # Test hosted endpoint after unpublish - should return 403
                            hosted_after_unpublish = await self.client.get(f"{self.base_url}/hosted/{project_id}")
                            if hosted_after_unpublish.status_code == 403:
                                self.log_test("Hosted Endpoint (Unpublished)", True, "✅ Returns 403 after unpublish")
                                return True
                            else:
                                self.log_test("Hosted Endpoint (Unpublished)", False, f"❌ Expected 403, got {hosted_after_unpublish.status_code}")
                        else:
                            self.log_test("Unpublish Project", False, "❌ Project not properly unpublished")
                    else:
                        self.log_test("Unpublish Project", False, f"❌ HTTP {unpublish_response.status_code}")
                else:
                    self.log_test("Publish Project", False, "❌ Invalid publish response structure")
            else:
                self.log_test("Publish Project", False, f"❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Publish/Unpublish", False, f"❌ Exception: {str(e)}")
        return False
    
    async def test_project_new_fields(self, project_id: str):
        """Test updating project with new fields (analytics, bundle_assets, language)"""
        try:
            # Test analytics update
            analytics_data = {
                "analytics": {
                    "ga_id": "G-TEST123456",
                    "custom_head_code": "<script>console.log('Custom tracking code');</script>"
                }
            }
            response = await self.client.put(f"{self.base_url}/projects/{project_id}", json=analytics_data)
            if response.status_code == 200:
                self.log_test("Update Analytics", True, "✅ Analytics fields updated")
            else:
                self.log_test("Update Analytics", False, f"❌ HTTP {response.status_code}")
                return False
            
            # Test bundle_assets update
            bundle_data = {"bundle_assets": True}
            response = await self.client.put(f"{self.base_url}/projects/{project_id}", json=bundle_data)
            if response.status_code == 200:
                self.log_test("Update Bundle Assets", True, "✅ Bundle assets field updated")
            else:
                self.log_test("Update Bundle Assets", False, f"❌ HTTP {response.status_code}")
                return False
            
            # Test language update
            lang_data = {"language": "de"}
            response = await self.client.put(f"{self.base_url}/projects/{project_id}", json=lang_data)
            if response.status_code == 200:
                self.log_test("Update Language", True, "✅ Language field updated to German")
            else:
                self.log_test("Update Language", False, f"❌ HTTP {response.status_code}")
                return False
            
            # Verify all fields are stored correctly
            get_response = await self.client.get(f"{self.base_url}/projects/{project_id}")
            if get_response.status_code == 200:
                project = get_response.json()
                analytics = project.get("analytics", {})
                
                # Check all updated fields
                checks = [
                    (analytics.get("ga_id") == "G-TEST123456", "GA ID"),
                    ("<script>" in analytics.get("custom_head_code", ""), "Custom head code"),
                    (project.get("bundle_assets") == True, "Bundle assets"),
                    (project.get("language") == "de", "Language")
                ]
                
                all_good = all(check[0] for check in checks)
                if all_good:
                    self.log_test("Verify New Fields", True, "✅ All new fields stored correctly")
                    return True
                else:
                    failed_checks = [check[1] for check in checks if not check[0]]
                    self.log_test("Verify New Fields", False, f"❌ Failed verifications: {', '.join(failed_checks)}")
            else:
                self.log_test("Verify New Fields", False, f"❌ Could not retrieve project: HTTP {get_response.status_code}")
                
        except Exception as e:
            self.log_test("Project New Fields", False, f"❌ Exception: {str(e)}")
        return False
    
    async def test_export_with_analytics(self, project_id: str):
        """Test export functionality and check if analytics code is included"""
        try:
            response = await self.client.post(f"{self.base_url}/projects/{project_id}/export")
            
            if response.status_code == 200:
                # Check content type
                content_type = response.headers.get("content-type", "")
                if "application/zip" in content_type:
                    self.log_test("Export Content Type", True, "✅ Returns ZIP file")
                    
                    # Extract and check ZIP contents
                    zip_data = response.content
                    with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zf:
                        file_list = zf.namelist()
                        
                        # Find HTML file
                        html_files = [f for f in file_list if f.endswith('.html')]
                        if html_files:
                            html_file = html_files[0]
                            html_content = zf.read(html_file).decode('utf-8')
                            
                            # Check for analytics code
                            analytics_checks = [
                                ("G-TEST123456" in html_content, "Google Analytics ID"),
                                ("gtag(" in html_content, "Google Analytics script"),
                                ("console.log('Custom tracking code')" in html_content, "Custom tracking code")
                            ]
                            
                            passed_checks = [check[1] for check in analytics_checks if check[0]]
                            failed_checks = [check[1] for check in analytics_checks if not check[0]]
                            
                            if len(passed_checks) >= 2:  # At least 2 out of 3 should pass
                                self.log_test("Export Analytics Integration", True, f"✅ Analytics code found: {', '.join(passed_checks)}")
                                return True
                            else:
                                self.log_test("Export Analytics Integration", False, f"❌ Analytics code missing: {', '.join(failed_checks)}")
                        else:
                            self.log_test("Export Analytics Integration", False, "❌ No HTML file found in ZIP")
                else:
                    self.log_test("Export Content Type", False, f"❌ Expected ZIP, got {content_type}")
            else:
                self.log_test("Export Project", False, f"❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Export with Analytics", False, f"❌ Exception: {str(e)}")
        return False
    
    async def test_booking_renderer(self, project_id: str):
        """Test if booking section is properly rendered in the project"""
        try:
            # Add a booking section to the project
            booking_section = {
                "sections": [
                    {
                        "id": "booking-section",
                        "type": "booking",
                        "visible": True,
                        "props": {
                            "title": "Book Your Stay",
                            "subtitle": "Reserve your room today",
                            "phone": "+90 123 456 7890",
                            "email": "reservations@hotelparadise.com",
                            "roomTypes": ["Standard Room", "Deluxe Room", "Suite"]
                        }
                    }
                ]
            }
            
            update_response = await self.client.put(f"{self.base_url}/projects/{project_id}", json=booking_section)
            if update_response.status_code == 200:
                self.log_test("Add Booking Section", True, "✅ Booking section added to project")
                
                # Test preview to check if booking renders
                preview_response = await self.client.get(f"{self.base_url}/projects/{project_id}/preview")
                if preview_response.status_code == 200:
                    html_content = preview_response.text
                    
                    # Check for booking form elements
                    booking_checks = [
                        ("Book Your Stay" in html_content, "Booking title"),
                        ("reservations@hotelparadise.com" in html_content, "Email contact"),
                        ("+90 123 456 7890" in html_content, "Phone contact"),
                        ("Standard Room" in html_content, "Room types"),
                        ("booking-" in html_content.lower(), "Booking form elements")
                    ]
                    
                    passed_checks = [check[1] for check in booking_checks if check[0]]
                    
                    if len(passed_checks) >= 3:
                        self.log_test("Booking Section Renderer", True, f"✅ Booking section rendered: {', '.join(passed_checks)}")
                        return True
                    else:
                        failed_checks = [check[1] for check in booking_checks if not check[0]]
                        self.log_test("Booking Section Renderer", False, f"❌ Booking elements missing: {', '.join(failed_checks)}")
                else:
                    self.log_test("Booking Section Renderer", False, f"❌ Preview failed: HTTP {preview_response.status_code}")
            else:
                self.log_test("Add Booking Section", False, f"❌ HTTP {update_response.status_code}")
                
        except Exception as e:
            self.log_test("Booking Renderer", False, f"❌ Exception: {str(e)}")
        return False
    
    async def cleanup_test_project(self, project_id: str):
        """Clean up test project"""
        try:
            response = await self.client.delete(f"{self.base_url}/projects/{project_id}")
            if response.status_code == 200:
                self.log_test("Cleanup Test Project", True, "✅ Test project deleted")
            else:
                self.log_test("Cleanup Test Project", False, f"❌ HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Cleanup Test Project", False, f"❌ Exception: {str(e)}")
    
async def main():
    """Main test runner"""
    tester = SectionPresetsBackendTester(BACKEND_URL)
    success = await tester.run_section_presets_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())