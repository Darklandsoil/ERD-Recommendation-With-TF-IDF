from pymongo import MongoClient
from config import Config

class Database:
    """Database connection and operations"""
    
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.DATABASE_NAME]
        self.collection = self.db[Config.COLLECTION_NAME]
    
    def find_erd_by_name(self, name):
        """Find ERD by name"""
        return self.collection.find_one({"name": name})
    
    def save_erd(self, erd_data):
        """Save ERD to database"""
        if not self.find_erd_by_name(erd_data["name"]):
            return self.collection.insert_one(erd_data)
        return None
    
    def get_all_erds(self):
        """Get all ERDs from database"""
        return list(self.collection.find({}))
    
    def get_erds_for_display(self):
        """Get ERDs with display names for listing"""
        erds = list(self.collection.find({}, {"_id": 0, "name": 1}))
        for erd in erds:
            erd['display_name'] = erd['name'].replace('_', ' ').title()
        return erds

# Global database instance
db = Database()