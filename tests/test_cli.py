"""Tests for the CLI module."""
import unittest
import tempfile
import shutil
from pathlib import Path

from src.cli.session import Session
from src.cli.formatter import Formatter
from src.cli.interactive import InteractiveREPL


class TestSession(unittest.TestCase):
    """Test session management."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.session = Session(output_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_session_creation(self):
        """Test session is created with ID."""
        self.assertIsNotNone(self.session.session_id)
        self.assertTrue(self.session.session_id.startswith('session_'))
    
    def test_session_save_and_load(self):
        """Test session can be saved and loaded."""
        # Add some data
        self.session.add_turn("test input", {"status": "complete"})
        
        # Create new session with same ID
        session2 = Session(session_id=self.session.session_id, output_dir=self.test_dir)
        
        # Verify data was loaded
        self.assertEqual(len(session2.history), 1)
        self.assertEqual(session2.history[0]['user_input'], "test input")
    
    def test_session_history(self):
        """Test conversation history management."""
        self.session.add_turn("input 1", {"status": "ok"})
        self.session.add_turn("input 2", {"status": "ok"})
        self.session.add_turn("input 3", {"status": "ok"})
        
        # Get all history
        history = self.session.get_history()
        self.assertEqual(len(history), 3)
        
        # Get limited history
        history = self.session.get_history(limit=2)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['user_input'], "input 2")
    
    def test_session_summary(self):
        """Test session summary."""
        self.session.add_turn("test", {
            "evidence_ids": ["EVD-0001", "EVD-0002"],
            "decision_id": "DEC-0001"
        })
        
        summary = self.session.get_summary()
        
        self.assertEqual(summary['turn_count'], 1)
        self.assertEqual(summary['evidence_count'], 2)
        self.assertEqual(summary['decision_count'], 1)
    
    def test_list_sessions(self):
        """Test listing sessions."""
        # Create additional sessions (one already exists from setUp)
        self.session.save()
        session2 = Session(output_dir=self.test_dir)
        session2.save()
        
        sessions = Session.list_sessions(output_dir=self.test_dir)
        self.assertEqual(len(sessions), 2)
    
    def test_delete_session(self):
        """Test deleting a session."""
        session_id = self.session.session_id
        self.session.save()
        
        # Verify file exists
        session_file = Path(self.test_dir) / f"{session_id}.json"
        self.assertTrue(session_file.exists())
        
        # Delete session
        Session.delete_session(session_id, output_dir=self.test_dir)
        
        # Verify file is gone
        self.assertFalse(session_file.exists())


class TestFormatter(unittest.TestCase):
    """Test output formatting."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.formatter = Formatter(use_colors=True)
        self.plain_formatter = Formatter(use_colors=False)
    
    def test_colored_output(self):
        """Test colored output includes ANSI codes."""
        result = self.formatter.success("test")
        self.assertIn('\033[', result)  # Contains ANSI codes
        self.assertIn('test', result)
    
    def test_plain_output(self):
        """Test plain output has no ANSI codes."""
        result = self.plain_formatter.success("test")
        self.assertNotIn('\033[', result)  # No ANSI codes
        self.assertEqual(result, "test")
    
    def test_formatting_methods(self):
        """Test various formatting methods."""
        text = "test"
        
        # Should not raise exceptions
        self.formatter.bold(text)
        self.formatter.dim(text)
        self.formatter.italic(text)
        self.formatter.success(text)
        self.formatter.error(text)
        self.formatter.warning(text)
        self.formatter.info(text)
        self.formatter.header(text)
        self.formatter.section(text)
        self.formatter.list_item(text)
    
    def test_format_dict(self):
        """Test dictionary formatting."""
        data = {
            'key1': 'value1',
            'key2': ['item1', 'item2'],
            'key3': {'nested': 'value'}
        }
        
        result = self.formatter.format_dict(data)
        self.assertIn('key1', result)
        self.assertIn('value1', result)
        self.assertIn('item1', result)
        self.assertIn('nested', result)
    
    def test_format_table(self):
        """Test table formatting."""
        headers = ['Col1', 'Col2']
        rows = [['A', 'B'], ['C', 'D']]
        
        result = self.formatter.format_table(headers, rows)
        self.assertIn('Col1', result)
        self.assertIn('Col2', result)
        self.assertIn('A', result)
        self.assertIn('B', result)


class TestInteractiveREPL(unittest.TestCase):
    """Test interactive REPL initialization."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
        # Clean up any created session directories
        shutil.rmtree('.rjw-sessions', ignore_errors=True)
    
    def test_repl_initialization(self):
        """Test REPL can be initialized."""
        repl = InteractiveREPL(yolo_mode=False, trust_level='SUPERVISED')
        
        self.assertIsNotNone(repl.session)
        self.assertIsNotNone(repl.optimizer)
        self.assertIsNotNone(repl.governance)
        self.assertIsNotNone(repl.formatter)
        self.assertFalse(repl.running)
    
    def test_repl_with_yolo_mode(self):
        """Test REPL initialization with YOLO mode."""
        repl = InteractiveREPL(yolo_mode=True, trust_level='AUTONOMOUS')
        
        self.assertTrue(repl.governance.yolo_mode)
        self.assertEqual(repl.governance.trust_level.name, 'AUTONOMOUS')
    
    def test_repl_commands_registered(self):
        """Test REPL has all commands registered."""
        repl = InteractiveREPL()
        
        expected_commands = [
            '/help', '/status', '/history', '/clear',
            '/yolo', '/trust', '/exit', '/quit'
        ]
        
        for cmd in expected_commands:
            self.assertIn(cmd, repl.commands)


if __name__ == '__main__':
    unittest.main()
