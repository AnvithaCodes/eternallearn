"""Teacher Agent - Explains concepts"""
import google.generativeai as genai
from config import Config
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
            
            # generate visual diagram for applicable topics
            if Config.ENABLE_VISUAL_LEARNING:
                visual_keywords = ["cycle", "process", "system", "photosynthesis", "respiration", 
                                 "circuit", "ecosystem", "reaction", "structure", "mechanism"]
                if any(keyword in topic.lower() for keyword in visual_keywords):
                    diagram = self._generate_diagram(topic)
                    if diagram:
                        explanation += f"\n\n{diagram}"
            
            context["session"].current_topic = topic
            return explanation
            
        except Exception as e:
            logger.error(f"Error: {e}")
            return f"I had trouble explaining {topic}. Could you rephrase your question?"
    
    def _generate_diagram(self, topic: str) -> str:
        """Generate a Mermaid diagram for the topic"""
        try:
            prompt = f"""Create a simple Mermaid flowchart diagram for: {topic}

Requirements:
- Use Mermaid flowchart syntax (graph TD or graph LR)
- 4-7 nodes maximum
- Show key concepts and their relationships
- Use arrows to show flow/connections
- Keep it simple and educational

Return ONLY the Mermaid code, no explanation, no markdown fences.
Start with 'graph TD' or 'graph LR'."""

            response = self.model.generate_content(prompt)
            mermaid_code = response.text.strip()
            
            # clean up response
            mermaid_code = mermaid_code.replace("```mermaid", "").replace("```", "").strip()
            
            # validate it starts with graph
            if not (mermaid_code.startswith("graph ") or mermaid_code.startswith("flowchart ")):
                return None
            
            return f"\n\n**Visual Diagram:**\n```mermaid\n{mermaid_code}\n```"
            
        except Exception as e:
            logger.error(f"Diagram generation error: {e}")
            return None

teacher_agent = TeacherAgent()