"""Teacher Agent - Explains concepts"""
import google.generativeai as genai
from config import Config
from tools.visual_tool import visual_tool
import logging

logger = logging.getLogger(__name__)

class TeacherAgent:
    """Explains concepts with visuals"""
    
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL_NAME)
        self.name = "Teacher"
    
    def explain(self, topic: str, context: dict) -> str:
        """Explain a topic"""
        logger.info(f"Explaining: {topic}")
        
        prompt = f"""You are an expert teacher. Explain this topic clearly and engagingly:

Topic: {topic}

Provide:
1. Simple definition
2. Step-by-step breakdown
3. Real-world example
4. Key takeaway

Keep it 200-300 words, conversational tone."""

        try:
            response = self.model.generate_content(prompt)
            explanation = response.text
            
            # Add visual
            if Config.ENABLE_VISUAL_LEARNING:
                visual = visual_tool.generate_concept_map(topic, ["Concept 1", "Concept 2", "Concept 3"])
                explanation += f"\n\n**Visual Aid:**\n{visual}"
            
            context["session"].current_topic = topic
            return explanation
            
        except Exception as e:
            logger.error(f"Error: {e}")
            return f"I had trouble explaining {topic}. Could you rephrase your question?"

teacher_agent = TeacherAgent()