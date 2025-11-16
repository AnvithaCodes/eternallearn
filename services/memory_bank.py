"""Memory Bank - Persistent student data storage"""
import json
import os
from datetime import datetime
from pathlib import Path

class MemoryBank:
    """Manages persistent storage of student learning data"""
    
    def __init__(self, storage_path: str = "./data/memory_bank.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.memory = self._load_memory()
    
    def _load_memory(self):
        """Load memory from disk"""
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {"students": {}, "metadata": {"created_at": datetime.now().isoformat()}}
    
    def _save_memory(self):
        """Save memory to disk"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def get_student_profile(self, student_id: str):
        """Get or create student profile"""
        if student_id not in self.memory["students"]:
            self.memory["students"][student_id] = {
                "id": student_id,
                "created_at": datetime.now().isoformat(),
                "topics_covered": [],
                "quiz_history": [],
                "weak_areas": [],
                "strong_areas": [],
                "preferences": {
                    "learning_style": "visual",
                    "difficulty_level": "medium"
                },
                "stats": {
                    "total_topics": 0,
                    "total_quizzes": 0,
                    "average_score": 0.0
                }
            }
            self._save_memory()
        return self.memory["students"][student_id]
    
    def add_quiz_result(self, student_id: str, topic: str, score: float, 
                       total_questions: int, correct_answers: int, questions: list):
        """Record quiz result"""
        profile = self.get_student_profile(student_id)
        
        quiz_entry = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "score": score,
            "total_questions": total_questions,
            "correct_answers": correct_answers
        }
        
        profile["quiz_history"].append(quiz_entry)
        profile["stats"]["total_quizzes"] += 1
        
        # Update average
        all_scores = [q["score"] for q in profile["quiz_history"]]
        profile["stats"]["average_score"] = sum(all_scores) / len(all_scores)
        
        # Update topic progress
        if topic not in profile["topics_covered"]:
            profile["topics_covered"].append(topic)
            profile["stats"]["total_topics"] += 1
        
        # Categorize strength
        if score >= 0.8 and topic not in profile["strong_areas"]:
            profile["strong_areas"].append(topic)
        elif score < 0.6 and topic not in profile["weak_areas"]:
            profile["weak_areas"].append(topic)
        
        self._save_memory()
    
    def get_progress_summary(self, student_id: str) -> str:
        """Generate progress summary"""
        profile = self.get_student_profile(student_id)
        stats = profile["stats"]
        
        summary = f"""
Learning Progress for {student_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topics Covered: {stats['total_topics']}
Quizzes Completed: {stats['total_quizzes']}
Average Score: {stats['average_score']*100:.1f}%
Strong Areas: {', '.join(profile['strong_areas'][:3]) or 'None yet'}
Areas to Review: {', '.join(profile['weak_areas'][:3]) or 'None'}
"""
        return summary.strip()

# Global instance
memory_bank = MemoryBank()