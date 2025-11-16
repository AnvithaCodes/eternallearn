"""
EternaLearn - web interface for hugging face spaces
"""
import gradio as gr
from agents.coordinator import coordinator
from agents.teacher_agent import teacher_agent
from agents.quizzer_agent import quizzer_agent
from agents.memory_agent import memory_agent
from services.memory_bank import memory_bank
from services.session_service import session_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EternaLearnWeb:
    def __init__(self):
        self.coordinator = coordinator
        self.teacher = teacher_agent
        self.quizzer = quizzer_agent
        self.memory = memory_agent
        logger.info("EternaLearn Web Interface Initialized")
    
    def process_message(self, message: str, history: list) -> str:
        try:
            if not message or message.strip() == "":
                return "Please enter a message :)"
            
            student_id = "student_web_001"
            message_lower = message.lower().strip()
            
            if any(keyword in message_lower for keyword in ["progress", "stats", "my progress"]):
                return "### Learning Progress\n\n" + self.memory.get_progress(student_id)
            
            if "quiz" in message_lower and not any(c.isdigit() and '.' in message for c in message):
                session = session_service.get_or_create_session(student_id)
                context = {
                    "agent": "quizzer",
                    "session": session,
                    "profile": memory_bank.get_student_profile(student_id),
                    "original_message": message
                }
                return "### Quiz Time\n\n" + self.quizzer.generate_quiz(message, context)
            
            if any(c.isdigit() and '.' in message for c in message):
                session = session_service.get_or_create_session(student_id)
                if "current_quiz" in session.context:
                    return "### Quiz Results\n\n" + self.quizzer.evaluate_answers(student_id, message, session)
            
            response = self.coordinator.coordinate_response(
                student_id, message,
                self.teacher, self.quizzer, self.memory
            )
            return "### Explanation\n\n" + response
            
        except Exception as e:
            logger.error(f"Error: {e}")
            return f"Error: {str(e)}\n\nPlease try again!"

logger.info("Initializing EternaLearn Web App...")
app = EternaLearnWeb()

def chat(message, history):
    return app.process_message(message, history)

# simple interface
demo = gr.ChatInterface(
    fn=chat,
    title="EternaLearn - AI Learning Companion",
    description="""
    **Your adaptive learning assistant powered by multi-agent AI**
    
    **What I can do:**
    - Explain any topic in detail
    - Generate personalized quizzes  
    - Track your learning progress
    
    **Try these:**
    - "Explain photosynthesis"
    - "Quiz me on water cycle"
    - "Show my progress"
    """,
    examples=[
        "Explain quantum physics",
        "Explain the water cycle",
        "Quiz me on photosynthesis",
        "Show my progress"
    ],
)

if __name__ == "__main__":
    demo.launch()