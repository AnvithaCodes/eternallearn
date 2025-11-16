"""Session Service - Manages conversation context"""
from datetime import datetime, timedelta

class Session:
    """Single learning session"""
    
    def __init__(self, session_id: str, student_id: str):
        self.session_id = session_id
        self.student_id = student_id
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.conversation_history = []
        self.current_topic = None
        self.context = {}
    
    def add_message(self, role: str, content: str):
        """Add message to history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.last_activity = datetime.now()
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """Check if session expired"""
        return datetime.now() - self.last_activity > timedelta(minutes=timeout_minutes)
    
    def get_context_summary(self) -> str:
        """Get context summary"""
        if not self.conversation_history:
            return "New session started."
        
        recent = self.conversation_history[-5:]
        summary = f"Current topic: {self.current_topic or 'General'}\n"
        summary += f"Recent messages ({len(recent)}):\n"
        for msg in recent:
            summary += f"- {msg['role']}: {msg['content'][:50]}...\n"
        return summary

class SessionService:
    """Manages multiple sessions"""
    
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, student_id: str) -> Session:
        """Create new session"""
        session_id = f"session_{student_id}_{datetime.now().timestamp()}"
        session = Session(session_id, student_id)
        self.sessions[session_id] = session
        return session
    
    def get_or_create_session(self, student_id: str) -> Session:
        """Get active session or create new"""
        for session in self.sessions.values():
            if session.student_id == student_id and not session.is_expired():
                return session
        return self.create_session(student_id)

session_service = SessionService()