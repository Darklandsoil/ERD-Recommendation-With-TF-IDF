from datetime import datetime
import uuid

class RequestModel:
    """Request model for ERD creation requests"""
    
    def __init__(self, user_id=None, query=None, description=None):
        self.request_id = str(uuid.uuid4())
        self.user_id = user_id
        self.query = query
        self.description = description
        self.status = "pending"  # pending, on_process, complete, cancelled
        self.advisor_id = None  # assigned advisor
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.completed_at = None
        self.erd_result = None  # ERD data when completed
        self.notes = None  # advisor notes
    
    def assign_advisor(self, advisor_id):
        """Assign advisor to request and change status to on_process"""
        self.advisor_id = advisor_id
        self.status = "on_process"
        self.updated_at = datetime.now()
    
    def complete_request(self, erd_result, notes=None):
        """Complete request with ERD result"""
        self.erd_result = erd_result
        self.notes = notes
        self.status = "complete"
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
    
    def cancel_request(self):
        """Cancel pending request"""
        if self.status == "pending":
            self.status = "cancelled"
            self.updated_at = datetime.now()
            return True
        return False
    
    def to_dict(self):
        """Convert to dictionary for MongoDB storage"""
        return {
            "request_id": self.request_id,
            "user_id": self.user_id,
            "query": self.query,
            "description": self.description,
            "status": self.status,
            "advisor_id": self.advisor_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completed_at": self.completed_at,
            "erd_result": self.erd_result,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create RequestModel from dictionary"""
        request = cls()
        request.request_id = data.get("request_id")
        request.user_id = data.get("user_id")
        request.query = data.get("query")
        request.description = data.get("description")
        request.status = data.get("status", "pending")
        request.advisor_id = data.get("advisor_id")
        request.created_at = data.get("created_at")
        request.updated_at = data.get("updated_at")
        request.completed_at = data.get("completed_at")
        request.erd_result = data.get("erd_result")
        request.notes = data.get("notes")
        return request
    
    def validate(self):
        """Validate request data"""
        errors = []
        
        if not self.user_id:
            errors.append("User ID diperlukan")
        
        if not self.query or len(self.query.strip()) < 3:
            errors.append("Query harus minimal 3 karakter")
        
        if not self.description or len(self.description.strip()) < 10:
            errors.append("Deskripsi harus minimal 10 karakter")
        
        return len(errors) == 0, errors
    
    def get_status_display(self):
        """Get human readable status"""
        status_map = {
            "pending": "Menunggu",
            "on_process": "Sedang Dikerjakan", 
            "complete": "Selesai",
            "cancelled": "Dibatalkan"
        }
        return status_map.get(self.status, self.status)