#!/usr/bin/env python3
"""
Script to create default admin account
Run this script once to initialize the admin account
"""

import sys
sys.path.insert(0, '/app')

from models.database import db
from models.user_model import UserModel

def create_admin():
    """Create default admin account"""
    
    # Default admin credentials
    admin_username = "admin"
    admin_email = "admin@erdgenerator.com"
    admin_password = "Admin123"
    
    # Check if admin already exists
    existing_admin = db.find_user_by_username(admin_username)
    if existing_admin:
        print(f"❌ Admin account '{admin_username}' already exists!")
        print(f"   User ID: {existing_admin['user_id']}")
        print(f"   Email: {existing_admin['email']}")
        return False
    
    # Create admin user
    admin = UserModel(
        username=admin_username,
        email=admin_email,
        password=admin_password,
        role='admin'
    )
    
    # Validate
    is_valid, errors = admin.validate()
    if not is_valid:
        print(f"❌ Validation failed: {'; '.join(errors)}")
        return False
    
    # Save to database
    result = db.create_user(admin.to_dict())
    
    if result:
        print("✅ Admin account created successfully!")
        print(f"   Username: {admin_username}")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        print(f"   User ID: {admin.user_id}")
        print(f"\n⚠️  PENTING: Silakan ganti password setelah login pertama!")
        return True
    else:
        print("❌ Failed to create admin account (email might already exist)")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("ERD Generator - Admin Account Initialization")
    print("=" * 60)
    print()
    create_admin()
    print()
    print("=" * 60)
