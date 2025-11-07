from pymongo import MongoClient
from config import Config
from bson import ObjectId

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
    
    def find_erd_by_id(self, erd_id):
        """Find ERD by erd_id"""
        return self.erd_collection.find_one({"erd_id": erd_id})
    
    def save_erd(self, erd_data):
        """Save ERD to database"""
        return self.erd_collection.insert_one(erd_data)
    
    def get_all_erds(self):
        """Get all ERDs from database"""
        return list(self.erd_collection.find({}))
    
    def get_erds_for_display(self):
        """Get ERDs with display names for listing"""
        erds = list(self.erd_collection.find({}, {"_id": 0, "name": 1}))
        for erd in erds:
            erd['display_name'] = erd['name'].replace('_', ' ').title()
        return erds
    
    def get_erds_by_advisor_id(self, advisor_id):
        """Get all ERDs created by specific advisor from ERD collection"""
        return list(self.erd_collection.find({"advisor_id": advisor_id}).sort("created_at", -1))
    
    def update_erd(self, erd_id, update_data):
        """Update ERD by erd_id"""
        return self.erd_collection.update_one(
            {"erd_id": erd_id},
            {"$set": update_data}
        )
    
    def delete_erd_by_id(self, erd_id):
        """Delete ERD by erd_id"""
        return self.erd_collection.delete_one({"erd_id": erd_id})
    
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
    
    def get_all_users_by_role(self, role):
        """Get all users by role"""
        return list(self.users_collection.find({"role": role}))
    
    def update_user(self, user_id, update_data):
        """Update user data"""
        return self.users_collection.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
    
    def delete_user(self, user_id):
        """Delete user (soft delete by setting is_active to False)"""
        return self.users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"is_active": False}}
        )
    
    def hard_delete_user(self, user_id):
        """Permanently delete user"""
        return self.users_collection.delete_one({"user_id": user_id})
    
    # ERD deletion methods
    def delete_erd(self, erd_name):
        """Delete ERD by name (legacy support)"""
        return self.erd_collection.delete_one({"name": erd_name})
    
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
    
    # Admin Statistics Methods
    def get_statistics(self):
        """Get system statistics for admin"""
        total_users = self.users_collection.count_documents({"role": "user", "is_active": True})
        total_advisors = self.users_collection.count_documents({"role": "advisor", "is_active": True})
        total_requests = self.requests_collection.count_documents({})
        total_erds = self.erd_collection.count_documents({})
        pending_requests = self.requests_collection.count_documents({"status": "pending"})
        completed_requests = self.requests_collection.count_documents({"status": "complete"})
        
        return {
            "total_users": total_users,
            "total_advisors": total_advisors,
            "total_requests": total_requests,
            "total_erds": total_erds,
            "pending_requests": pending_requests,
            "completed_requests": completed_requests
        }
    
    def get_advisor_activity(self, advisor_id):
        """Get activity statistics for specific advisor"""
        # Count ERDs created by advisor
        total_erds = self.erd_collection.count_documents({"advisor_id": advisor_id})
        
        # Count requests completed by advisor
        completed_requests = self.requests_collection.count_documents({
            "advisor_id": advisor_id,
            "status": "complete"
        })
        
        # Count requests currently being processed
        in_progress_requests = self.requests_collection.count_documents({
            "advisor_id": advisor_id,
            "status": "on_process"
        })
        
        return {
            "total_erds": total_erds,
            "completed_requests": completed_requests,
            "in_progress_requests": in_progress_requests
        }
    
    def get_all_advisor_activities(self):
        """Get activity statistics for all advisors"""
        advisors = self.get_all_advisors()
        activities = []
        
        for advisor in advisors:
            activity = self.get_advisor_activity(advisor['user_id'])
            activities.append({
                "advisor_id": advisor['user_id'],
                "username": advisor['username'],
                "email": advisor['email'],
                "total_erds": activity['total_erds'],
                "completed_requests": activity['completed_requests'],
                "in_progress_requests": activity['in_progress_requests']
            })
        
        return activities

# Global database instance
db = Database()