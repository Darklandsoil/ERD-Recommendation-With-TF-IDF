from pymongo import MongoClient
from config import Config

class Database:
    """Database connection and operations"""
    
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.DATABASE_NAME]
        self.erd_collection = self.db[Config.COLLECTION_NAME]
        self.users_collection = self.db[Config.USERS_COLLECTION]
        self.requests_collection = self.db[Config.REQUESTS_COLLECTION]
    
    # ERD Methods
    def find_erd_by_name(self, name):
        """Find ERD by name"""
        return self.erd_collection.find_one({"name": name})
    
    def save_erd(self, erd_data):
        """Save ERD to database"""
        if not self.find_erd_by_name(erd_data["name"]):
            return self.erd_collection.insert_one(erd_data)
        return None
    
    def get_all_erds(self):
        """Get all ERDs from database"""
        return list(self.erd_collection.find({}))
    
    def get_erds_for_display(self):
        """Get ERDs with display names for listing"""
        erds = list(self.erd_collection.find({}, {"_id": 0, "name": 1}))
        for erd in erds:
            erd['display_name'] = erd['name'].replace('_', ' ').title()
        return erds
    
    # User Methods
    def create_user(self, user_data):
        """Create new user"""
        # Check if username or email already exists
        if self.users_collection.find_one({"$or": [{"username": user_data["username"]}, {"email": user_data["email"]}]}):
            return None
        return self.users_collection.insert_one(user_data)
    
    def find_user_by_username(self, username):
        """Find user by username"""
        return self.users_collection.find_one({"username": username})
    
    def find_user_by_id(self, user_id):
        """Find user by user_id"""
        return self.users_collection.find_one({"user_id": user_id})
    
    def find_user_by_email(self, email):
        """Find user by email"""
        return self.users_collection.find_one({"email": email})
    
    def get_all_advisors(self):
        """Get all advisors"""
        return list(self.users_collection.find({"role": "advisor", "is_active": True}))
    
    # Request Methods
    def create_request(self, request_data):
        """Create new request"""
        return self.requests_collection.insert_one(request_data)
    
    def find_request_by_id(self, request_id):
        """Find request by request_id"""
        return self.requests_collection.find_one({"request_id": request_id})
    
    def get_requests_by_user(self, user_id):
        """Get all requests by user"""
        return list(self.requests_collection.find({"user_id": user_id}).sort("created_at", -1))
    
    def get_requests_by_status(self, status):
        """Get requests by status"""
        return list(self.requests_collection.find({"status": status}).sort("created_at", -1))
    
    def get_requests_by_advisor(self, advisor_id):
        """Get requests assigned to advisor"""
        return list(self.requests_collection.find({"advisor_id": advisor_id}).sort("updated_at", -1))
    
    def update_request(self, request_id, update_data):
        """Update request"""
        return self.requests_collection.update_one(
            {"request_id": request_id},
            {"$set": update_data}
        )
    
    def get_pending_requests(self):
        """Get all pending requests"""
        return list(self.requests_collection.find({"status": "pending"}).sort("created_at", 1))

# Global database instance
db = Database()