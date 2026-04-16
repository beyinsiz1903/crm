#!/usr/bin/env python3
"""
Syroce CRM v3.1 Backend API Test Suite
Tests all newly added endpoints for CRM features including auth, profile, dashboard, leads, conversion, pagination, CSV export, bulk operations, notifications, and form auto-creation.
"""

import requests
import json
import csv
import io
import time
from typing import Dict, Any, List, Optional
import sys
import os

# Backend URL from frontend .env
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000/api")

class SyroceCRMTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_results = []
        self.created_leads = []
        self.created_form_id = None
        
    def log_result(self, test_name: str, success: bool, message: str, data: Any = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "data": data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}: {message}")
        if not success and data:
            print(f"   Error details: {data}")
    
    def set_auth_header(self):
        """Set authorization header for subsequent requests"""
        if self.token:
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
    
    def test_register(self):
        """Test user registration"""
        try:
            data = {
                "email": "testuser@test.com", 
                "password": "test123456", 
                "name": "Test User"
            }
            response = self.session.post(f"{BACKEND_URL}/auth/register", json=data)
            
            if response.status_code == 200:
                result = response.json()
                self.token = result.get("token")
                self.set_auth_header()
                self.log_result(
                    "User Registration", 
                    True, 
                    f"User registered successfully. Token obtained, role: {result.get('user', {}).get('role', 'unknown')}"
                )
                return True
            elif response.status_code == 400 and "zaten kayitli" in response.text:
                # User already exists, try login
                return self.test_login()
            else:
                self.log_result(
                    "User Registration", 
                    False, 
                    f"Registration failed with status {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("User Registration", False, f"Exception occurred: {str(e)}")
            return False
    
    def test_login(self):
        """Test user login (fallback if registration fails)"""
        try:
            data = {"email": "testuser@test.com", "password": "test123456"}
            response = self.session.post(f"{BACKEND_URL}/auth/login", json=data)
            
            if response.status_code == 200:
                result = response.json()
                self.token = result.get("token")
                self.set_auth_header()
                self.log_result("User Login", True, "Login successful, token obtained")
                return True
            else:
                self.log_result(
                    "User Login", 
                    False, 
                    f"Login failed with status {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("User Login", False, f"Exception occurred: {str(e)}")
            return False

    def test_profile_update(self):
        """Test profile name update"""
        try:
            data = {"name": "Updated Name"}
            response = self.session.put(f"{BACKEND_URL}/auth/profile", json=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("name") == "Updated Name":
                    self.log_result("Profile Update", True, "Profile name updated successfully")
                    return True
                else:
                    self.log_result("Profile Update", False, "Profile update returned but name not changed", result)
                    return False
            else:
                self.log_result(
                    "Profile Update", 
                    False, 
                    f"Profile update failed with status {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Profile Update", False, f"Exception occurred: {str(e)}")
            return False

    def test_password_change_success(self):
        """Test successful password change"""
        try:
            data = {"current_password": "test123456", "new_password": "newpass123"}
            response = self.session.put(f"{BACKEND_URL}/auth/change-password", json=data)
            
            if response.status_code == 200:
                self.log_result("Password Change (Success)", True, "Password changed successfully")
                return True
            else:
                self.log_result(
                    "Password Change (Success)", 
                    False, 
                    f"Password change failed with status {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Password Change (Success)", False, f"Exception occurred: {str(e)}")
            return False

    def test_password_change_fail(self):
        """Test password change with wrong current password"""
        try:
            data = {"current_password": "wrong", "new_password": "abc"}
            response = self.session.put(f"{BACKEND_URL}/auth/change-password", json=data)
            
            if response.status_code == 400:
                self.log_result("Password Change (Fail)", True, "Password change correctly rejected with wrong current password")
                return True
            else:
                self.log_result(
                    "Password Change (Fail)", 
                    False, 
                    f"Expected 400 error but got {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Password Change (Fail)", False, f"Exception occurred: {str(e)}")
            return False

    def test_dashboard_stats(self):
        """Test enhanced dashboard CRM metrics"""
        try:
            response = self.session.get(f"{BACKEND_URL}/dashboard/stats")
            
            if response.status_code == 200:
                result = response.json()
                required_fields = [
                    "total_leads", "conversion_rate", "avg_lead_score", 
                    "pipeline_summary", "active_campaigns", "total_communications"
                ]
                
                missing_fields = [field for field in required_fields if field not in result]
                
                if not missing_fields:
                    self.log_result(
                        "Dashboard Stats", 
                        True, 
                        f"Dashboard stats returned all required fields. Total leads: {result.get('total_leads', 0)}, "
                        f"Conversion rate: {result.get('conversion_rate', 0)}%, "
                        f"Avg score: {result.get('avg_lead_score', 0)}"
                    )
                    return True
                else:
                    self.log_result(
                        "Dashboard Stats", 
                        False, 
                        f"Missing required fields: {missing_fields}",
                        result
                    )
                    return False
            else:
                self.log_result(
                    "Dashboard Stats", 
                    False, 
                    f"Dashboard stats failed with status {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Dashboard Stats", False, f"Exception occurred: {str(e)}")
            return False

    def test_create_lead(self):
        """Test creating a lead for conversion testing"""
        try:
            data = {
                "name": "Test Lead",
                "email": "lead@test.com",
                "company": "Test Hotel",
                "source": "referral",
                "score": 50,
                "stage": "new",
                "tags": ["test"],
                "notes": "Test lead for conversion",
                "phone": "+90 555 123 4567"
            }
            response = self.session.post(f"{BACKEND_URL}/leads", json=data)
            
            if response.status_code == 200:
                result = response.json()
                lead_id = result.get("id")
                if lead_id:
                    self.created_leads.append(lead_id)
                    self.log_result("Lead Creation", True, f"Lead created successfully with ID: {lead_id}")
                    return lead_id
                else:
                    self.log_result("Lead Creation", False, "Lead creation returned success but no ID", result)
                    return None
            else:
                self.log_result(
                    "Lead Creation", 
                    False, 
                    f"Lead creation failed with status {response.status_code}",
                    response.text
                )
                return None
        except Exception as e:
            self.log_result("Lead Creation", False, f"Exception occurred: {str(e)}")
            return None

    def test_lead_conversion(self, lead_id: str):
        """Test converting lead to client"""
        try:
            response = self.session.post(f"{BACKEND_URL}/leads/{lead_id}/convert")
            
            if response.status_code == 200:
                result = response.json()
                client_id = result.get("client_id")
                if client_id:
                    self.log_result(
                        "Lead Conversion", 
                        True, 
                        f"Lead converted to client successfully. Client ID: {client_id}"
                    )
                    return True
                else:
                    self.log_result("Lead Conversion", False, "Conversion returned success but no client ID", result)
                    return False
            else:
                self.log_result(
                    "Lead Conversion", 
                    False, 
                    f"Lead conversion failed with status {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Lead Conversion", False, f"Exception occurred: {str(e)}")
            return False

    def test_pagination(self):
        """Test leads pagination"""
        try:
            response = self.session.get(f"{BACKEND_URL}/leads?page=1&limit=10")
            
            if response.status_code == 200:
                result = response.json()
                required_fields = ["items", "total", "page", "limit", "pages"]
                missing_fields = [field for field in required_fields if field not in result]
                
                if not missing_fields:
                    self.log_result(
                        "Pagination", 
                        True, 
                        f"Pagination working correctly. Total: {result.get('total')}, "
                        f"Page: {result.get('page')}, Limit: {result.get('limit')}, "
                        f"Pages: {result.get('pages')}"
                    )
                    return True
                else:
                    self.log_result(
                        "Pagination", 
                        False, 
                        f"Missing pagination fields: {missing_fields}",
                        result
                    )
                    return False
            else:
                self.log_result(
                    "Pagination", 
                    False, 
                    f"Pagination failed with status {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Pagination", False, f"Exception occurred: {str(e)}")
            return False

    def test_csv_export(self):
        """Test CSV export for leads"""
        try:
            response = self.session.get(f"{BACKEND_URL}/leads/export/csv")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'text/csv' in content_type:
                    # Try to parse the CSV content
                    csv_content = response.text
                    reader = csv.reader(io.StringIO(csv_content))
                    rows = list(reader)
                    
                    if len(rows) > 0:
                        headers = rows[0]
                        expected_headers = ["Ad", "Email", "Telefon", "Sirket", "Kaynak", "Asama", "Skor"]
                        has_expected = all(h in headers for h in expected_headers)
                        
                        if has_expected:
                            self.log_result(
                                "CSV Export", 
                                True, 
                                f"CSV export successful. {len(rows)-1} data rows, proper headers found"
                            )
                            return True
                        else:
                            self.log_result(
                                "CSV Export", 
                                False, 
                                f"CSV export missing expected headers. Got: {headers}"
                            )
                            return False
                    else:
                        self.log_result("CSV Export", True, "CSV export successful (empty file)")
                        return True
                else:
                    self.log_result(
                        "CSV Export", 
                        False, 
                        f"Expected CSV content-type but got: {content_type}"
                    )
                    return False
            else:
                self.log_result(
                    "CSV Export", 
                    False, 
                    f"CSV export failed with status {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("CSV Export", False, f"Exception occurred: {str(e)}")
            return False

    def test_bulk_operations(self):
        """Test bulk stage change operations"""
        try:
            # Create additional leads for bulk testing
            lead_ids = []
            for i in range(2):
                lead_data = {
                    "name": f"Bulk Test Lead {i+1}",
                    "email": f"bulk{i+1}@test.com",
                    "company": f"Bulk Hotel {i+1}",
                    "source": "website",
                    "score": 30,
                    "stage": "new",
                    "tags": ["bulk-test"],
                    "notes": f"Bulk test lead {i+1}"
                }
                response = self.session.post(f"{BACKEND_URL}/leads", json=lead_data)
                if response.status_code == 200:
                    result = response.json()
                    lead_id = result.get("id")
                    if lead_id:
                        lead_ids.append(lead_id)
                        self.created_leads.append(lead_id)
            
            if len(lead_ids) >= 2:
                # Test bulk stage change
                bulk_data = {"lead_ids": lead_ids, "stage": "contacted"}
                response = self.session.post(f"{BACKEND_URL}/leads/bulk/stage", json=bulk_data)
                
                if response.status_code == 200:
                    result = response.json()
                    message = result.get("message", "")
                    self.log_result(
                        "Bulk Operations", 
                        True, 
                        f"Bulk stage update successful: {message}"
                    )
                    return True
                else:
                    self.log_result(
                        "Bulk Operations", 
                        False, 
                        f"Bulk operations failed with status {response.status_code}",
                        response.text
                    )
                    return False
            else:
                self.log_result("Bulk Operations", False, "Could not create enough leads for bulk testing")
                return False
        except Exception as e:
            self.log_result("Bulk Operations", False, f"Exception occurred: {str(e)}")
            return False

    def test_notifications(self):
        """Test notifications endpoints"""
        try:
            # Test list notifications
            response = self.session.get(f"{BACKEND_URL}/notifications")
            
            if response.status_code == 200:
                notifications = response.json()
                self.log_result(
                    "Notifications List", 
                    True, 
                    f"Notifications list retrieved successfully. Count: {len(notifications)}"
                )
                
                # Test unread count
                response2 = self.session.get(f"{BACKEND_URL}/notifications/unread-count")
                if response2.status_code == 200:
                    count_result = response2.json()
                    if "count" in count_result:
                        self.log_result(
                            "Notifications Unread Count", 
                            True, 
                            f"Unread count retrieved: {count_result.get('count')}"
                        )
                        return True
                    else:
                        self.log_result(
                            "Notifications Unread Count", 
                            False, 
                            "Count field missing in response",
                            count_result
                        )
                        return False
                else:
                    self.log_result(
                        "Notifications Unread Count", 
                        False, 
                        f"Unread count failed with status {response2.status_code}",
                        response2.text
                    )
                    return False
            else:
                self.log_result(
                    "Notifications List", 
                    False, 
                    f"Notifications list failed with status {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Notifications", False, f"Exception occurred: {str(e)}")
            return False

    def test_form_creation_with_auto_lead(self):
        """Test form creation with auto_create_lead feature"""
        try:
            form_data = {
                "name": "Contact Form",
                "form_type": "contact",
                "auto_create_lead": True,
                "project_id": "",
                "fields": [
                    {"name": "name", "type": "text", "required": True},
                    {"name": "email", "type": "email", "required": True}
                ]
            }
            response = self.session.post(f"{BACKEND_URL}/forms", json=form_data)
            
            if response.status_code == 200:
                result = response.json()
                form_id = result.get("id")
                if form_id:
                    self.created_form_id = form_id
                    self.log_result(
                        "Form Creation", 
                        True, 
                        f"Form created successfully with auto_create_lead=True. Form ID: {form_id}"
                    )
                    return form_id
                else:
                    self.log_result("Form Creation", False, "Form creation returned success but no ID", result)
                    return None
            else:
                self.log_result(
                    "Form Creation", 
                    False, 
                    f"Form creation failed with status {response.status_code}",
                    response.text
                )
                return None
        except Exception as e:
            self.log_result("Form Creation", False, f"Exception occurred: {str(e)}")
            return None

    def test_form_submission_auto_lead(self, form_id: str):
        """Test form submission that should auto-create a lead"""
        try:
            # Count leads before submission
            response_before = self.session.get(f"{BACKEND_URL}/leads")
            leads_before = 0
            if response_before.status_code == 200:
                leads_data = response_before.json()
                if isinstance(leads_data, dict) and "items" in leads_data:
                    leads_before = len(leads_data["items"])
                elif isinstance(leads_data, list):
                    leads_before = len(leads_data)
            
            # Submit form (public endpoint, no auth)
            session_no_auth = requests.Session()  # New session without auth
            submission_data = {
                "fields": {
                    "name": "Form Lead",
                    "email": "formlead@test.com"
                }
            }
            response = session_no_auth.post(f"{BACKEND_URL}/forms/{form_id}/submit", json=submission_data)
            
            if response.status_code == 200:
                # Wait a moment for lead creation
                time.sleep(1)
                
                # Check if a new lead was created
                response_after = self.session.get(f"{BACKEND_URL}/leads?search=formlead@test.com")
                if response_after.status_code == 200:
                    leads_data = response_after.json()
                    leads_list = leads_data.get("items", []) if isinstance(leads_data, dict) else leads_data
                    
                    # Look for our form lead
                    form_lead = None
                    for lead in leads_list:
                        if lead.get("email") == "formlead@test.com":
                            form_lead = lead
                            break
                    
                    if form_lead:
                        # Check if lead has correct attributes
                        has_correct_source = form_lead.get("source") == "website"
                        has_form_tag = "form-submission" in form_lead.get("tags", [])
                        
                        if has_correct_source and has_form_tag:
                            self.log_result(
                                "Form Auto-Lead Creation", 
                                True, 
                                f"Form submission auto-created lead successfully. Lead name: {form_lead.get('name')}, "
                                f"Source: {form_lead.get('source')}, Tags: {form_lead.get('tags')}"
                            )
                            return True
                        else:
                            self.log_result(
                                "Form Auto-Lead Creation", 
                                False, 
                                f"Lead created but missing expected attributes. Source: {form_lead.get('source')}, "
                                f"Tags: {form_lead.get('tags')}"
                            )
                            return False
                    else:
                        self.log_result(
                            "Form Auto-Lead Creation", 
                            False, 
                            "Form submitted successfully but no lead was auto-created"
                        )
                        return False
                else:
                    self.log_result(
                        "Form Auto-Lead Creation", 
                        False, 
                        f"Could not verify lead creation. Status: {response_after.status_code}"
                    )
                    return False
            else:
                self.log_result(
                    "Form Auto-Lead Creation", 
                    False, 
                    f"Form submission failed with status {response.status_code}",
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Form Auto-Lead Creation", False, f"Exception occurred: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all backend tests in sequence"""
        print("🚀 Starting Syroce CRM v3.1 Backend Test Suite")
        print("=" * 60)
        
        # Step 1: Authentication
        if not self.test_register():
            print("❌ Authentication failed. Cannot continue tests.")
            return False
        
        # Step 2: Profile endpoints
        self.test_profile_update()
        self.test_password_change_success()
        self.test_password_change_fail()
        
        # Step 3: Dashboard
        self.test_dashboard_stats()
        
        # Step 4: Lead creation and conversion
        lead_id = self.test_create_lead()
        if lead_id:
            self.test_lead_conversion(lead_id)
        
        # Step 5: Pagination
        self.test_pagination()
        
        # Step 6: CSV Export
        self.test_csv_export()
        
        # Step 7: Bulk operations
        self.test_bulk_operations()
        
        # Step 8: Notifications
        self.test_notifications()
        
        # Step 9: Form with auto-create lead
        form_id = self.test_form_creation_with_auto_lead()
        if form_id:
            self.test_form_submission_auto_lead(form_id)
        
        # Summary
        self.print_summary()
        
        return True

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   - {result['test']}: {result['message']}")
        
        print(f"\n📝 Created {len(self.created_leads)} test leads during testing")
        if self.created_form_id:
            print(f"📄 Created 1 test form: {self.created_form_id}")
        
        print("\n🎯 All backend endpoints tested according to Syroce CRM v3.1 specifications")

if __name__ == "__main__":
    tester = SyroceCRMTester()
    tester.run_all_tests()