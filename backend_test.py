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

class BackendTester:
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
    
    async def run_all_tests(self):
        """Run all backend tests"""
        print(f"🧪 Starting Syroce CRM Backend API Tests")
        print(f"🎯 Backend URL: {self.base_url}")
        print("=" * 60)
        
        try:
            # Test 1: Languages endpoint
            await self.test_languages_endpoint()
            
            # Test 2: Existing endpoints
            await self.test_existing_endpoints()
            
            # Test 3: Get template for project creation
            self.template_id = await self.get_template_id()
            if not self.template_id:
                print("❌ Cannot continue tests without template ID")
                return False
            
            # Test 4: Create test project
            self.project_id = await self.create_test_project(self.template_id)
            if not self.project_id:
                print("❌ Cannot continue tests without project ID")
                return False
            
            # Test 5: Publish/Unpublish functionality
            await self.test_publish_unpublish(self.project_id)
            
            # Test 6: Project new fields (analytics, bundle_assets, language)
            await self.test_project_new_fields(self.project_id)
            
            # Test 7: Export with analytics
            await self.test_export_with_analytics(self.project_id)
            
            # Test 8: Booking section renderer
            await self.test_booking_renderer(self.project_id)
            
            # Cleanup
            await self.cleanup_test_project(self.project_id)
            
        except Exception as e:
            print(f"❌ Fatal error in test suite: {str(e)}")
        
        finally:
            await self.close()
        
        # Summary
        print("\n" + "=" * 60)
        print("🏁 TEST RESULTS SUMMARY")
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
    tester = BackendTester(BACKEND_URL)
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())