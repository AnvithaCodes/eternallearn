"""Quizzer Agent - Generates quizzes"""
import google.generativeai as genai
from config import Config
from services.memory_bank import memory_bank
import logging
import re

logger = logging.getLogger(__name__)

class QuizzerAgent:
    """Creates and evaluates quizzes"""
    
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL_NAME)
        self.name = "Quizzer"
    
    def generate_quiz(self, request: str, context: dict) -> str:
        """Generate quiz questions"""
        logger.info(f"Generating quiz")
        
        # Extract topic from request
        topic = self._extract_topic(request)
        if not topic:
            topic = context["session"].current_topic or "general knowledge"
        
        # Update session topic
        context["session"].current_topic = topic
        
        prompt = f"""Create a quiz on: {topic}

Generate exactly 5 multiple-choice questions. Format:

Q1: [Question]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct: [A/B/C/D]

Make questions test understanding."""

        try:
            response = self.model.generate_content(prompt)
            quiz_text = response.text
            
            # store quiz
            context["session"].context["current_quiz"] = {
                "topic": topic,
                "quiz_text": quiz_text
            }
            
            # format for student (hide answers)
            lines = quiz_text.split('\n')
            formatted = [line for line in lines if not line.startswith('Correct:')]
            
            result = f"**Quiz: {topic}**\n\n"
            result += '\n'.join(formatted)
            result += "\n\n**Submit answers as:** `1.A 2.B 3.C 4.D 5.A`"
            
            return result
            
        except Exception as e:
            logger.error(f"Error: {e}")
            return "I had trouble creating a quiz. Please try again."
    
    def evaluate_answers(self, student_id: str, answers: str, session) -> str:
        """Evaluate quiz answers"""
        logger.info(f"Evaluating answers")
        
        quiz_data = session.context.get("current_quiz")
        if not quiz_data:
            return "No active quiz found!"
        
        # Parse student answers
        student_ans = {}
        matches = re.findall(r'(\d+)\.([A-Da-d])', answers)
        for num, letter in matches:
            student_ans[int(num)] = letter.upper()
        
        # Extract correct answers
        correct_ans = {}
        for line in quiz_data["quiz_text"].split('\n'):
            if line.startswith('Correct:'):
                q_num = len(correct_ans) + 1
                correct_ans[q_num] = line.split(':')[-1].strip().upper()
        
        # Calculate score
        correct_count = sum(1 for q in student_ans if student_ans.get(q) == correct_ans.get(q))
        total = len(correct_ans)
        score = correct_count / total if total > 0 else 0
        
        feedback = f"📊 **Quiz Results: {quiz_data['topic']}**\n\n"
        for i in range(1, total + 1):
            student = student_ans.get(i, "?")
            correct = correct_ans.get(i, "?")
            if student == correct:
                feedback += f"✅ Q{i}: Correct!\n"
            else:
                feedback += f"❌ Q{i}: Your answer: {student}, Correct: {correct}\n"
        
        feedback += f"\n**Score: {correct_count}/{total} ({score*100:.0f}%)**\n\n"
        
        if score >= 0.8:
            feedback += "🎉 Excellent work!\n"
        elif score >= 0.6:
            feedback += "👍 Good job!\n"
        else:
            feedback += "💪 Keep practicing!\n"
        
        # Save to memory
        memory_bank.add_quiz_result(
            student_id, quiz_data["topic"], score, total, correct_count, []
        )
        
        return feedback
    
    def _extract_topic(self, request: str) -> str:
        """Extract topic from quiz request"""
        request_lower = request.lower()
        
        # Common patterns
        patterns = [
            r'quiz me on (.+)',
            r'quiz me about (.+)',
            r'quiz on (.+)',
            r'quiz about (.+)',
            r'test me on (.+)',
            r'(.+) quiz'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, request_lower)
            if match:
                return match.group(1).strip()
        
        return None

quizzer_agent = QuizzerAgent()