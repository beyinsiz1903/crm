#!/usr/bin/env python3
"""
Syroce CRM v3.0 Backend API Testing Suite

Tests all new CRM endpoints including:
- Authentication (register, login, me)
- Leads CRUD + scoring + stage management
- Pipeline stages and board
- Communications timeline
- Campaigns (MOCK) - activate/pause
- Reports (overview, pipeline, leads, activity)
- Forms CRUD + submissions
- Blog posts CRUD
- Domain management (MOCK)
- Team management + RBAC
- Enhanced client model
- User model with roles
"""

import requests
import json
import sys
from datetime import datetime
import uuid

# Backend URL from environment
BASE_URL = "https://crm-lead-scoring.preview.emergentagent.com/api"

class CRMTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.user_id = None
        self.test_data = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.results = []
        
    def log(self, message, test_name="", status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if test_name:
            print(f"[{timestamp}] [{status}] {test_name}: {message}")
        else:
            print(f"[{timestamp}] [{status}] {message}")
        
    def test(self, test_name):
        """Decorator for test methods"""
        def decorator(func):
            def wrapper(self_inner, *args, **kwargs):
                self_inner.total_tests += 1
                self_inner.log(f"Starting test...", test_name, "TEST")
                try:
                    result = func(self_inner, *args, **kwargs)
                    self_inner.passed_tests += 1
                    self_inner.log(f"✅ PASSED", test_name, "PASS")
                    self_inner.results.append({"test": test_name, "status": "PASSED", "details": "Success"})
                    return result
                except Exception as e:
                    self_inner.failed_tests += 1
                    error_msg = str(e)
                    self_inner.log(f"❌ FAILED - {error_msg}", test_name, "FAIL")
                    self_inner.results.append({"test": test_name, "status": "FAILED", "details": error_msg})
                    return None
            return wrapper
        return decorator
    
    def make_request(self, method, endpoint, data=None, headers=None, expect_status=200):
        """Make HTTP request and validate response"""
        url = f"{self.base_url}{endpoint}"
        
        # Add auth header if token exists
        if self.token and headers is None:
            headers = {"Authorization": f"Bearer {self.token}"}
        elif self.token and headers:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                raise Exception(f"Unsupported HTTP method: {method}")
            
            # Validate status code
            if response.status_code != expect_status:
                raise Exception(f"Expected status {expect_status}, got {response.status_code}. Response: {response.text}")
            
            # Try to parse JSON response
            try:
                return response.json()
            except:
                return response.text
                
        except requests.exceptions.Timeout:
            raise Exception("Request timed out after 30 seconds")
        except requests.exceptions.ConnectionError:
            raise Exception("Could not connect to backend server")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")
    
    # ==================== AUTH TESTS ====================
    
    @test("User Registration")
    def test_register(self):
        """Test user registration - first user should become admin"""
        user_data = {
            "email": "admin@syroce.com",
            "password": "SecurePass123!",
            "name": "Admin User"
        }
        
        response = self.make_request("POST", "/auth/register", user_data, headers={})
        
        if not response or "token" not in response:
            raise Exception("Registration failed - no token returned")
        
        self.token = response["token"]
        user = response["user"]
        self.user_id = user["id"]
        
        # First user should be admin
        if user.get("role") != "admin":
            raise Exception(f"Expected admin role, got {user.get('role')}")
        
        self.test_data["admin_user"] = user
        return response
    
    @test("User Login")
    def test_login(self):
        """Test user login with registered credentials"""
        login_data = {
            "email": "admin@syroce.com",
            "password": "SecurePass123!"
        }
        
        response = self.make_request("POST", "/auth/login", login_data, headers={})
        
        if not response or "token" not in response:
            raise Exception("Login failed - no token returned")
        
        # Update token for subsequent requests
        self.token = response["token"]
        user = response["user"]
        
        if user.get("role") != "admin":
            raise Exception(f"Expected admin role, got {user.get('role')}")
        
        return response
    
    @test("Get Current User (/auth/me)")
    def test_get_me(self):
        """Test getting current user info - should include role field"""
        response = self.make_request("GET", "/auth/me")
        
        required_fields = ["id", "email", "name", "role"]
        for field in required_fields:
            if field not in response:
                raise Exception(f"Missing field '{field}' in user response")
        
        if response.get("role") != "admin":
            raise Exception(f"Expected admin role, got {response.get('role')}")
        
        return response
    
    # ==================== LEADS TESTS ====================
    
    @test("Create Lead with Auto-scoring")
    def test_create_lead(self):
        """Test creating a lead with automatic scoring"""
        lead_data = {
            "name": "John Doe",
            "email": "john.doe@company.com",
            "phone": "+1234567890",
            "company": "Acme Corporation",
            "source": "referral",
            "score": 0,  # Should be auto-calculated
            "stage": "new",
            "tags": ["premium", "hot-lead"],
            "notes": "Interested in premium package"
        }
        
        response = self.make_request("POST", "/leads", lead_data)
        
        # Verify lead was created
        if not response or "id" not in response:
            raise Exception("Lead creation failed - no ID returned")
        
        # Check auto-scoring: email(10) + phone(10) + company(10) + referral(20) = 50
        expected_score = 50
        if response.get("score") != expected_score:
            raise Exception(f"Auto-scoring failed. Expected {expected_score}, got {response.get('score')}")
        
        self.test_data["lead_id"] = response["id"]
        return response
    
    @test("List Leads with Filters")
    def test_list_leads(self):
        """Test listing leads with various filters"""
        # Test basic listing
        response = self.make_request("GET", "/leads")
        
        if not isinstance(response, list):
            raise Exception("Expected list of leads")
        
        if len(response) == 0:
            raise Exception("No leads found - expected at least 1 from creation test")
        
        # Test stage filter
        stage_response = self.make_request("GET", "/leads?stage=new")
        if not isinstance(stage_response, list):
            raise Exception("Stage filter failed")
        
        # Test source filter  
        source_response = self.make_request("GET", "/leads?source=referral")
        if not isinstance(source_response, list):
            raise Exception("Source filter failed")
        
        # Test search
        search_response = self.make_request("GET", "/leads?search=John")
        if not isinstance(search_response, list):
            raise Exception("Search filter failed")
        
        return response
    
    @test("Update Lead Stage")
    def test_update_lead_stage(self):
        """Test changing lead stage"""
        if "lead_id" not in self.test_data:
            raise Exception("No lead ID available - create lead test must run first")
        
        lead_id = self.test_data["lead_id"]
        stage_data = {"stage": "contacted"}
        
        response = self.make_request("PUT", f"/leads/{lead_id}/stage", stage_data)
        
        if response.get("stage") != "contacted":
            raise Exception(f"Stage update failed. Expected 'contacted', got {response.get('stage')}")
        
        return response
    
    @test("Update Lead Score")
    def test_update_lead_score(self):
        """Test changing lead score"""
        if "lead_id" not in self.test_data:
            raise Exception("No lead ID available - create lead test must run first")
        
        lead_id = self.test_data["lead_id"]
        score_data = {"score": 80}
        
        response = self.make_request("PUT", f"/leads/{lead_id}/score", score_data)
        
        if response.get("score") != 80:
            raise Exception(f"Score update failed. Expected 80, got {response.get('score')}")
        
        return response
    
    @test("Update Lead (General)")
    def test_update_lead(self):
        """Test updating lead information"""
        if "lead_id" not in self.test_data:
            raise Exception("No lead ID available - create lead test must run first")
        
        lead_id = self.test_data["lead_id"]
        update_data = {
            "notes": "Updated notes - showed high interest",
            "tags": ["premium", "hot-lead", "follow-up"]
        }
        
        response = self.make_request("PUT", f"/leads/{lead_id}", update_data)
        
        if "Updated notes" not in response.get("notes", ""):
            raise Exception("Lead update failed - notes not updated")
        
        return response
    
    # ==================== PIPELINE TESTS ====================
    
    @test("Get Pipeline Stages (Auto-seed)")
    def test_pipeline_stages(self):
        """Test getting pipeline stages - should auto-seed 7 defaults"""
        response = self.make_request("GET", "/pipeline/stages")
        
        if not isinstance(response, list):
            raise Exception("Expected list of pipeline stages")
        
        # Should have 7 default stages
        if len(response) != 7:
            raise Exception(f"Expected 7 default stages, got {len(response)}")
        
        # Verify stage structure
        required_fields = ["id", "name", "key", "order", "color"]
        for stage in response:
            for field in required_fields:
                if field not in stage:
                    raise Exception(f"Missing field '{field}' in stage")
        
        # Check specific stages exist
        stage_keys = [s.get("key") for s in response]
        expected_keys = ["new", "contacted", "qualified", "proposal", "negotiation", "won", "lost"]
        for key in expected_keys:
            if key not in stage_keys:
                raise Exception(f"Missing expected stage: {key}")
        
        return response
    
    @test("Get Pipeline Board")
    def test_pipeline_board(self):
        """Test getting Kanban board data"""
        response = self.make_request("GET", "/pipeline/board")
        
        if not isinstance(response, dict):
            raise Exception("Expected pipeline board object")
        
        # Should have entries for each stage
        expected_stages = ["new", "contacted", "qualified", "proposal", "negotiation", "won", "lost"]
        for stage in expected_stages:
            if stage not in response:
                raise Exception(f"Missing stage in board: {stage}")
            
            stage_data = response[stage]
            required_fields = ["stage", "leads", "total_value"]
            for field in required_fields:
                if field not in stage_data:
                    raise Exception(f"Missing field '{field}' in stage data")
        
        return response
    
    # ==================== COMMUNICATIONS TESTS ====================
    
    @test("Create Communication")
    def test_create_communication(self):
        """Test creating communication entry"""
        if "lead_id" not in self.test_data:
            raise Exception("No lead ID available - create lead test must run first")
        
        comm_data = {
            "entity_type": "lead",
            "entity_id": self.test_data["lead_id"],
            "comm_type": "email",
            "subject": "Initial Contact",
            "content": "Sent welcome email with company information",
            "direction": "outbound"
        }
        
        response = self.make_request("POST", "/communications", comm_data)
        
        if not response or "id" not in response:
            raise Exception("Communication creation failed - no ID returned")
        
        self.test_data["communication_id"] = response["id"]
        
        # Verify communication data
        if response.get("entity_type") != "lead":
            raise Exception("Communication entity_type mismatch")
        
        if response.get("comm_type") != "email":
            raise Exception("Communication type mismatch")
        
        return response
    
    @test("List Communications")
    def test_list_communications(self):
        """Test listing communications with filters"""
        if "lead_id" not in self.test_data:
            raise Exception("No lead ID available - create lead test must run first")
        
        lead_id = self.test_data["lead_id"]
        
        # List all communications
        response = self.make_request("GET", "/communications")
        
        if not isinstance(response, list):
            raise Exception("Expected list of communications")
        
        # List communications for specific entity
        entity_response = self.make_request("GET", f"/communications?entity_type=lead&entity_id={lead_id}")
        
        if not isinstance(entity_response, list):
            raise Exception("Entity filter failed")
        
        # Should have at least 1 communication from creation test
        if len(entity_response) == 0:
            raise Exception("No communications found for lead")
        
        return response
    
    # ==================== CAMPAIGNS TESTS (MOCK) ====================
    
    @test("Create Campaign")
    def test_create_campaign(self):
        """Test creating email campaign (MOCK)"""
        campaign_data = {
            "name": "Welcome Series",
            "subject": "Welcome to Our Service!",
            "content": "Thank you for joining us. Here's what you can expect...",
            "campaign_type": "single",
            "recipient_filter": {"stage": "new"},
            "steps": []
        }
        
        response = self.make_request("POST", "/campaigns", campaign_data)
        
        if not response or "id" not in response:
            raise Exception("Campaign creation failed - no ID returned")
        
        self.test_data["campaign_id"] = response["id"]
        
        # Verify campaign data
        if response.get("name") != campaign_data["name"]:
            raise Exception("Campaign name mismatch")
        
        if response.get("status") != "draft":
            raise Exception("Campaign should start in draft status")
        
        return response
    
    @test("List Campaigns")
    def test_list_campaigns(self):
        """Test listing campaigns"""
        response = self.make_request("GET", "/campaigns")
        
        if not isinstance(response, list):
            raise Exception("Expected list of campaigns")
        
        # Should have at least 1 campaign from creation test
        if len(response) == 0:
            raise Exception("No campaigns found")
        
        return response
    
    @test("Activate Campaign (MOCK)")
    def test_activate_campaign(self):
        """Test activating campaign - should generate mock stats"""
        if "campaign_id" not in self.test_data:
            raise Exception("No campaign ID available - create campaign test must run first")
        
        campaign_id = self.test_data["campaign_id"]
        
        response = self.make_request("POST", f"/campaigns/{campaign_id}/activate")
        
        if response.get("status") != "active":
            raise Exception("Campaign activation failed - status not active")
        
        # Should have mock stats
        stats = response.get("stats", {})
        if not stats or "sent" not in stats:
            raise Exception("Campaign activation failed - no mock stats generated")
        
        # Stats should be reasonable numbers
        sent_count = stats.get("sent", 0)
        if sent_count <= 0:
            raise Exception("Campaign mock stats invalid - sent count should be > 0")
        
        return response
    
    @test("Pause Campaign")
    def test_pause_campaign(self):
        """Test pausing campaign"""
        if "campaign_id" not in self.test_data:
            raise Exception("No campaign ID available - create campaign test must run first")
        
        campaign_id = self.test_data["campaign_id"]
        
        response = self.make_request("POST", f"/campaigns/{campaign_id}/pause")
        
        if response.get("status") != "paused":
            raise Exception("Campaign pause failed - status not paused")
        
        return response
    
    # ==================== REPORTS TESTS ====================
    
    @test("Reports Overview")
    def test_reports_overview(self):
        """Test reports overview endpoint"""
        response = self.make_request("GET", "/reports/overview")
        
        if not isinstance(response, dict):
            raise Exception("Expected reports overview object")
        
        # Check required metrics
        required_metrics = [
            "total_leads", "won_leads", "lost_leads", "conversion_rate",
            "total_clients", "total_projects", "total_campaigns", "active_campaigns",
            "total_communications", "avg_lead_score", "recent_activities",
            "source_distribution", "stage_distribution"
        ]
        
        for metric in required_metrics:
            if metric not in response:
                raise Exception(f"Missing metric in overview: {metric}")
        
        # Verify data types
        if not isinstance(response["source_distribution"], dict):
            raise Exception("source_distribution should be a dict")
        
        if not isinstance(response["stage_distribution"], dict):
            raise Exception("stage_distribution should be a dict")
        
        return response
    
    @test("Reports Pipeline")
    def test_reports_pipeline(self):
        """Test pipeline report endpoint"""
        response = self.make_request("GET", "/reports/pipeline")
        
        if not isinstance(response, list):
            raise Exception("Expected pipeline report list")
        
        # Should have entries for each stage
        if len(response) != 7:
            raise Exception(f"Expected 7 pipeline stages, got {len(response)}")
        
        # Verify structure
        for stage in response:
            required_fields = ["name", "key", "color", "count"]
            for field in required_fields:
                if field not in stage:
                    raise Exception(f"Missing field '{field}' in pipeline stage")
        
        return response
    
    @test("Reports Leads")
    def test_reports_leads(self):
        """Test leads report endpoint"""
        response = self.make_request("GET", "/reports/leads")
        
        if not isinstance(response, dict):
            raise Exception("Expected leads report object")
        
        required_sections = ["monthly_trend", "source_data", "score_distribution"]
        for section in required_sections:
            if section not in response:
                raise Exception(f"Missing section in leads report: {section}")
        
        # Verify data types
        if not isinstance(response["monthly_trend"], list):
            raise Exception("monthly_trend should be a list")
        
        if not isinstance(response["source_data"], list):
            raise Exception("source_data should be a list")
        
        if not isinstance(response["score_distribution"], list):
            raise Exception("score_distribution should be a list")
        
        return response
    
    @test("Reports Activity")
    def test_reports_activity(self):
        """Test activity report endpoint"""
        response = self.make_request("GET", "/reports/activity")
        
        if not isinstance(response, dict):
            raise Exception("Expected activity report object")
        
        required_fields = ["total", "by_type", "daily", "recent"]
        for field in required_fields:
            if field not in response:
                raise Exception(f"Missing field in activity report: {field}")
        
        # Verify data types
        if not isinstance(response["by_type"], dict):
            raise Exception("by_type should be a dict")
        
        if not isinstance(response["daily"], list):
            raise Exception("daily should be a list")
        
        if not isinstance(response["recent"], list):
            raise Exception("recent should be a list")
        
        return response
    
    # ==================== FORMS TESTS ====================
    
    @test("Create Form")
    def test_create_form(self):
        """Test creating form"""
        form_data = {
            "name": "Contact Form",
            "form_type": "contact",
            "fields": [
                {"type": "text", "label": "Name", "required": True},
                {"type": "email", "label": "Email", "required": True},
                {"type": "textarea", "label": "Message", "required": False}
            ]
        }
        
        response = self.make_request("POST", "/forms", form_data)
        
        if not response or "id" not in response:
            raise Exception("Form creation failed - no ID returned")
        
        self.test_data["form_id"] = response["id"]
        
        # Verify form data
        if response.get("name") != form_data["name"]:
            raise Exception("Form name mismatch")
        
        if len(response.get("fields", [])) != 3:
            raise Exception("Form fields count mismatch")
        
        return response
    
    @test("List Forms")
    def test_list_forms(self):
        """Test listing forms"""
        response = self.make_request("GET", "/forms")
        
        if not isinstance(response, list):
            raise Exception("Expected list of forms")
        
        # Should have at least 1 form from creation test
        if len(response) == 0:
            raise Exception("No forms found")
        
        return response
    
    @test("Submit Form (Public)")
    def test_submit_form(self):
        """Test form submission (public endpoint - no auth)"""
        if "form_id" not in self.test_data:
            raise Exception("No form ID available - create form test must run first")
        
        form_id = self.test_data["form_id"]
        submission_data = {
            "fields": {
                "Name": "Jane Smith",
                "Email": "jane.smith@example.com",
                "Message": "I'm interested in your services"
            }
        }
        
        # Remove auth header for public endpoint
        response = self.make_request("POST", f"/forms/{form_id}/submit", submission_data, headers={})
        
        if not response or "id" not in response:
            raise Exception("Form submission failed - no ID returned")
        
        self.test_data["submission_id"] = response["id"]
        
        if "basariyla" not in response.get("message", ""):
            raise Exception("Form submission success message not found")
        
        return response
    
    @test("Get Form Submissions")
    def test_get_form_submissions(self):
        """Test getting form submissions"""
        if "form_id" not in self.test_data:
            raise Exception("No form ID available - create form test must run first")
        
        form_id = self.test_data["form_id"]
        
        response = self.make_request("GET", f"/forms/{form_id}/submissions")
        
        if not isinstance(response, list):
            raise Exception("Expected list of submissions")
        
        # Should have at least 1 submission from submit test
        if len(response) == 0:
            raise Exception("No submissions found")
        
        return response
    
    # ==================== BLOG TESTS ====================
    
    @test("Create Blog Post")
    def test_create_blog_post(self):
        """Test creating blog post"""
        blog_data = {
            "project_id": "",  # Empty for system blog
            "title": "Getting Started with CRM",
            "content": "This is a comprehensive guide on how to use our CRM system effectively...",
            "excerpt": "Learn the basics of CRM management",
            "tags": ["crm", "guide", "tutorial"],
            "status": "draft"
        }
        
        response = self.make_request("POST", "/blog/posts", blog_data)
        
        if not response or "id" not in response:
            raise Exception("Blog post creation failed - no ID returned")
        
        self.test_data["blog_post_id"] = response["id"]
        
        # Verify blog data
        if response.get("title") != blog_data["title"]:
            raise Exception("Blog title mismatch")
        
        # Should auto-generate slug
        if not response.get("slug"):
            raise Exception("Blog slug not auto-generated")
        
        return response
    
    @test("List Blog Posts")
    def test_list_blog_posts(self):
        """Test listing blog posts"""
        response = self.make_request("GET", "/blog/posts")
        
        if not isinstance(response, list):
            raise Exception("Expected list of blog posts")
        
        # Should have at least 1 post from creation test
        if len(response) == 0:
            raise Exception("No blog posts found")
        
        return response
    
    @test("Update Blog Post")
    def test_update_blog_post(self):
        """Test updating blog post (publish)"""
        if "blog_post_id" not in self.test_data:
            raise Exception("No blog post ID available - create blog post test must run first")
        
        blog_post_id = self.test_data["blog_post_id"]
        update_data = {"status": "published"}
        
        response = self.make_request("PUT", f"/blog/posts/{blog_post_id}", update_data)
        
        if response.get("status") != "published":
            raise Exception("Blog post status update failed")
        
        return response
    
    # ==================== TEAM TESTS ====================
    
    @test("List Team")
    def test_list_team(self):
        """Test listing team members"""
        response = self.make_request("GET", "/team")
        
        if not isinstance(response, list):
            raise Exception("Expected list of team members")
        
        # Should have at least 1 user (admin from registration)
        if len(response) == 0:
            raise Exception("No team members found")
        
        # Check admin user exists
        admin_found = False
        for user in response:
            if user.get("role") == "admin":
                admin_found = True
                break
        
        if not admin_found:
            raise Exception("Admin user not found in team list")
        
        return response
    
    @test("Invite Team Member")
    def test_invite_team_member(self):
        """Test inviting team member"""
        invite_data = {
            "email": "editor@test.com",
            "name": "Editor User",
            "role": "editor"
        }
        
        response = self.make_request("POST", "/team/invite", invite_data)
        
        if not response or "id" not in response:
            raise Exception("Team invite failed - no ID returned")
        
        self.test_data["editor_user_id"] = response["id"]
        
        # Should return temporary password
        if not response.get("temp_password"):
            raise Exception("Team invite should return temporary password")
        
        if response.get("role") != "editor":
            raise Exception("Team invite role mismatch")
        
        return response
    
    # ==================== CLIENT MODEL TESTS ====================
    
    @test("Create Client with Tags and Category")
    def test_create_client_enhanced(self):
        """Test creating client with new fields (tags, category, custom_fields)"""
        client_data = {
            "hotel_name": "Luxury Resort & Spa",
            "contact_name": "Michael Johnson",
            "email": "michael@luxuryresort.com",
            "phone": "+1-555-0123",
            "city": "Miami",
            "tags": ["premium", "vip", "high-value"],
            "category": "luxury",
            "custom_fields": {
                "property_type": "resort",
                "room_count": 150,
                "annual_revenue": 5000000
            }
        }
        
        response = self.make_request("POST", "/clients", client_data)
        
        if not response or "id" not in response:
            raise Exception("Client creation failed - no ID returned")
        
        self.test_data["client_id"] = response["id"]
        
        # Verify enhanced fields
        if not isinstance(response.get("tags"), list):
            raise Exception("Client tags should be a list")
        
        if len(response.get("tags", [])) != 3:
            raise Exception("Client tags count mismatch")
        
        if response.get("category") != "luxury":
            raise Exception("Client category mismatch")
        
        if not isinstance(response.get("custom_fields"), dict):
            raise Exception("Client custom_fields should be a dict")
        
        return response
    
    # ==================== CLEANUP TESTS ====================
    
    @test("Delete Test Data")
    def test_cleanup(self):
        """Clean up test data"""
        cleanup_count = 0
        
        # Delete lead
        if "lead_id" in self.test_data:
            try:
                self.make_request("DELETE", f"/leads/{self.test_data['lead_id']}")
                cleanup_count += 1
            except:
                pass
        
        # Delete campaign  
        if "campaign_id" in self.test_data:
            try:
                self.make_request("DELETE", f"/campaigns/{self.test_data['campaign_id']}")
                cleanup_count += 1
            except:
                pass
        
        # Delete form
        if "form_id" in self.test_data:
            try:
                self.make_request("DELETE", f"/forms/{self.test_data['form_id']}")
                cleanup_count += 1
            except:
                pass
        
        # Delete blog post
        if "blog_post_id" in self.test_data:
            try:
                self.make_request("DELETE", f"/blog/posts/{self.test_data['blog_post_id']}")
                cleanup_count += 1
            except:
                pass
        
        # Note: Don't delete client, user accounts as they may be needed for other tests
        
        self.log(f"Cleaned up {cleanup_count} test records", "Cleanup", "INFO")
        return {"cleaned_up": cleanup_count}
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("=" * 80)
        print("🚀 SYROCE CRM v3.0 BACKEND API TESTING SUITE")
        print(f"🌐 Backend URL: {self.base_url}")
        print("=" * 80)
        
        # Authentication Tests
        print("\n🔐 AUTHENTICATION TESTS")
        print("-" * 40)
        self.test_register()
        self.test_login()
        self.test_get_me()
        
        # Leads Tests
        print("\n👥 LEADS CRUD TESTS")
        print("-" * 40)
        self.test_create_lead()
        self.test_list_leads()
        self.test_update_lead_stage()
        self.test_update_lead_score()
        self.test_update_lead()
        
        # Pipeline Tests
        print("\n📊 PIPELINE TESTS")
        print("-" * 40)
        self.test_pipeline_stages()
        self.test_pipeline_board()
        
        # Communications Tests
        print("\n💬 COMMUNICATIONS TESTS")
        print("-" * 40)
        self.test_create_communication()
        self.test_list_communications()
        
        # Campaigns Tests (MOCK)
        print("\n📧 CAMPAIGNS TESTS (MOCK)")
        print("-" * 40)
        self.test_create_campaign()
        self.test_list_campaigns()
        self.test_activate_campaign()
        self.test_pause_campaign()
        
        # Reports Tests
        print("\n📈 REPORTS TESTS")
        print("-" * 40)
        self.test_reports_overview()
        self.test_reports_pipeline()
        self.test_reports_leads()
        self.test_reports_activity()
        
        # Forms Tests
        print("\n📋 FORMS TESTS")
        print("-" * 40)
        self.test_create_form()
        self.test_list_forms()
        self.test_submit_form()
        self.test_get_form_submissions()
        
        # Blog Tests
        print("\n📝 BLOG TESTS")
        print("-" * 40)
        self.test_create_blog_post()
        self.test_list_blog_posts()
        self.test_update_blog_post()
        
        # Team Tests
        print("\n👨‍💼 TEAM MANAGEMENT TESTS")
        print("-" * 40)
        self.test_list_team()
        self.test_invite_team_member()
        
        # Enhanced Models Tests
        print("\n🏢 ENHANCED CLIENT MODEL TESTS")
        print("-" * 40)
        self.test_create_client_enhanced()
        
        # Cleanup
        print("\n🧹 CLEANUP")
        print("-" * 40)
        self.test_cleanup()
        
        # Final Summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📈 Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        if self.failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.results:
                if result["status"] == "FAILED":
                    print(f"  • {result['test']}: {result['details']}")
        
        print("=" * 80)
        return {
            "total": self.total_tests,
            "passed": self.passed_tests,
            "failed": self.failed_tests,
            "success_rate": round(self.passed_tests/self.total_tests*100, 1)
        }

if __name__ == "__main__":
    tester = CRMTester()
    results = tester.run_all_tests()
    
    # Exit with error code if tests failed
    sys.exit(0 if results["failed"] == 0 else 1)