#!/usr/bin/env python3

import requests
import json
import sys
import io
from datetime import datetime

class SyroceCRMTester:
    def __init__(self):
        self.base_url = "https://web-generator-hotels.preview.emergentagent.com/api"
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        self.tests_run = 0
        self.tests_passed = 0
        self.token = None
        self.created_resources = {
            'clients': [],
            'projects': [],
            'templates': [],
            'versions': []
        }

    def log_test(self, name, success, response_data=None, error=None):
        """Log test result"""
        self.tests_run += 1
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {name}")
        
        if success:
            self.tests_passed += 1
            if response_data:
                print(f"    → Response: {str(response_data)[:100]}")
        else:
            print(f"    → Error: {error}")
        print()

    def test_api_request(self, method, endpoint, data=None, expected_status=200, files=None):
        """Make API request and validate response"""
        url = f"{self.base_url}/{endpoint}"
        try:
            # Set authorization header if token exists
            headers = {'Content-Type': 'application/json'}
            if self.token:
                headers['Authorization'] = f'Bearer {self.token}'
                
            if files:
                # For file uploads, don't set Content-Type (let requests set it)
                headers.pop('Content-Type', None)
            
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                if files:
                    response = requests.post(url, files=files, headers=headers)
                else:
                    response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            
            success = response.status_code == expected_status
            response_data = None
            
            if success:
                try:
                    response_data = response.json()
                except:
                    if response.headers.get('content-type', '').startswith('application/zip'):
                        response_data = "ZIP_FILE_CONTENT"
                    else:
                        response_data = response.text[:100] if response.text else "No content"
            
            return success, response_data, response.status_code, response.text
            
        except Exception as e:
            return False, None, None, str(e)

    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        success, data, status, error = self.test_api_request('GET', 'dashboard/stats')
        
        if success:
            # Check if stats have required fields
            required_fields = ['total_clients', 'total_projects', 'total_templates', 'status_distribution']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                self.log_test("Dashboard Stats - Structure", False, error=f"Missing fields: {missing_fields}")
                return False
                
            # Check if templates count is 30 (seeded templates)
            if data.get('total_templates', 0) >= 30:
                self.log_test("Dashboard Stats - Template Count", True, f"Templates: {data['total_templates']}")
            else:
                self.log_test("Dashboard Stats - Template Count", False, error=f"Expected >=30 templates, got {data.get('total_templates', 0)}")
                
            self.log_test("Dashboard Stats", True, data)
            return True
        else:
            self.log_test("Dashboard Stats", False, error=f"Status {status}: {error}")
            return False

    def test_templates_endpoint(self):
        """Test templates CRUD operations"""
        
        # Test GET all templates
        success, templates, status, error = self.test_api_request('GET', 'templates')
        if not success:
            self.log_test("Templates - GET All", False, error=f"Status {status}: {error}")
            return False
            
        if not isinstance(templates, list):
            self.log_test("Templates - GET All", False, error="Response is not a list")
            return False
            
        if len(templates) < 30:
            self.log_test("Templates - Count", False, error=f"Expected >=30 templates, got {len(templates)}")
        else:
            self.log_test("Templates - Count", True, f"Found {len(templates)} templates")
        
        # Test template structure
        if templates:
            template = templates[0]
            required_fields = ['id', 'name', 'category', 'description', 'thumbnail', 'theme', 'sections']
            missing_fields = [field for field in required_fields if field not in template]
            
            if missing_fields:
                self.log_test("Templates - Structure", False, error=f"Missing fields: {missing_fields}")
            else:
                self.log_test("Templates - Structure", True, "All required fields present")
        
        # Test category filtering
        categories = ['luxury', 'boutique', 'resort', 'business', 'beach', 'mountain', 'city']
        for category in categories[:3]:  # Test first 3 categories
            success, filtered, status, error = self.test_api_request('GET', f'templates?category={category}')
            if success and filtered:
                category_match = all(t.get('category') == category for t in filtered)
                self.log_test(f"Templates - Filter {category}", category_match, f"Found {len(filtered)} templates")
            else:
                self.log_test(f"Templates - Filter {category}", False, error=f"Status {status}")
        
        # Test GET single template
        if templates:
            template_id = templates[0]['id']
            success, template, status, error = self.test_api_request('GET', f'templates/{template_id}')
            self.log_test("Templates - GET Single", success, template.get('name') if success else error)
        
        self.log_test("Templates - GET All", True, f"Retrieved {len(templates)} templates")
        return True

    def test_clients_crud(self):
        """Test clients CRUD operations"""
        
        # Test GET clients (empty initially)
        success, clients, status, error = self.test_api_request('GET', 'clients')
        if not success:
            self.log_test("Clients - GET All", False, error=f"Status {status}: {error}")
            return False
        self.log_test("Clients - GET All", True, f"Retrieved {len(clients)} clients")
        
        # Test CREATE client
        test_client = {
            "hotel_name": "Test Hotel Istanbul",
            "contact_name": "Ahmet Test",
            "email": "test@hotel.com", 
            "phone": "+90 212 555 0123",
            "address": "Test Caddesi No:1",
            "city": "Istanbul",
            "notes": "Test client for API testing"
        }
        
        success, client, status, error = self.test_api_request('POST', 'clients', test_client, 200)
        if success:
            self.created_resources['clients'].append(client['id'])
            self.log_test("Clients - CREATE", True, f"Created client: {client['hotel_name']}")
            
            # Test GET single client
            client_id = client['id']
            success, retrieved_client, status, error = self.test_api_request('GET', f'clients/{client_id}')
            self.log_test("Clients - GET Single", success, retrieved_client.get('hotel_name') if success else error)
            
            # Test UPDATE client
            update_data = {"hotel_name": "Updated Test Hotel", "city": "Ankara"}
            success, updated, status, error = self.test_api_request('PUT', f'clients/{client_id}', update_data)
            if success and updated.get('hotel_name') == 'Updated Test Hotel':
                self.log_test("Clients - UPDATE", True, f"Updated: {updated['hotel_name']}")
            else:
                self.log_test("Clients - UPDATE", False, error=error)
                
        else:
            self.log_test("Clients - CREATE", False, error=f"Status {status}: {error}")
            return False
            
        # Test search functionality
        success, search_results, status, error = self.test_api_request('GET', 'clients?search=Test')
        if success:
            found_test_client = any('Test' in c.get('hotel_name', '') for c in search_results)
            self.log_test("Clients - SEARCH", found_test_client, f"Found {len(search_results)} results")
        else:
            self.log_test("Clients - SEARCH", False, error=error)
            
        return True

    def test_projects_crud(self):
        """Test projects CRUD operations"""
        
        # First get templates to create a project
        success, templates, status, error = self.test_api_request('GET', 'templates')
        if not success or not templates:
            self.log_test("Projects - Prerequisites", False, error="No templates available for project creation")
            return False
            
        template_id = templates[0]['id']
        
        # Test CREATE project
        test_project = {
            "name": "Test Hotel Website",
            "template_id": template_id
        }
        
        success, project, status, error = self.test_api_request('POST', 'projects', test_project, 200)
        if success:
            self.created_resources['projects'].append(project['id'])
            self.log_test("Projects - CREATE", True, f"Created project: {project['name']}")
            
            project_id = project['id']
            
            # Test GET single project  
            success, retrieved, status, error = self.test_api_request('GET', f'projects/{project_id}')
            self.log_test("Projects - GET Single", success, retrieved.get('name') if success else error)
            
            # Test UPDATE project
            update_data = {
                "name": "Updated Test Project",
                "status": "published"
            }
            success, updated, status, error = self.test_api_request('PUT', f'projects/{project_id}', update_data)
            if success:
                self.log_test("Projects - UPDATE", True, f"Updated: {updated.get('name')} - {updated.get('status')}")
            else:
                self.log_test("Projects - UPDATE", False, error=error)
                
            # Test project export (should return ZIP file)
            success, export_data, status, error = self.test_api_request('POST', f'projects/{project_id}/export')
            if success:
                # For binary data, check if we got content
                export_success = status == 200 and export_data is not None
                self.log_test("Projects - EXPORT", export_success, "ZIP file generated")
            else:
                self.log_test("Projects - EXPORT", False, error=f"Status {status}: {error}")
                
        else:
            self.log_test("Projects - CREATE", False, error=f"Status {status}: {error}")
            return False
            
        # Test GET all projects
        success, projects, status, error = self.test_api_request('GET', 'projects')
        if success:
            self.log_test("Projects - GET All", True, f"Retrieved {len(projects)} projects")
        else:
            self.log_test("Projects - GET All", False, error=error)
            
        return True

    def test_activity_log(self):
        """Test dashboard activity endpoint"""
        success, activities, status, error = self.test_api_request('GET', 'dashboard/activity')
        
        if success:
            if isinstance(activities, list):
                self.log_test("Activity Log", True, f"Retrieved {len(activities)} activities")
                
                # Check activity structure if any exist
                if activities:
                    activity = activities[0]
                    required_fields = ['id', 'type', 'message', 'created_at']
                    missing_fields = [field for field in required_fields if field not in activity]
                    
                    if missing_fields:
                        self.log_test("Activity Log - Structure", False, error=f"Missing fields: {missing_fields}")
                    else:
                        self.log_test("Activity Log - Structure", True, "Activity structure valid")
            else:
                self.log_test("Activity Log", False, error="Response is not a list")
        else:
            self.log_test("Activity Log", False, error=f"Status {status}: {error}")
        
        return success

    def cleanup_resources(self):
        """Clean up created test resources"""
        print("\n🧹 Cleaning up test resources...")
        
        # Delete created projects
        for project_id in self.created_resources['projects']:
            success, _, status, _ = self.test_api_request('DELETE', f'projects/{project_id}')
            if success:
                print(f"    Deleted project: {project_id}")
            else:
                print(f"    Failed to delete project: {project_id}")
        
        # Delete created clients  
        for client_id in self.created_resources['clients']:
            success, _, status, _ = self.test_api_request('DELETE', f'clients/{client_id}')
            if success:
                print(f"    Deleted client: {client_id}")
            else:
                print(f"    Failed to delete client: {client_id}")

    def run_all_tests(self):
        """Run all backend API tests"""
        print("🚀 Starting Syroce CRM Backend API Tests")
        print(f"📡 Backend URL: {self.base_url}")
        print("=" * 60)
        
        # Test basic connectivity
        success, _, status, error = self.test_api_request('GET', 'dashboard/stats')
        if not success:
            print(f"❌ Cannot connect to backend API: {error}")
            return 1
        
        try:
            # Run all tests
            self.test_dashboard_stats()
            self.test_templates_endpoint()
            self.test_clients_crud()
            self.test_projects_crud()
            self.test_activity_log()
            
        except Exception as e:
            print(f"❌ Test execution error: {e}")
            return 1
        finally:
            # Always cleanup
            self.cleanup_resources()
        
        # Print results
        print("=" * 60)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("✅ Backend API tests PASSED")
            return 0
        else:
            print("❌ Backend API tests FAILED")
            return 1

def main():
    tester = SyroceCRMTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())