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

# Premium CSS with smooth animations and perfect contrast
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Smooth cursor on all interactive elements */
button, input, textarea {
    cursor: pointer !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

/* Container styling */
.gradio-container {
    max-width: 1000px !important;
    margin: 0 auto !important;
}

/* Example buttons hover */
.examples button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
}

/* Submit button styling */
button.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

button.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35) !important;
}

/* Message animation */
.message {
    animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
"""

# Create simple interface - let Gradio handle Mermaid rendering
demo = gr.ChatInterface(
    fn=chat,
    title="EternaLearn",
    description="AI-Powered Adaptive Learning System · Multi-Agent Intelligence",
    examples=[
        "Explain quantum physics",
        "Explain the water cycle",
        "Quiz me on photosynthesis",
        "Show my progress"
    ],
    css=custom_css,
    theme=gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="purple",
    )
)

if __name__ == "__main__":
    demo.launch()