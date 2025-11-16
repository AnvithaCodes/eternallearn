"""Visual Learning Tool - Generates diagrams"""

class VisualTool:
    """Creates visual representations"""
    
    def __init__(self):
        self.name = "visual_generator"
    
    def generate_concept_map(self, topic: str, concepts: list) -> str:
        """Generate Mermaid concept map"""
        mermaid = f"```mermaid\ngraph TD\n    A[{topic}]\n"
        for i, concept in enumerate(concepts, 1):
            mermaid += f"    A --> B{i}[{concept}]\n"
        mermaid += "```"
        return mermaid
    
    def generate_process_flow(self, topic: str, steps: list) -> str:
        """Generate process flowchart"""
        mermaid = f"```mermaid\nflowchart LR\n    Start([{topic}])\n"
        prev = "Start"
        for i, step in enumerate(steps, 1):
            current = f"Step{i}"
            mermaid += f"    {prev} --> {current}[{step}]\n"
            prev = current
        mermaid += f"    {prev} --> End([Complete])\n```"
        return mermaid

visual_tool = VisualTool()