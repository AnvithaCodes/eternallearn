"""Memory Agent - Tracks progress"""
from services.memory_bank import memory_bank
import logging

logger = logging.getLogger(__name__)

class MemoryAgent:
    """Manages student progress"""
    
    def __init__(self):
        self.name = "Memory"
    
    def get_progress(self, student_id: str) -> str:
        """Get progress report"""
        logger.info(f"Getting progress for {student_id}")
        
        try:
            summary = memory_bank.get_progress_summary(student_id)
            profile = memory_bank.get_student_profile(student_id)
            
            # add recent quizzes
            recent = profile.get("quiz_history", [])[-3:]
            if recent:
                summary += "\n\n**Recent Quizzes:**\n"
                for quiz in recent:
                    summary += f"• {quiz['topic']}: {quiz['score']*100:.0f}%\n"
            
            return summary
            
        except Exception as e:
            logger.error(f"Error: {e}")
            return "Unable to retrieve progress."

memory_agent = MemoryAgent()