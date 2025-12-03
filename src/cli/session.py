"""
Session management for the RJW-IDD CLI.

Handles conversation history, context persistence, and multi-turn interactions.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class Session:
    """
    Manages a conversation session with the RJW-IDD agent.
    
    Attributes:
        session_id: Unique identifier for the session
        history: List of conversation turns
        context: Session context and metadata
        output_dir: Directory for session artifacts
    """
    
    def __init__(self, session_id: Optional[str] = None, output_dir: str = ".rjw-sessions"):
        """
        Initialize a session.
        
        Args:
            session_id: Optional session ID (generates one if not provided)
            output_dir: Directory to store session data
        """
        self.session_id = session_id or self._generate_session_id()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.history: List[Dict] = []
        self.context: Dict = {
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'evidence_ids': [],
            'decision_ids': [],
            'spec_ids': [],
            'trust_level': 'SUPERVISED',
            'yolo_mode': False
        }
        
        # Try to load existing session
        self._load_session()
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        import random
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = ''.join(random.choices('0123456789abcdef', k=6))
        return f"session_{timestamp}_{random_suffix}"
    
    def _session_file(self) -> Path:
        """Get the session file path."""
        return self.output_dir / f"{self.session_id}.json"
    
    def _load_session(self):
        """Load session from disk if it exists."""
        session_file = self._session_file()
        if session_file.exists():
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    self.history = data.get('history', [])
                    self.context = data.get('context', self.context)
            except (json.JSONDecodeError, IOError):
                # If loading fails, start fresh
                pass
    
    def save(self):
        """Save session to disk."""
        self.context['updated_at'] = datetime.now().isoformat()
        
        session_data = {
            'session_id': self.session_id,
            'history': self.history,
            'context': self.context
        }
        
        with open(self._session_file(), 'w') as f:
            json.dump(session_data, f, indent=2)
    
    def add_turn(self, user_input: str, agent_response: Dict):
        """
        Add a conversation turn to the history.
        
        Args:
            user_input: User's input
            agent_response: Agent's response dictionary
        """
        turn = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'agent_response': agent_response
        }
        self.history.append(turn)
        
        # Update context with any new artifacts
        if 'evidence_ids' in agent_response:
            self.context['evidence_ids'].extend(agent_response['evidence_ids'])
        if 'decision_id' in agent_response:
            self.context['decision_ids'].append(agent_response['decision_id'])
        if 'spec_id' in agent_response:
            self.context['spec_ids'].append(agent_response['spec_id'])
        
        self.save()
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get conversation history.
        
        Args:
            limit: Maximum number of turns to return (most recent)
            
        Returns:
            List of conversation turns
        """
        if limit:
            return self.history[-limit:]
        return self.history
    
    def clear_history(self):
        """Clear conversation history."""
        self.history = []
        self.save()
    
    def get_summary(self) -> Dict:
        """
        Get a summary of the session.
        
        Returns:
            Dictionary with session statistics
        """
        return {
            'session_id': self.session_id,
            'turn_count': len(self.history),
            'created_at': self.context['created_at'],
            'updated_at': self.context['updated_at'],
            'evidence_count': len(set(self.context['evidence_ids'])),
            'decision_count': len(set(self.context['decision_ids'])),
            'spec_count': len(set(self.context['spec_ids'])),
            'trust_level': self.context['trust_level'],
            'yolo_mode': self.context['yolo_mode']
        }
    
    def update_context(self, key: str, value):
        """
        Update session context.
        
        Args:
            key: Context key
            value: Context value
        """
        self.context[key] = value
        self.save()
    
    @classmethod
    def list_sessions(cls, output_dir: str = ".rjw-sessions") -> List[str]:
        """
        List all available sessions.
        
        Args:
            output_dir: Directory containing session files
            
        Returns:
            List of session IDs
        """
        sessions_path = Path(output_dir)
        if not sessions_path.exists():
            return []
        
        session_files = sessions_path.glob("session_*.json")
        return [f.stem for f in session_files]
    
    @classmethod
    def delete_session(cls, session_id: str, output_dir: str = ".rjw-sessions"):
        """
        Delete a session.
        
        Args:
            session_id: Session ID to delete
            output_dir: Directory containing session files
        """
        session_file = Path(output_dir) / f"{session_id}.json"
        if session_file.exists():
            session_file.unlink()
