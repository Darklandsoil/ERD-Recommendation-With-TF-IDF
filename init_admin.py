#!/usr/bin/env python3
"""
Script to initialize admin account in the database
Run this script once to create the default admin account
"""

from models.database import db
from models.user_model import UserModel

def init_admin():
    """Initialize admin account"""
    
    # Check if admin already exists
    existing_admin = db.find_user_by_username("admin")
    if existing_admin:
        print("Admin account already exists!")
        print(f"Username: {existing_admin['username']}")
        print(f"Email: {existing_admin['email']}")
        return
    
    # Create admin account
    admin = UserModel(
        username="admin",
        email="admin@erdgenerator.com",
        password="admin123",
        role="admin"
    )
    
    # Save to database
    result = db.create_user(admin.to_dict())
    
    if result:
        print("✅ Admin account created successfully!")
        print(f"Username: admin")
        print(f"Password: admin123")
        print(f"Email: admin@erdgenerator.com")
        print("\n⚠️  Please login and change the default password!")
    else:
        print("❌ Failed to create admin account!")

if __name__ == "__main__":
    init_admin()
