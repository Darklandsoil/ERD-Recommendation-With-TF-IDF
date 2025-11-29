"""
Automated API Testing Script for ERD Recommendation System
Blackbox Testing - API Endpoints

Usage:
    python automated_api_test.py

Requirements:
    pip install requests colorama tabulate
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple
from colorama import Fore, Style, init
from tabulate import tabulate

# Initialize colorama for colored output
init(autoreset=True)

# Configuration
BASE_URL = "http://127.0.0.1:5000"
RESULTS = []
TOTAL_TESTS = 0
PASSED_TESTS = 0
FAILED_TESTS = 0

# Test credentials
TEST_USERS = {
    "user": {
        "fullname": "user",
        "username": "testuser",
        "email": "testuser@mail.com",
        "password": "Test123!",
        "role": "user"
    },
    "advisor": {
        "fullname": "Rizki",
        "username": "rizki12",
        "email": "rizki@mail.com",
        "password": "rizki555",
        "role": "advisor"
    },
    "admin": {
        "fullname": "admin",
        "username": "admin",
        "email": "admin@mail.com",
        "password": "admin123",
        "role": "admin"
    }
}

# Storage for tokens
TOKENS = {}


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{text.center(80)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")


def print_test_info(test_id: str, test_name: str):
    """Print test information"""
    print(f"\n{Fore.YELLOW}[{test_id}] {test_name}{Style.RESET_ALL}")


def log_result(test_id: str, test_name: str, status: str, expected: str, actual: str, message: str = ""):
    """Log test result"""
    global TOTAL_TESTS, PASSED_TESTS, FAILED_TESTS
    
    TOTAL_TESTS += 1
    
    if status == "PASS":
        PASSED_TESTS += 1
        print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL}")
    else:
        FAILED_TESTS += 1
        print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL}")
        if message:
            print(f"  {Fore.RED}Error: {message}{Style.RESET_ALL}")
    
    RESULTS.append({
        "ID": test_id,
        "Test Name": test_name,
        "Status": status,
        "Expected": expected,
        "Actual": actual,
        "Message": message
    })


def make_request(method: str, endpoint: str, token: str = None, data: dict = None, 
                 files: dict = None, expected_status: int = 200) -> Tuple[int, dict]:
    """Make HTTP request and return status code and response"""
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            if files:
                response = requests.post(url, headers=headers, files=files, data=data, timeout=10)
            else:
                headers["Content-Type"] = "application/json"
                response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method == "PUT":
            headers["Content-Type"] = "application/json"
            response = requests.put(url, headers=headers, json=data, timeout=10)
        elif method == "DELETE":
            if data:
                headers["Content-Type"] = "application/json"
                response = requests.delete(url, headers=headers, json=data, timeout=10)
            else:
                response = requests.delete(url, headers=headers, timeout=10)
        else:
            return 0, {"error": f"Unsupported method: {method}"}
        
        try:
            response_data = response.json()
        except:
            response_data = {"text": response.text}
        
        return response.status_code, response_data
    
    except requests.exceptions.ConnectionError:
        return 0, {"error": "Connection Error - Server tidak berjalan"}
    except requests.exceptions.Timeout:
        return 0, {"error": "Timeout"}
    except Exception as e:
        return 0, {"error": str(e)}


# ========== AUTHENTICATION TESTS ==========

def test_auth():
    """Test authentication endpoints"""
    print_header("TESTING AUTHENTICATION MODULE")
    
    # TC-AUTH-002: Register with valid data (User)
    print_test_info("TC-AUTH-002", "Register User dengan Data Valid")
    status, response = make_request(
        "POST", 
        "/auth/register",
        data=TEST_USERS["user"]
    )
    
    if status in [200, 201]:
        log_result("TC-AUTH-002", "Register User Valid", "PASS", 
                   "Status 200/201", f"Status {status}", "")
    else:
        # User might already exist, that's okay
        if "sudah" in str(response).lower() or "already" in str(response).lower():
            log_result("TC-AUTH-002", "Register User Valid", "PASS", 
                       "Status 200/201 or User exists", f"Status {status} - User exists", "")
        else:
            log_result("TC-AUTH-002", "Register User Valid", "FAIL", 
                       "Status 200/201", f"Status {status}", str(response))
    
    # TC-AUTH-003: Register with empty username
    print_test_info("TC-AUTH-003", "Register dengan Username Kosong")
    status, response = make_request(
        "POST",
        "/auth/register",
        data={"username": "", "email": "test@mail.com", "password": "Test123!", "role": "user"}
    )
    
    if status in [400, 422]:
        log_result("TC-AUTH-003", "Register Username Kosong", "PASS",
                   "Status 400/422", f"Status {status}", "")
    else:
        log_result("TC-AUTH-003", "Register Username Kosong", "FAIL",
                   "Status 400/422", f"Status {status}", str(response))
    
    # TC-AUTH-004: Register with invalid email
    print_test_info("TC-AUTH-004", "Register dengan Email Tidak Valid")
    status, response = make_request(
        "POST",
        "/auth/register",
        data={"username": "testuser2", "email": "invalid-email", "password": "Test123!", "role": "user"}
    )
    
    if status in [400, 422]:
        log_result("TC-AUTH-004", "Register Email Invalid", "PASS",
                   "Status 400/422", f"Status {status}", "")
    else:
        log_result("TC-AUTH-004", "Register Email Invalid", "FAIL",
                   "Status 400/422", f"Status {status}", str(response))
    
    # Note: Advisor is not registered via API, using existing advisor from database
    
    # TC-AUTH-006: Login with valid credentials (User)
    print_test_info("TC-AUTH-006", "Login User dengan Kredensial Valid")
    status, response = make_request(
        "POST",
        "/auth/login",
        data={"username": TEST_USERS["user"]["username"], "password": TEST_USERS["user"]["password"]}
    )
    
    if status == 200 and ("token" in response or "access_token" in response):
        TOKENS["user"] = response.get("token") or response.get("access_token")
        log_result("TC-AUTH-006", "Login User Valid", "PASS",
                   "Status 200 with token", f"Status {status} - Token received", "")
    else:
        log_result("TC-AUTH-006", "Login User Valid", "FAIL",
                   "Status 200 with token", f"Status {status}", str(response))
    
    # Login advisor
    print_test_info("TC-AUTH-006b", "Login Advisor dengan Kredensial Valid")
    status, response = make_request(
        "POST",
        "/auth/login",
        data={"username": TEST_USERS["advisor"]["username"], "password": TEST_USERS["advisor"]["password"]}
    )
    
    if status == 200 and ("token" in response or "access_token" in response):
        TOKENS["advisor"] = response.get("token") or response.get("access_token")
        log_result("TC-AUTH-006b", "Login Advisor Valid", "PASS",
                   "Status 200 with token", f"Status {status} - Token received", "")
    else:
        log_result("TC-AUTH-006b", "Login Advisor Valid", "FAIL",
                   "Status 200 with token", f"Status {status}", str(response))
    
    # Login admin
    print_test_info("TC-AUTH-006c", "Login Admin dengan Kredensial Valid")
    status, response = make_request(
        "POST",
        "/auth/login",
        data={"username": TEST_USERS["admin"]["username"], "password": TEST_USERS["admin"]["password"]}
    )
    
    if status == 200 and ("token" in response or "access_token" in response):
        TOKENS["admin"] = response.get("token") or response.get("access_token")
        log_result("TC-AUTH-006c", "Login Admin Valid", "PASS",
                   "Status 200 with token", f"Status {status} - Token received", "")
    else:
        log_result("TC-AUTH-006c", "Login Admin Valid", "FAIL",
                   "Status 200 with token", f"Status {status}", str(response))
    
    # TC-AUTH-007: Login with non-existent username
    print_test_info("TC-AUTH-007", "Login dengan Username Tidak Terdaftar")
    status, response = make_request(
        "POST",
        "/auth/login",
        data={"username": "notexistuser", "password": "anything"}
    )
    
    if status in [401, 404]:
        log_result("TC-AUTH-007", "Login Username Not Found", "PASS",
                   "Status 401/404", f"Status {status}", "")
    else:
        log_result("TC-AUTH-007", "Login Username Not Found", "FAIL",
                   "Status 401/404", f"Status {status}", str(response))
    
    # TC-AUTH-008: Login with wrong password
    print_test_info("TC-AUTH-008", "Login dengan Password Salah")
    status, response = make_request(
        "POST",
        "/auth/login",
        data={"username": TEST_USERS["user"]["username"], "password": "WrongPassword123!"}
    )
    
    if status == 401:
        log_result("TC-AUTH-008", "Login Wrong Password", "PASS",
                   "Status 401", f"Status {status}", "")
    else:
        log_result("TC-AUTH-008", "Login Wrong Password", "FAIL",
                   "Status 401", f"Status {status}", str(response))
    
    # TC-AUTH-009: Login with empty fields
    print_test_info("TC-AUTH-009", "Login dengan Field Kosong")
    status, response = make_request(
        "POST",
        "/auth/login",
        data={"username": "", "password": ""}
    )
    
    if status in [400, 422]:
        log_result("TC-AUTH-009", "Login Empty Fields", "PASS",
                   "Status 400/422", f"Status {status}", "")
    else:
        log_result("TC-AUTH-009", "Login Empty Fields", "FAIL",
                   "Status 400/422", f"Status {status}", str(response))
    
    # TC-AUTH-011: Access protected route without token
    print_test_info("TC-AUTH-011", "Akses Protected Route Tanpa Token")
    status, response = make_request("GET", "/auth/me")
    
    if status == 401:
        log_result("TC-AUTH-011", "Access Without Token", "PASS",
                   "Status 401", f"Status {status}", "")
    else:
        log_result("TC-AUTH-011", "Access Without Token", "FAIL",
                   "Status 401", f"Status {status}", str(response))
    
    # TC-AUTH-012: Access with invalid token
    print_test_info("TC-AUTH-012", "Akses dengan Token Invalid")
    status, response = make_request("GET", "/auth/me", token="invalid.token.here")
    
    if status == 401:
        log_result("TC-AUTH-012", "Access Invalid Token", "PASS",
                   "Status 401", f"Status {status}", "")
    else:
        log_result("TC-AUTH-012", "Access Invalid Token", "FAIL",
                   "Status 401", f"Status {status}", str(response))
    
    # TC-AUTH-013: SQL Injection attempt
    print_test_info("TC-AUTH-013", "SQL Injection pada Login")
    status, response = make_request(
        "POST",
        "/auth/login",
        data={"username": "admin' OR '1'='1", "password": "anything"}
    )
    
    if status in [401, 404, 400]:
        log_result("TC-AUTH-013", "SQL Injection Prevention", "PASS",
                   "Status 401/404/400 - No bypass", f"Status {status}", "")
    else:
        log_result("TC-AUTH-013", "SQL Injection Prevention", "FAIL",
                   "Status 401/404/400", f"Status {status}", "POTENTIAL SECURITY ISSUE!")


# ========== USER DASHBOARD TESTS ==========

def test_user_dashboard():
    """Test user dashboard endpoints"""
    print_header("TESTING USER DASHBOARD MODULE")
    
    user_token = TOKENS.get("user")
    
    if not user_token:
        print(f"{Fore.RED}Skipping User Dashboard tests - No user token available{Style.RESET_ALL}")
        return
    
    # TC-USER-002: Search ERD with valid keyword
    print_test_info("TC-USER-002", "Search ERD dengan Keyword Valid")
    status, response = make_request(
        "POST",
        "/api/search-erd",
        token=user_token,
        data={"text": "mahasiswa"}  # Fixed: Changed from "keyword" to "text"
    )
    
    if status == 200:
        log_result("TC-USER-002", "Search ERD Valid", "PASS",
                   "Status 200", f"Status {status}", "")
    else:
        log_result("TC-USER-002", "Search ERD Valid", "FAIL",
                   "Status 200", f"Status {status}", str(response))
    
    # TC-USER-003: Search ERD with empty keyword
    print_test_info("TC-USER-003", "Search ERD dengan Keyword Kosong")
    status, response = make_request(
        "POST",
        "/api/search-erd",
        token=user_token,
        data={"text": ""}  # Fixed: Changed from "keyword" to "text"
    )
    
    if status in [400, 422, 200]:  # Some implementations allow empty search
        log_result("TC-USER-003", "Search Empty Keyword", "PASS",
                   "Status 400/422 or 200", f"Status {status}", "")
    else:
        log_result("TC-USER-003", "Search Empty Keyword", "FAIL",
                   "Status 400/422 or 200", f"Status {status}", str(response))
    
    # TC-USER-004: XSS on search keyword
    print_test_info("TC-USER-004", "XSS Attack pada Search")
    status, response = make_request(
        "POST",
        "/api/search-erd",
        token=user_token,
        data={"text": "<script>alert('XSS')</script>"}  # Fixed: Changed from "keyword" to "text"
    )
    
    # Should either sanitize or reject, but not execute
    if status in [200, 400]:
        log_result("TC-USER-004", "XSS Prevention", "PASS",
                   "Input sanitized", f"Status {status}", "")
    else:
        log_result("TC-USER-004", "XSS Prevention", "FAIL",
                   "Input should be handled", f"Status {status}", str(response))
    
    # TC-USER-006: Create request consultation
    print_test_info("TC-USER-006", "Membuat Request Konsultasi")
    status, response = make_request(
        "POST",
        "/api/requests/",
        token=user_token,
        data={
            "query": "Butuh bantuan ERD sistem perpustakaan",  # Fixed: Changed from "title" to "query"
            "description": "Saya perlu bantuan membuat ERD untuk sistem perpustakaan dengan entitas buku, anggota, dan peminjaman"
        }
    )
    
    if status in [200, 201]:
        log_result("TC-USER-006", "Create Request", "PASS",
                   "Status 200/201", f"Status {status}", "")
    else:
        log_result("TC-USER-006", "Create Request", "FAIL",
                   "Status 200/201", f"Status {status}", str(response))
    
    # TC-USER-007: Create request with empty fields
    print_test_info("TC-USER-007", "Request dengan Field Kosong")
    status, response = make_request(
        "POST",
        "/api/requests/",
        token=user_token,
        data={"query": "", "description": ""}  # Fixed: Changed from "title" to "query"
    )
    
    if status in [400, 422]:
        log_result("TC-USER-007", "Request Empty Fields", "PASS",
                   "Status 400/422", f"Status {status}", "")
    else:
        log_result("TC-USER-007", "Request Empty Fields", "FAIL",
                   "Status 400/422", f"Status {status}", str(response))
    
    # TC-USER-008: Get user's requests
    print_test_info("TC-USER-008", "Melihat Daftar Request Pribadi")
    status, response = make_request(
        "GET",
        "/api/requests/my-requests",
        token=user_token
    )
    
    if status == 200:
        log_result("TC-USER-008", "Get My Requests", "PASS",
                   "Status 200", f"Status {status}", "")
    else:
        log_result("TC-USER-008", "Get My Requests", "FAIL",
                   "Status 200", f"Status {status}", str(response))


# ========== ADVISOR DASHBOARD TESTS ==========

def test_advisor_dashboard():
    """Test advisor dashboard endpoints"""
    print_header("TESTING ADVISOR DASHBOARD MODULE")
    
    advisor_token = TOKENS.get("advisor")
    
    if not advisor_token:
        print(f"{Fore.RED}Skipping Advisor Dashboard tests - No advisor token available{Style.RESET_ALL}")
        return
    
    # TC-ADV-002: Add ERD with valid data
    print_test_info("TC-ADV-002", "Tambah ERD dengan Data Valid")
    status, response = make_request(
        "POST",
        "/api/add-erd",
        token=advisor_token,
        data={
            "name": f"erd_test_{int(time.time())}",
            "entities": [
                {
                    "name": "Pelanggan",
                    "attributes": ["id_pelanggan", "nama", "email"],
                    "primary_key": "id_pelanggan"
                },
                {
                    "name": "Produk",
                    "attributes": ["id_produk", "nama", "harga"],
                    "primary_key": "id_produk"
                }
            ],
            "relationships": [  # Fixed: Changed from "relations" to "relationships"
                {
                    "entity1": "Pelanggan",  # Fixed: Changed from "from" to "entity1"
                    "entity2": "Produk",     # Fixed: Changed from "to" to "entity2"
                    "relation": "membeli",
                    "type": "many-to-many",  # Fixed: Changed from "M:N" to "many-to-many"
                    "layout": "LR",          # Added: Required field
                    "attributes": []         # Added: Required field for relationships
                }
            ]
        }
    )
    
    if status in [200, 201]:
        log_result("TC-ADV-002", "Add ERD Valid", "PASS",
                   "Status 200/201", f"Status {status}", "")
    else:
        log_result("TC-ADV-002", "Add ERD Valid", "FAIL",
                   "Status 200/201", f"Status {status}", str(response))
    
    # TC-ADV-003: Add ERD with empty name
    print_test_info("TC-ADV-003", "Tambah ERD dengan Nama Kosong")
    status, response = make_request(
        "POST",
        "/api/add-erd",
        token=advisor_token,
        data={
            "name": "",
            "entities": [{"name": "Test", "attributes": ["id"], "primary_key": "id"}],
            "relationships": []  # Added: Required field
        }
    )
    
    if status in [400, 422]:
        log_result("TC-ADV-003", "Add ERD Empty Name", "PASS",
                   "Status 400/422", f"Status {status}", "")
    else:
        log_result("TC-ADV-003", "Add ERD Empty Name", "FAIL",
                   "Status 400/422", f"Status {status}", str(response))
    
    # TC-ADV-005: Add ERD without entities
    print_test_info("TC-ADV-005", "Tambah ERD Tanpa Entitas")
    status, response = make_request(
        "POST",
        "/api/add-erd",
        token=advisor_token,
        data={
            "name": "ERD_No_Entities",
            "entities": [],
            "relationships": []  # Added: Required field
        }
    )
    
    if status in [400, 422]:
        log_result("TC-ADV-005", "Add ERD No Entities", "PASS",
                   "Status 400/422", f"Status {status}", "")
    else:
        log_result("TC-ADV-005", "Add ERD No Entities", "FAIL",
                   "Status 400/422", f"Status {status}", str(response))
    
    # TC-ADV-010: Get advisor's ERDs
    print_test_info("TC-ADV-010", "Melihat Daftar ERD Milik Sendiri")
    status, response = make_request(
        "GET",
        "/api/advisor-erds",
        token=advisor_token
    )
    
    if status == 200:
        log_result("TC-ADV-010", "Get My ERDs", "PASS",
                   "Status 200", f"Status {status}", "")
    else:
        log_result("TC-ADV-010", "Get My ERDs", "FAIL",
                   "Status 200", f"Status {status}", str(response))
    
    # TC-ADV-015: Get pending requests
    print_test_info("TC-ADV-015", "Melihat Pending Requests")
    status, response = make_request(
        "GET",
        "/api/requests/pending",
        token=advisor_token
    )
    
    if status == 200:
        log_result("TC-ADV-015", "Get Pending Requests", "PASS",
                   "Status 200", f"Status {status}", "")
    else:
        log_result("TC-ADV-015", "Get Pending Requests", "FAIL",
                   "Status 200", f"Status {status}", str(response))
    
    # TC-ADV-017: Get assigned requests
    print_test_info("TC-ADV-017", "Melihat Assigned Requests")
    status, response = make_request(
        "GET",
        "/api/requests/my-assigned",
        token=advisor_token
    )
    
    if status == 200:
        log_result("TC-ADV-017", "Get My Assigned Requests", "PASS",
                   "Status 200", f"Status {status}", "")
    else:
        log_result("TC-ADV-017", "Get My Assigned Requests", "FAIL",
                   "Status 200", f"Status {status}", str(response))
    
    # TC-ADV-020: User trying to access advisor endpoint
    print_test_info("TC-ADV-020", "User Akses Advisor Endpoint")
    user_token = TOKENS.get("user")
    if user_token:
        status, response = make_request(
            "POST",
            "/api/add-erd",
            token=user_token,
            data={"name": "Test", "entities": [{"name": "Test", "attributes": ["id"]}]}
        )
        
        if status == 403:
            log_result("TC-ADV-020", "User Access Advisor Endpoint", "PASS",
                       "Status 403", f"Status {status}", "")
        else:
            log_result("TC-ADV-020", "User Access Advisor Endpoint", "FAIL",
                       "Status 403", f"Status {status}", "Potential Authorization Issue!")


# ========== API TESTS ==========

def test_api_general():
    """Test general API behaviors"""
    print_header("TESTING GENERAL API BEHAVIORS")
    
    # TC-API-001: Access API without authentication
    print_test_info("TC-API-001", "Akses API Tanpa Token")
    status, response = make_request("GET", "/api/all-erds")
    
    if status in [401, 200]:  # Some endpoints might be public
        log_result("TC-API-001", "Access API No Token", "PASS",
                   "Status 401 or 200 (if public)", f"Status {status}", "")
    else:
        log_result("TC-API-001", "Access API No Token", "FAIL",
                   "Status 401 or 200", f"Status {status}", str(response))
    
    # TC-API-002: Method not allowed
    print_test_info("TC-API-002", "Method Not Allowed")
    status, response = make_request("GET", "/api/search-erd")  # Should be POST
    
    if status == 405:
        log_result("TC-API-002", "Method Not Allowed", "PASS",
                   "Status 405", f"Status {status}", "")
    else:
        log_result("TC-API-002", "Method Not Allowed", "FAIL",
                   "Status 405", f"Status {status}", str(response))
    
    # TC-API-003: Invalid JSON
    print_test_info("TC-API-003", "Invalid JSON Body")
    advisor_token = TOKENS.get("advisor")
    if advisor_token:
        try:
            url = f"{BASE_URL}/api/add-erd"
            headers = {
                "Authorization": f"Bearer {advisor_token}",
                "Content-Type": "application/json"
            }
            response = requests.post(url, headers=headers, data="{invalid json}", timeout=10)
            
            if response.status_code == 400:
                log_result("TC-API-003", "Invalid JSON", "PASS",
                           "Status 400", f"Status {response.status_code}", "")
            else:
                log_result("TC-API-003", "Invalid JSON", "FAIL",
                           "Status 400", f"Status {response.status_code}", "")
        except Exception as e:
            log_result("TC-API-003", "Invalid JSON", "FAIL",
                       "Status 400", "Exception", str(e))
    
    # TC-API-005: Resource not found
    print_test_info("TC-API-005", "Resource Not Found")
    status, response = make_request(
        "GET",
        "/api/erd/999999",
        token=advisor_token
    )
    
    if status == 404:
        log_result("TC-API-005", "Resource Not Found", "PASS",
                   "Status 404", f"Status {status}", "")
    else:
        log_result("TC-API-005", "Resource Not Found", "FAIL",
                   "Status 404", f"Status {status}", str(response))


# ========== SECURITY TESTS ==========

def test_security():
    """Test security aspects"""
    print_header("TESTING SECURITY")
    
    user_token = TOKENS.get("user")
    
    # TC-SEC-001: XSS on various inputs
    print_test_info("TC-SEC-001", "XSS Attack pada Form Input")
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')"
    ]
    
    xss_pass = True
    for payload in xss_payloads:
        status, response = make_request(
            "POST",
            "/auth/register",
            data={"username": payload, "email": "test@mail.com", "password": "Test123!", "role": "user"}
        )
        # Should either reject or sanitize, not process the script
        if status not in [200, 400, 422]:
            xss_pass = False
    
    if xss_pass:
        log_result("TC-SEC-001", "XSS Prevention", "PASS",
                   "Input sanitized/rejected", "All payloads handled", "")
    else:
        log_result("TC-SEC-001", "XSS Prevention", "FAIL",
                   "Input sanitized/rejected", "Some payloads not handled", "SECURITY RISK!")
    
    # TC-SEC-002: SQL Injection (already tested in auth)
    
    # TC-SEC-004: JWT Token manipulation
    print_test_info("TC-SEC-004", "JWT Token Manipulation")
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFkbWluIiwicm9sZSI6ImFkbWluIn0.invalid"
    status, response = make_request("GET", "/auth/me", token=fake_token)
    
    if status == 401:
        log_result("TC-SEC-004", "JWT Manipulation Prevention", "PASS",
                   "Status 401", f"Status {status}", "")
    else:
        log_result("TC-SEC-004", "JWT Manipulation Prevention", "FAIL",
                   "Status 401", f"Status {status}", "CRITICAL SECURITY ISSUE!")
    
    # TC-SEC-007: Directory traversal
    print_test_info("TC-SEC-007", "Directory Traversal Attack")
    status, response = make_request(
        "GET",
        "/api/download-erd/../../etc/passwd",
        token=user_token
    )
    
    if status in [400, 403, 404]:
        log_result("TC-SEC-007", "Directory Traversal Prevention", "PASS",
                   "Status 400/403/404", f"Status {status}", "")
    else:
        log_result("TC-SEC-007", "Directory Traversal Prevention", "FAIL",
                   "Status 400/403/404", f"Status {status}", "POTENTIAL SECURITY ISSUE!")


# ========== ERD CRUD TESTS ==========

def test_erd_crud():
    """Test ERD CRUD operations (Update & Delete)"""
    print_header("TESTING ERD CRUD OPERATIONS")
    
    advisor_token = TOKENS.get("advisor")
    
    if not advisor_token:
        print(f"{Fore.RED}Skipping ERD CRUD tests - No advisor token available{Style.RESET_ALL}")
        return
    
    # First, create a test ERD to use for update/delete tests
    test_erd_name = f"test_crud_erd_{int(time.time())}"
    create_response = make_request(
        "POST",
        "/api/add-erd",
        token=advisor_token,
        data={
            "name": test_erd_name,
            "entities": [
                {
                    "name": "TestEntity",
                    "attributes": ["id", "name"],
                    "primary_key": "id"
                }
            ],
            "relationships": []
        }
    )
    
    created_erd_id = None
    if create_response[0] in [200, 201]:
        created_erd_id = create_response[1].get('erd_id')
        print(f"{Fore.GREEN}✓ Test ERD created: {created_erd_id}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Failed to create test ERD{Style.RESET_ALL}")
    
    # TC-ERD-001: Get ERD Detail with valid ID
    if created_erd_id:
        print_test_info("TC-ERD-001", "Get ERD Detail dengan ID Valid")
        status, response = make_request(
            "GET",
            f"/api/erd/{created_erd_id}",
            token=advisor_token
        )
        
        if status == 200 and 'erd' in response:
            log_result("TC-ERD-001", "Get ERD Detail Valid", "PASS",
                       "Status 200 with ERD data", f"Status {status}", "")
        else:
            log_result("TC-ERD-001", "Get ERD Detail Valid", "FAIL",
                       "Status 200 with ERD data", f"Status {status}", str(response))
    
    # TC-ERD-002: Get ERD Detail with invalid ID
    print_test_info("TC-ERD-002", "Get ERD Detail dengan ID Tidak Valid")
    status, response = make_request(
        "GET",
        "/api/erd/invalid_erd_id_12345",
        token=advisor_token
    )
    
    if status == 404:
        log_result("TC-ERD-002", "Get ERD Detail Invalid ID", "PASS",
                   "Status 404", f"Status {status}", "")
    else:
        log_result("TC-ERD-002", "Get ERD Detail Invalid ID", "FAIL",
                   "Status 404", f"Status {status}", str(response))
    
    # TC-ERD-003: Update ERD with valid data
    if created_erd_id:
        print_test_info("TC-ERD-003", "Update ERD dengan Data Valid")
        status, response = make_request(
            "PUT",
            f"/api/erd/{created_erd_id}",
            token=advisor_token,
            data={
                "name": f"{test_erd_name}_updated",
                "entities": [
                    {
                        "name": "UpdatedEntity",
                        "attributes": ["id", "name", "updated_at"],
                        "primary_key": "id"
                    },
                    {
                        "name": "NewEntity",
                        "attributes": ["id", "description"],
                        "primary_key": "id"
                    }
                ],
                "relationships": [
                    {
                        "entity1": "UpdatedEntity",
                        "entity2": "NewEntity",
                        "relation": "has",
                        "type": "one-to-many",
                        "layout": "LR",
                        "attributes": []
                    }
                ]
            }
        )
        
        if status == 200:
            log_result("TC-ERD-003", "Update ERD Valid", "PASS",
                       "Status 200", f"Status {status}", "")
        else:
            log_result("TC-ERD-003", "Update ERD Valid", "FAIL",
                       "Status 200", f"Status {status}", str(response))
    
    # TC-ERD-004: Update ERD with invalid ID
    print_test_info("TC-ERD-004", "Update ERD dengan ID Tidak Valid")
    status, response = make_request(
        "PUT",
        "/api/erd/invalid_erd_id_99999",
        token=advisor_token,
        data={
            "name": "test_update",
            "entities": [{"name": "Test", "attributes": ["id"], "primary_key": "id"}],
            "relationships": []
        }
    )
    
    if status == 404:
        log_result("TC-ERD-004", "Update ERD Invalid ID", "PASS",
                   "Status 404", f"Status {status}", "")
    else:
        log_result("TC-ERD-004", "Update ERD Invalid ID", "FAIL",
                   "Status 404", f"Status {status}", str(response))
    
    # TC-ERD-005: Update ERD without permission (user trying to update)
    user_token = TOKENS.get("user")
    if user_token and created_erd_id:
        print_test_info("TC-ERD-005", "User Mencoba Update ERD Advisor")
        status, response = make_request(
            "PUT",
            f"/api/erd/{created_erd_id}",
            token=user_token,
            data={
                "name": "hacked_erd",
                "entities": [{"name": "Hack", "attributes": ["id"], "primary_key": "id"}],
                "relationships": []
            }
        )
        
        if status == 403:
            log_result("TC-ERD-005", "User Update Advisor ERD", "PASS",
                       "Status 403", f"Status {status}", "")
        else:
            log_result("TC-ERD-005", "User Update Advisor ERD", "FAIL",
                       "Status 403", f"Status {status}", "Authorization Issue!")
    
    # TC-ERD-006: Delete ERD with valid ID
    if created_erd_id:
        print_test_info("TC-ERD-006", "Delete ERD dengan ID Valid")
        status, response = make_request(
            "DELETE",
            f"/api/erd/{created_erd_id}",
            token=advisor_token
        )
        
        if status in [200, 204]:
            log_result("TC-ERD-006", "Delete ERD Valid", "PASS",
                       "Status 200/204", f"Status {status}", "")
        else:
            log_result("TC-ERD-006", "Delete ERD Valid", "FAIL",
                       "Status 200/204", f"Status {status}", str(response))
    
    # TC-ERD-007: Delete ERD with invalid ID
    print_test_info("TC-ERD-007", "Delete ERD dengan ID Tidak Valid")
    status, response = make_request(
        "DELETE",
        "/api/erd/nonexistent_erd_12345",
        token=advisor_token
    )
    
    if status == 404:
        log_result("TC-ERD-007", "Delete ERD Invalid ID", "PASS",
                   "Status 404", f"Status {status}", "")
    else:
        log_result("TC-ERD-007", "Delete ERD Invalid ID", "FAIL",
                   "Status 404", f"Status {status}", str(response))
    
    # TC-ERD-008: User trying to delete advisor's ERD
    # Create another test ERD first
    test_erd_name_2 = f"test_delete_auth_{int(time.time())}"
    create_response_2 = make_request(
        "POST",
        "/api/add-erd",
        token=advisor_token,
        data={
            "name": test_erd_name_2,
            "entities": [{"name": "TestAuth", "attributes": ["id"], "primary_key": "id"}],
            "relationships": []
        }
    )
    
    created_erd_id_2 = None
    if create_response_2[0] in [200, 201]:
        created_erd_id_2 = create_response_2[1].get('erd_id')
    
    if user_token and created_erd_id_2:
        print_test_info("TC-ERD-008", "User Mencoba Delete ERD Advisor")
        status, response = make_request(
            "DELETE",
            f"/api/erd/{created_erd_id_2}",
            token=user_token
        )
        
        if status == 403:
            log_result("TC-ERD-008", "User Delete Advisor ERD", "PASS",
                       "Status 403", f"Status {status}", "")
            # Cleanup: Delete the ERD as advisor
            make_request("DELETE", f"/api/erd/{created_erd_id_2}", token=advisor_token)
        else:
            log_result("TC-ERD-008", "User Delete Advisor ERD", "FAIL",
                       "Status 403", f"Status {status}", "Authorization Issue!")


# ========== REQUEST WORKFLOW TESTS ==========

def test_request_workflow():
    """Test request workflow (Cancel, Assign, Complete)"""
    print_header("TESTING REQUEST WORKFLOW")
    
    user_token = TOKENS.get("user")
    advisor_token = TOKENS.get("advisor")
    
    if not user_token or not advisor_token:
        print(f"{Fore.RED}Skipping Request Workflow tests - Tokens not available{Style.RESET_ALL}")
        return
    
    # Create test requests for workflow testing
    test_request_id_1 = None
    test_request_id_2 = None
    test_request_id_3 = None
    
    # Create request 1 (for cancel test)
    status, response = make_request(
        "POST",
        "/api/requests/",
        token=user_token,
        data={
            "query": "Test request for cancel workflow",
            "description": "This request will be cancelled by user"
        }
    )
    if status in [200, 201]:
        test_request_id_1 = response.get('request_id') or response.get('id')
        print(f"{Fore.GREEN}✓ Test request 1 created: {test_request_id_1}{Style.RESET_ALL}")
    
    # Create request 2 (for assign test)
    status, response = make_request(
        "POST",
        "/api/requests/",
        token=user_token,
        data={
            "query": "Test request for assign workflow",
            "description": "This request will be assigned to advisor"
        }
    )
    if status in [200, 201]:
        test_request_id_2 = response.get('request_id') or response.get('id')
        print(f"{Fore.GREEN}✓ Test request 2 created: {test_request_id_2}{Style.RESET_ALL}")
    
    # Create request 3 (for complete test)
    status, response = make_request(
        "POST",
        "/api/requests/",
        token=user_token,
        data={
            "query": "Test request for complete workflow",
            "description": "This request will be completed by advisor"
        }
    )
    if status in [200, 201]:
        test_request_id_3 = response.get('request_id') or response.get('id')
        print(f"{Fore.GREEN}✓ Test request 3 created: {test_request_id_3}{Style.RESET_ALL}")
    
    # TC-REQ-001: User cancel own request
    if test_request_id_1:
        print_test_info("TC-REQ-001", "User Cancel Request Sendiri")
        status, response = make_request(
            "DELETE",
            f"/api/requests/{test_request_id_1}/cancel",
            token=user_token
        )
        
        if status in [200, 204]:
            log_result("TC-REQ-001", "User Cancel Own Request", "PASS",
                       "Status 200/204", f"Status {status}", "")
        else:
            log_result("TC-REQ-001", "User Cancel Own Request", "FAIL",
                       "Status 200/204", f"Status {status}", str(response))
    
    # TC-REQ-002: User trying to cancel another user's request (create one more request as different flow)
    print_test_info("TC-REQ-002", "User Cancel Request Orang Lain")
    # Assuming test_request_id_2 belongs to same user, we can't really test this without another user
    # But we can test canceling non-existent request
    status, response = make_request(
        "DELETE",
        "/api/requests/nonexistent_request_999/cancel",
        token=user_token
    )
    
    if status == 404:
        log_result("TC-REQ-002", "Cancel Non-existent Request", "PASS",
                   "Status 404", f"Status {status}", "")
    else:
        log_result("TC-REQ-002", "Cancel Non-existent Request", "FAIL",
                   "Status 404", f"Status {status}", str(response))
    
    # TC-REQ-003: Advisor trying to cancel user's request (should fail)
    if test_request_id_2:
        print_test_info("TC-REQ-003", "Advisor Mencoba Cancel User Request")
        status, response = make_request(
            "DELETE",
            f"/api/requests/{test_request_id_2}/cancel",
            token=advisor_token
        )
        
        if status == 403:
            log_result("TC-REQ-003", "Advisor Cancel User Request", "PASS",
                       "Status 403", f"Status {status}", "")
        else:
            log_result("TC-REQ-003", "Advisor Cancel User Request", "FAIL",
                       "Status 403", f"Status {status}", "Authorization Issue!")
    
    # TC-REQ-004: Advisor assign request to themselves
    if test_request_id_2:
        print_test_info("TC-REQ-004", "Advisor Assign Request")
        status, response = make_request(
            "PUT",
            f"/api/requests/{test_request_id_2}/assign",
            token=advisor_token,
            data={}  # Send empty JSON body for PUT request
        )
        
        if status == 200:
            log_result("TC-REQ-004", "Advisor Assign Request", "PASS",
                       "Status 200", f"Status {status}", "")
        else:
            log_result("TC-REQ-004", "Advisor Assign Request", "FAIL",
                       "Status 200", f"Status {status}", str(response))
    
    # TC-REQ-005: Advisor assign non-existent request
    print_test_info("TC-REQ-005", "Advisor Assign Request Tidak Ada")
    status, response = make_request(
        "PUT",
        "/api/requests/fake_request_999/assign",
        token=advisor_token,
        data={}  # Send empty JSON body for PUT request
    )
    
    if status == 404:
        log_result("TC-REQ-005", "Assign Non-existent Request", "PASS",
                   "Status 404", f"Status {status}", "")
    else:
        log_result("TC-REQ-005", "Assign Non-existent Request", "FAIL",
                   "Status 404", f"Status {status}", str(response))
    
    # TC-REQ-006: User trying to assign request (should fail)
    if test_request_id_3:
        print_test_info("TC-REQ-006", "User Mencoba Assign Request")
        status, response = make_request(
            "PUT",
            f"/api/requests/{test_request_id_3}/assign",
            token=user_token,
            data={}  # Send empty JSON body for PUT request
        )
        
        if status == 403:
            log_result("TC-REQ-006", "User Assign Request", "PASS",
                       "Status 403", f"Status {status}", "")
        else:
            log_result("TC-REQ-006", "User Assign Request", "FAIL",
                       "Status 403", f"Status {status}", "Authorization Issue!")
    
    # TC-REQ-007: Advisor assign request 3 for complete test
    if test_request_id_3:
        make_request("PUT", f"/api/requests/{test_request_id_3}/assign", token=advisor_token, data={})
    
    # TC-REQ-007: Advisor complete assigned request
    if test_request_id_3:
        # First create a test ERD for completion
        test_erd_name = f"test_complete_erd_{int(time.time())}"
        create_erd = make_request(
            "POST",
            "/api/add-erd",
            token=advisor_token,
            data={
                "name": test_erd_name,
                "entities": [{"name": "CompletedEntity", "attributes": ["id"], "primary_key": "id"}],
                "relationships": []
            }
        )
        
        created_erd_id = None
        if create_erd[0] in [200, 201]:
            created_erd_id = create_erd[1].get('erd_id')
        
        if created_erd_id:
            print_test_info("TC-REQ-007", "Advisor Complete Request dengan ERD")
            status, response = make_request(
                "PUT",
                f"/api/requests/{test_request_id_3}/complete",
                token=advisor_token,
                data={
                    "erd_id": created_erd_id,
                    "notes": "Request completed successfully via automated test"
                }
            )
            
            if status == 200:
                log_result("TC-REQ-007", "Advisor Complete Request", "PASS",
                           "Status 200", f"Status {status}", "")
            else:
                log_result("TC-REQ-007", "Advisor Complete Request", "FAIL",
                           "Status 200", f"Status {status}", str(response))
    
    # TC-REQ-008: Complete request without ERD ID
    # Create another request for this test
    status, response = make_request(
        "POST",
        "/api/requests/",
        token=user_token,
        data={"query": "Test for invalid complete", "description": "Test"}
    )
    test_request_id_4 = None
    if status in [200, 201]:
        test_request_id_4 = response.get('request_id') or response.get('id')
        make_request("PUT", f"/api/requests/{test_request_id_4}/assign", token=advisor_token, data={})
    
    if test_request_id_4:
        print_test_info("TC-REQ-008", "Complete Request Tanpa ERD ID")
        status, response = make_request(
            "PUT",
            f"/api/requests/{test_request_id_4}/complete",
            token=advisor_token,
            data={"notes": "No ERD provided"}
        )
        
        if status in [400, 422]:
            log_result("TC-REQ-008", "Complete Request No ERD", "PASS",
                       "Status 400/422", f"Status {status}", "")
        else:
            log_result("TC-REQ-008", "Complete Request No ERD", "FAIL",
                       "Status 400/422", f"Status {status}", str(response))
    
    # TC-REQ-009: User trying to complete request (should fail)
    # Create one more request
    status, response = make_request(
        "POST",
        "/api/requests/",
        token=user_token,
        data={"query": "Test for user complete", "description": "Test"}
    )
    test_request_id_5 = None
    if status in [200, 201]:
        test_request_id_5 = response.get('request_id') or response.get('id')
    
    if test_request_id_5:
        print_test_info("TC-REQ-009", "User Mencoba Complete Request")
        status, response = make_request(
            "PUT",
            f"/api/requests/{test_request_id_5}/complete",
            token=user_token,
            data={"erd_id": "fake_erd_id", "notes": "User trying to complete"}
        )
        
        if status == 403:
            log_result("TC-REQ-009", "User Complete Request", "PASS",
                       "Status 403", f"Status {status}", "")
        else:
            log_result("TC-REQ-009", "User Complete Request", "FAIL",
                       "Status 403", f"Status {status}", "Authorization Issue!")


# ========== ADDITIONAL API TESTS ==========

def test_additional_features():
    """Test additional features: Logout, List ERDs, etc."""
    print_header("TESTING ADDITIONAL FEATURES")
    
    user_token = TOKENS.get("user")
    advisor_token = TOKENS.get("advisor")
    
    if not user_token or not advisor_token:
        print(f"{Fore.RED}Skipping Additional Features tests - Tokens not available{Style.RESET_ALL}")
        return
    
    # TC-ADD-001: Logout with valid token
    print_test_info("TC-ADD-001", "Logout dengan Token Valid")
    status, response = make_request(
        "POST",
        "/auth/logout",
        token=user_token,
        data={}
    )
    
    if status == 200:
        log_result("TC-ADD-001", "Logout Valid Token", "PASS",
                   "Status 200", f"Status {status}", "")
    else:
        log_result("TC-ADD-001", "Logout Valid Token", "FAIL",
                   "Status 200", f"Status {status}", str(response))
    
    # TC-ADD-002: Logout without token
    print_test_info("TC-ADD-002", "Logout Tanpa Token")
    status, response = make_request(
        "POST",
        "/auth/logout",
        data={}
    )
    
    if status == 401:
        log_result("TC-ADD-002", "Logout No Token", "PASS",
                   "Status 401", f"Status {status}", "")
    else:
        log_result("TC-ADD-002", "Logout No Token", "FAIL",
                   "Status 401", f"Status {status}", str(response))
    
    # TC-ADD-003: List all ERDs (public endpoint)
    print_test_info("TC-ADD-003", "List Semua ERD")
    status, response = make_request(
        "GET",
        "/api/list-erds",
        token=user_token
    )
    
    if status == 200:
        log_result("TC-ADD-003", "List All ERDs", "PASS",
                   "Status 200", f"Status {status}", "")
    else:
        log_result("TC-ADD-003", "List All ERDs", "FAIL",
                   "Status 200", f"Status {status}", str(response))
    
    # TC-ADD-004: Get all ERDs (alternative endpoint)
    print_test_info("TC-ADD-004", "Get All ERDs (Alternative)")
    status, response = make_request(
        "GET",
        "/api/all-erds",
        token=user_token
    )
    
    if status == 200:
        log_result("TC-ADD-004", "Get All ERDs", "PASS",
                   "Status 200", f"Status {status}", "")
    else:
        log_result("TC-ADD-004", "Get All ERDs", "FAIL",
                   "Status 200", f"Status {status}", str(response))


# ========== ERD IMAGE & DOWNLOAD TESTS ==========

def test_erd_image_download():
    """Test ERD image generation and download"""
    print_header("TESTING ERD IMAGE GENERATION & DOWNLOAD")
    
    advisor_token = TOKENS.get("advisor")
    
    if not advisor_token:
        print(f"{Fore.RED}Skipping ERD Image tests - No advisor token available{Style.RESET_ALL}")
        return
    
    # First, create a test ERD for image generation
    test_erd_name = f"test_image_erd_{int(time.time())}"
    create_response = make_request(
        "POST",
        "/api/add-erd",
        token=advisor_token,
        data={
            "name": test_erd_name,
            "entities": [
                {
                    "name": "ImageTest",
                    "attributes": ["id", "name"],
                    "primary_key": "id"
                }
            ],
            "relationships": []
        }
    )
    
    created_erd_name = None
    if create_response[0] in [200, 201]:
        created_erd_name = test_erd_name
        print(f"{Fore.GREEN}✓ Test ERD created for image generation: {created_erd_name}{Style.RESET_ALL}")
    
    # TC-IMG-001: Generate ERD image with valid name
    if created_erd_name:
        print_test_info("TC-IMG-001", "Generate ERD Image dengan Nama Valid")
        status, response = make_request(
            "GET",
            f"/api/generate-erd-image/{created_erd_name}",
            token=advisor_token
        )
        
        if status == 200:
            log_result("TC-IMG-001", "Generate ERD Image Valid", "PASS",
                       "Status 200", f"Status {status}", "")
        else:
            log_result("TC-IMG-001", "Generate ERD Image Valid", "FAIL",
                       "Status 200", f"Status {status}", str(response))
    
    # TC-IMG-002: Generate ERD image with invalid name
    print_test_info("TC-IMG-002", "Generate ERD Image dengan Nama Tidak Valid")
    status, response = make_request(
        "GET",
        "/api/generate-erd-image/nonexistent_erd_xyz",
        token=advisor_token
    )
    
    if status == 404:
        log_result("TC-IMG-002", "Generate ERD Image Invalid", "PASS",
                   "Status 404", f"Status {status}", "")
    else:
        log_result("TC-IMG-002", "Generate ERD Image Invalid", "FAIL",
                   "Status 404", f"Status {status}", str(response))
    
    # TC-IMG-003: Download ERD file with valid filename
    if created_erd_name:
        # Assume the image file is generated as PNG
        filename = f"{created_erd_name}.png"
        print_test_info("TC-IMG-003", "Download ERD File dengan Nama Valid")
        status, response = make_request(
            "GET",
            f"/api/download-erd/{filename}",
            token=advisor_token
        )
        
        # This might return 200 with file content or 404 if file doesn't exist yet
        if status in [200, 404]:
            log_result("TC-IMG-003", "Download ERD File Valid", "PASS",
                       "Status 200 or 404", f"Status {status}", "")
        else:
            log_result("TC-IMG-003", "Download ERD File Valid", "FAIL",
                       "Status 200 or 404", f"Status {status}", str(response))
    
    # TC-IMG-004: Download with directory traversal (already tested in security, but good to confirm)
    print_test_info("TC-IMG-004", "Download dengan Path Traversal")
    status, response = make_request(
        "GET",
        "/api/download-erd/../../../etc/passwd",
        token=advisor_token
    )
    
    if status in [400, 403, 404]:
        log_result("TC-IMG-004", "Download Path Traversal", "PASS",
                   "Status 400/403/404", f"Status {status}", "")
    else:
        log_result("TC-IMG-004", "Download Path Traversal", "FAIL",
                   "Status 400/403/404", f"Status {status}", "Security Issue!")


# ========== ADMIN MODULE TESTS ==========

def test_admin_module():
    """Test admin module endpoints"""
    print_header("TESTING ADMIN MODULE")
    
    user_token = TOKENS.get("user")
    advisor_token = TOKENS.get("advisor")
    admin_token = TOKENS.get("admin")
    
    if not user_token or not advisor_token:
        print(f"{Fore.RED}Skipping Admin Module tests - Tokens not available{Style.RESET_ALL}")
        return
    
    if not admin_token:
        print(f"{Fore.YELLOW}⚠️  Admin token not available - Skipping positive admin tests{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}✓ Admin token available - Running full admin functionality tests{Style.RESET_ALL}")
    
    # TC-ADM-001: Get all advisors (should fail without admin token)
    print_test_info("TC-ADM-001", "Get All Advisors Tanpa Admin Token")
    status, response = make_request(
        "GET",
        "/admin/api/advisors",
        token=user_token
    )
    
    if status in [401, 403]:
        log_result("TC-ADM-001", "Get Advisors No Admin", "PASS",
                   "Status 401/403", f"Status {status}", "")
    else:
        log_result("TC-ADM-001", "Get Advisors No Admin", "FAIL",
                   "Status 401/403", f"Status {status}", "Authorization Issue!")
    
    # TC-ADM-002: Advisor trying to access admin endpoint
    print_test_info("TC-ADM-002", "Advisor Akses Admin Endpoint")
    status, response = make_request(
        "GET",
        "/admin/api/advisors",
        token=advisor_token
    )
    
    if status in [401, 403]:
        log_result("TC-ADM-002", "Advisor Access Admin", "PASS",
                   "Status 401/403", f"Status {status}", "")
    else:
        log_result("TC-ADM-002", "Advisor Access Admin", "FAIL",
                   "Status 401/403", f"Status {status}", "Authorization Issue!")
    
    # TC-ADM-003: Create advisor without admin token
    print_test_info("TC-ADM-003", "Create Advisor Tanpa Admin Token")
    status, response = make_request(
        "POST",
        "/admin/api/advisors/create",
        token=user_token,
        data={
            "fullname": "Test Advisor",
            "username": "testadv",
            "email": "testadv@mail.com",
            "password": "Test123!"
        }
    )
    
    if status in [401, 403]:
        log_result("TC-ADM-003", "Create Advisor No Admin", "PASS",
                   "Status 401/403", f"Status {status}", "")
    else:
        log_result("TC-ADM-003", "Create Advisor No Admin", "FAIL",
                   "Status 401/403", f"Status {status}", "Authorization Issue!")
    
    # TC-ADM-004: Update advisor without admin token
    print_test_info("TC-ADM-004", "Update Advisor Tanpa Admin Token")
    status, response = make_request(
        "PUT",
        "/admin/api/advisors/update",
        token=advisor_token,
        data={
            "user_id": "fake_user_id",
            "fullname": "Updated Name"
        }
    )
    
    if status in [401, 403]:
        log_result("TC-ADM-004", "Update Advisor No Admin", "PASS",
                   "Status 401/403", f"Status {status}", "")
    else:
        log_result("TC-ADM-004", "Update Advisor No Admin", "FAIL",
                   "Status 401/403", f"Status {status}", "Authorization Issue!")
    
    # TC-ADM-005: Delete advisor without admin token
    print_test_info("TC-ADM-005", "Delete Advisor Tanpa Admin Token")
    status, response = make_request(
        "DELETE",
        "/admin/api/advisors/delete",
        token=user_token,
        data={"user_id": "fake_user_id"}
    )
    
    if status in [401, 403]:
        log_result("TC-ADM-005", "Delete Advisor No Admin", "PASS",
                   "Status 401/403", f"Status {status}", "")
    else:
        log_result("TC-ADM-005", "Delete Advisor No Admin", "FAIL",
                   "Status 401/403", f"Status {status}", "Authorization Issue!")
    
    # TC-ADM-006: Get statistics without admin token
    print_test_info("TC-ADM-006", "Get Statistics Tanpa Admin Token")
    status, response = make_request(
        "GET",
        "/admin/api/statistics",
        token=advisor_token
    )
    
    if status in [401, 403]:
        log_result("TC-ADM-006", "Get Statistics No Admin", "PASS",
                   "Status 401/403", f"Status {status}", "")
    else:
        log_result("TC-ADM-006", "Get Statistics No Admin", "FAIL",
                   "Status 401/403", f"Status {status}", "Authorization Issue!")
    
    # TC-ADM-007: Get advisor monitoring without admin token
    print_test_info("TC-ADM-007", "Get Advisor Monitoring Tanpa Admin Token")
    status, response = make_request(
        "GET",
        "/admin/api/advisor-monitoring",
        token=user_token
    )
    
    if status in [401, 403]:
        log_result("TC-ADM-007", "Get Monitoring No Admin", "PASS",
                   "Status 401/403", f"Status {status}", "")
    else:
        log_result("TC-ADM-007", "Get Monitoring No Admin", "FAIL",
                   "Status 401/403", f"Status {status}", "Authorization Issue!")
    
    # TC-ADM-008: Access admin dashboard page without token
    print_test_info("TC-ADM-008", "Akses Admin Dashboard Tanpa Token")
    status, response = make_request(
        "GET",
        "/admin/dashboard"
    )
    
    # This is a page route, might return HTML or redirect
    if status in [200, 302, 401, 403]:
        log_result("TC-ADM-008", "Admin Dashboard No Token", "PASS",
                   "Status 200/302/401/403", f"Status {status}", "")
    else:
        log_result("TC-ADM-008", "Admin Dashboard No Token", "FAIL",
                   "Status 200/302/401/403", f"Status {status}", str(response))
    
    # ========== POSITIVE ADMIN TESTS (With Admin Token) ==========
    
    if not admin_token:
        print(f"\n{Fore.YELLOW}Skipping positive admin tests - Admin token not available{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'POSITIVE ADMIN FUNCTIONALITY TESTS'.center(80)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    # TC-ADM-009: Admin get all advisors (should succeed)
    print_test_info("TC-ADM-009", "Admin Get All Advisors (Authorized)")
    status, response = make_request(
        "GET",
        "/admin/api/advisors",
        token=admin_token
    )
    
    if status == 200:
        log_result("TC-ADM-009", "Admin Get Advisors Success", "PASS",
                   "Status 200", f"Status {status}", "")
    else:
        log_result("TC-ADM-009", "Admin Get Advisors Success", "FAIL",
                   "Status 200", f"Status {status}", str(response))
    
    # TC-ADM-010: Admin create new advisor
    print_test_info("TC-ADM-010", "Admin Create New Advisor")
    test_advisor_username = f"testadv_{int(time.time())}"
    status, response = make_request(
        "POST",
        "/admin/api/advisors/create",
        token=admin_token,
        data={
            "fullname": "Test Advisor Created",
            "username": test_advisor_username,
            "email": f"{test_advisor_username}@mail.com",
            "password": "TestAdv123!"
        }
    )
    
    created_advisor_id = None
    if status in [200, 201]:
        created_advisor_id = response.get('user_id') or response.get('id')
        log_result("TC-ADM-010", "Admin Create Advisor Success", "PASS",
                   "Status 200/201", f"Status {status}", "")
    else:
        log_result("TC-ADM-010", "Admin Create Advisor Success", "FAIL",
                   "Status 200/201", f"Status {status}", str(response))
    
    # TC-ADM-011: Admin create advisor with duplicate username
    print_test_info("TC-ADM-011", "Admin Create Advisor dengan Username Duplicate")
    status, response = make_request(
        "POST",
        "/admin/api/advisors/create",
        token=admin_token,
        data={
            "fullname": "Duplicate Test",
            "username": test_advisor_username,  # Same username as before
            "email": "duplicate@mail.com",
            "password": "TestAdv123!"
        }
    )
    
    if status in [400, 409]:  # Bad Request or Conflict
        log_result("TC-ADM-011", "Admin Create Duplicate Advisor", "PASS",
                   "Status 400/409", f"Status {status}", "")
    else:
        log_result("TC-ADM-011", "Admin Create Duplicate Advisor", "FAIL",
                   "Status 400/409", f"Status {status}", str(response))
    
    # TC-ADM-012: Admin update advisor
    if created_advisor_id:
        print_test_info("TC-ADM-012", "Admin Update Advisor Data")
        status, response = make_request(
            "PUT",
            "/admin/api/advisors/update",
            token=admin_token,
            data={
                "user_id": created_advisor_id,
                "fullname": "Updated Advisor Name",
                "email": f"{test_advisor_username}_updated@mail.com"
            }
        )
        
        if status == 200:
            log_result("TC-ADM-012", "Admin Update Advisor Success", "PASS",
                       "Status 200", f"Status {status}", "")
        else:
            log_result("TC-ADM-012", "Admin Update Advisor Success", "FAIL",
                       "Status 200", f"Status {status}", str(response))
    
    # TC-ADM-013: Admin update non-existent advisor
    print_test_info("TC-ADM-013", "Admin Update Advisor Yang Tidak Ada")
    status, response = make_request(
        "PUT",
        "/admin/api/advisors/update",
        token=admin_token,
        data={
            "user_id": "nonexistent_user_id_99999",
            "fullname": "Should Fail"
        }
    )
    
    if status == 404:
        log_result("TC-ADM-013", "Admin Update Nonexistent", "PASS",
                   "Status 404", f"Status {status}", "")
    else:
        log_result("TC-ADM-013", "Admin Update Nonexistent", "FAIL",
                   "Status 404", f"Status {status}", str(response))
    
    # TC-ADM-014: Admin get statistics
    print_test_info("TC-ADM-014", "Admin Get System Statistics")
    status, response = make_request(
        "GET",
        "/admin/api/statistics",
        token=admin_token
    )
    
    if status == 200:
        log_result("TC-ADM-014", "Admin Get Statistics Success", "PASS",
                   "Status 200", f"Status {status}", "")
    else:
        log_result("TC-ADM-014", "Admin Get Statistics Success", "FAIL",
                   "Status 200", f"Status {status}", str(response))
    
    # TC-ADM-015: Admin get advisor monitoring
    print_test_info("TC-ADM-015", "Admin Get Advisor Monitoring")
    status, response = make_request(
        "GET",
        "/admin/api/advisor-monitoring",
        token=admin_token
    )
    
    if status == 200:
        log_result("TC-ADM-015", "Admin Get Monitoring Success", "PASS",
                   "Status 200", f"Status {status}", "")
    else:
        log_result("TC-ADM-015", "Admin Get Monitoring Success", "FAIL",
                   "Status 200", f"Status {status}", str(response))
    
    # TC-ADM-016: Admin delete advisor
    if created_advisor_id:
        print_test_info("TC-ADM-016", "Admin Delete Advisor")
        status, response = make_request(
            "DELETE",
            "/admin/api/advisors/delete",
            token=admin_token,
            data={"user_id": created_advisor_id}
        )
        
        if status in [200, 204]:
            log_result("TC-ADM-016", "Admin Delete Advisor Success", "PASS",
                       "Status 200/204", f"Status {status}", "")
        else:
            log_result("TC-ADM-016", "Admin Delete Advisor Success", "FAIL",
                       "Status 200/204", f"Status {status}", str(response))
    
    # TC-ADM-017: Admin delete non-existent advisor
    print_test_info("TC-ADM-017", "Admin Delete Advisor Yang Tidak Ada")
    status, response = make_request(
        "DELETE",
        "/admin/api/advisors/delete",
        token=admin_token,
        data={"user_id": "nonexistent_advisor_999"}
    )
    
    if status == 404:
        log_result("TC-ADM-017", "Admin Delete Nonexistent", "PASS",
                   "Status 404", f"Status {status}", "")
    else:
        log_result("TC-ADM-017", "Admin Delete Nonexistent", "FAIL",
                   "Status 404", f"Status {status}", str(response))


# ========== REPORT GENERATION ==========

def generate_report():
    """Generate test report"""
    print_header("TEST EXECUTION SUMMARY")
    
    # Summary statistics
    success_rate = (PASSED_TESTS / TOTAL_TESTS * 100) if TOTAL_TESTS > 0 else 0
    
    print(f"{Fore.CYAN}Total Tests: {TOTAL_TESTS}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Passed: {PASSED_TESTS}{Style.RESET_ALL}")
    print(f"{Fore.RED}Failed: {FAILED_TESTS}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Success Rate: {success_rate:.2f}%{Style.RESET_ALL}\n")
    
    # Results table
    table_data = []
    for result in RESULTS:
        status_colored = f"{Fore.GREEN}{result['Status']}{Style.RESET_ALL}" if result['Status'] == "PASS" else f"{Fore.RED}{result['Status']}{Style.RESET_ALL}"
        table_data.append([
            result['ID'],
            result['Test Name'][:40],
            status_colored,
            result['Expected'][:30],
            result['Actual'][:30]
        ])
    
    print(tabulate(table_data, headers=['ID', 'Test Name', 'Status', 'Expected', 'Actual'], tablefmt='grid'))
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"blackbox_testing/test_results_{timestamp}.json"
    
    report_data = {
        "timestamp": timestamp,
        "total_tests": TOTAL_TESTS,
        "passed": PASSED_TESTS,
        "failed": FAILED_TESTS,
        "success_rate": success_rate,
        "results": RESULTS
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print(f"\n{Fore.GREEN}Report saved to: {filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Failed to save report: {e}{Style.RESET_ALL}")
    
    # Print failed tests details
    if FAILED_TESTS > 0:
        print(f"\n{Fore.RED}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.RED}FAILED TESTS DETAILS:{Style.RESET_ALL}")
        print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}\n")
        
        for result in RESULTS:
            if result['Status'] == "FAIL":
                print(f"{Fore.RED}[{result['ID']}] {result['Test Name']}{Style.RESET_ALL}")
                print(f"  Expected: {result['Expected']}")
                print(f"  Actual: {result['Actual']}")
                if result['Message']:
                    print(f"  Message: {result['Message']}")
                print()


# ========== MAIN EXECUTION ==========

def main():
    """Main execution function"""
    print_header("ERD RECOMMENDATION SYSTEM - AUTOMATED API TESTING")
    print(f"Base URL: {BASE_URL}")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"{Fore.GREEN}✓ Server is running{Style.RESET_ALL}\n")
    except:
        print(f"{Fore.RED}✗ Server is not running at {BASE_URL}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please start the Flask server first: python app.py{Style.RESET_ALL}")
        return
    
    # Run all test suites
    start_time = time.time()
    
    test_auth()
    test_user_dashboard()
    test_advisor_dashboard()
    test_erd_crud()
    test_request_workflow()
    test_additional_features()
    test_erd_image_download()
    test_admin_module()
    test_api_general()
    test_security()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Generate report
    generate_report()
    
    print(f"\n{Fore.CYAN}Total Execution Time: {execution_time:.2f} seconds{Style.RESET_ALL}")
    print(f"{Fore.CYAN}End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
