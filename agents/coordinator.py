"""Coordinator Agent - Routes requests"""
import google.generativeai as genai
from config import Config
from services.session_service import session_service
from services.memory_bank import memory_bank
import logging

logger = logging.getLogger(__name__)

class CoordinatorAgent:
    """Main orchestrator agent"""
    
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL_NAME)
        self.name = "Coordinator"
    
    def route_request(self, student_id: str, message: str):
        """Route student request to appropriate agent"""
        logger.info(f"Routing request for {student_id}")
        
        session = session_service.get_or_create_session(student_id)
        profile = memory_bank.get_student_profile(student_id)
        
        # simple routing logic
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["quiz", "test", "questions"]):
            agent = "quizzer"
        elif any(word in message_lower for word in ["progress", "stats", "how am i doing"]):
            agent = "memory"
        else:
            agent = "teacher"
        
        logger.info(f"Routed to {agent}")
        
        return {
            "agent": agent,
            "session": session,
            "profile": profile,
            "original_message": message
        }
    
    def coordinate_response(self, student_id: str, message: str, 
                          teacher_agent, quizzer_agent, memory_agent) -> str:
        """Coordinate response from agents"""
        routing_info = self.route_request(student_id, message)
        
        if routing_info["agent"] == "teacher":
            response = teacher_agent.explain(message, routing_info)
        elif routing_info["agent"] == "quizzer":
            response = quizzer_agent.generate_quiz(message, routing_info)
        else:
            response = memory_agent.get_progress(student_id)
        
        routing_info["session"].add_message("student", message)
        routing_info["session"].add_message("assistant", response)
        
        return response

coordinator = CoordinatorAgent()