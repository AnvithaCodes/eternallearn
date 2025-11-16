"""
EternaLearn - Main Entry Point
Multi-agent adaptive learning system
"""
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from agents.coordinator import coordinator
from services.memory_bank import memory_bank #new
from agents.teacher_agent import teacher_agent
from agents.quizzer_agent import quizzer_agent
from agents.memory_agent import memory_agent
from config import Config
import logging

logging.basicConfig(
    level=Config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

console = Console()

class EternaLearn:
    """Main application"""
    
    def __init__(self):
        self.coordinator = coordinator
        self.teacher = teacher_agent
        self.quizzer = quizzer_agent
        self.memory = memory_agent
        self.current_student = "student_001"
        logger.info("🎓 EternaLearn initialized")
    
    def display_welcome(self):
        """Display welcome"""
        welcome = """
# Welcome to EternaLearn!

Your AI-powered adaptive learning companion.

**What I can do:**
- Explain complex topics with visual aids
- Generate personalized quizzes
- Track your learning progress

**Commands:**
- Type any topic to learn
- Say "quiz me on [topic]" to practice
- Say "show my progress" for stats
- Type "exit" to quit

Let's make learning eternal :)
"""
        console.print(Panel(Markdown(welcome), style="bold blue"))
    
    def process_message(self, message: str) -> str:
        """Process student message"""
        message_lower = message.lower()
        
        if message_lower in ["progress", "show my progress", "my stats"]:
            return self.memory.get_progress(self.current_student)
        
        if "quiz" in message_lower:
            from services.session_service import session_service
            session = session_service.get_or_create_session(self.current_student)
            
            context = {
                "agent": "quizzer",
                "session": session,
                "profile": memory_bank.get_student_profile(self.current_student),
                "original_message": message
            }
            
            return self.quizzer.generate_quiz(message, context)
        
        # check if quiz answers
        if any(c.isdigit() and '.' in message for c in message):
            from services.session_service import session_service
            session = session_service.get_or_create_session(self.current_student)
            
            if "current_quiz" in session.context:
                return self.quizzer.evaluate_answers(
                    self.current_student, message, session
                )
        
        # route through coordinator
        return self.coordinator.coordinate_response(
            self.current_student, message, 
            self.teacher, self.quizzer, self.memory
        )
    
    def run_interactive(self):
        """Run interactive mode"""
        self.display_welcome()
        
        while True:
            try:
                console.print("\n[bold cyan]You:[/bold cyan]", end=" ")
                user_input = input().strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    console.print("\n[bold green]Happy learning![/bold green]")
                    break
                
                console.print("\n[bold yellow]EternaLearn:[/bold yellow]")
                response = self.process_message(user_input)
                console.print(Panel(Markdown(response), style="green"))
                
            except KeyboardInterrupt:
                console.print("\n\n[bold red]Goodbye![/bold red]")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                console.print(f"\n[bold red]Error: {e}[/bold red]")

def main():
    """Entry point"""
    app = EternaLearn()
    app.run_interactive()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        console.print(f"[bold red]Fatal error: {e}[/bold red]")