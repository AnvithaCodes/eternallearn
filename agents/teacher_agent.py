"""Teacher Agent - Explains concepts"""
import google.generativeai as genai
from config import Config
import logging
import re

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
            prompt = f"""Create a simple Mermaid flowchart for: {topic}

CRITICAL RULES:
1. Start with EXACTLY: graph TD
2. Use this EXACT format for each line: A[Label] --> B[Label]
3. Use only letters A-Z for node IDs
4. Put labels in square brackets: [Label Text]
5. Use --> for arrows
6. Maximum 6 nodes
7. No special characters in labels (avoid quotes, apostrophes)

Example format:
graph TD
A[Start] --> B[Process]
B --> C[End]

Return ONLY the Mermaid code, nothing else."""

            response = self.model.generate_content(prompt)
            mermaid_code = response.text.strip()
            
            mermaid_code = mermaid_code.replace("```mermaid", "").replace("```", "").strip()
            mermaid_code = mermaid_code.replace("flowchart TD", "graph TD")
            mermaid_code = mermaid_code.replace("flowchart LR", "graph LR")
            
            lines = mermaid_code.split('\n')
            cleaned_lines = []
            for line in lines:
                line = line.strip()
                if line.startswith('graph ') or '-->' in line or line == '':
                    cleaned_lines.append(line)
            
            mermaid_code = '\n'.join(cleaned_lines).strip()
            
            if not mermaid_code.startswith('graph '):
                logger.warning(f"Invalid Mermaid start: {mermaid_code[:50]}")
                return self._create_fallback_diagram(topic)
            
            # node check
            if '-->' not in mermaid_code:
                logger.warning("No arrows found in Mermaid code")
                return self._create_fallback_diagram(topic)
            
            return f"\n\n**Visual Diagram:**\n```mermaid\n{mermaid_code}\n```"
            
        except Exception as e:
            logger.error(f"Diagram generation error: {e}")
            return self._create_fallback_diagram(topic)
    
    def _create_fallback_diagram(self, topic: str) -> str:
        """Create a simple fallback diagram when AI generation fails"""
        # template based diags for common topics
        if 'water cycle' in topic.lower():
            return """

**Visual Diagram:**
```mermaid
graph TD
A[Evaporation] --> B[Condensation]
B --> C[Precipitation]
C --> D[Collection]
D --> A
```"""
        elif 'photosynthesis' in topic.lower():
            return """

**Visual Diagram:**
```mermaid
graph LR
A[Sunlight] --> B[Chlorophyll]
C[Water] --> B
D[CO2] --> B
B --> E[Glucose]
B --> F[Oxygen]
```"""
        else:
            # generic process diagram
            return """

**Visual Diagram:**
```mermaid
graph TD
A[Input] --> B[Process]
B --> C[Output]
```"""

teacher_agent = TeacherAgent()