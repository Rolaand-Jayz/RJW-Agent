"""
Interactive REPL for the RJW-IDD CLI.

Provides a conversational interface similar to Claude, Gemini, and other AI CLIs.
"""
import sys
import readline  # For command history and editing
from typing import Optional

from .session import Session
from .formatter import Formatter
from ..interaction.optimizer import PromptOptimizer
from ..governance.manager import GovernanceManager, TrustLevel


class InteractiveREPL:
    """
    Interactive Read-Eval-Print Loop for RJW-IDD Agent.
    
    Provides a conversational interface with:
    - Multi-turn conversations
    - Session management
    - Command history
    - Colored output
    - Special commands (help, status, etc.)
    """
    
    def __init__(self, 
                 session_id: Optional[str] = None,
                 yolo_mode: bool = False,
                 trust_level: str = "SUPERVISED"):
        """
        Initialize the interactive REPL.
        
        Args:
            session_id: Optional session ID to resume
            yolo_mode: Enable YOLO mode for auto-approval
            trust_level: Initial trust level
        """
        self.session = Session(session_id)
        self.formatter = Formatter()
        
        # Initialize RJW-IDD components
        self.optimizer = PromptOptimizer(
            research_output_dir=f".rjw-sessions/{self.session.session_id}/research",
            specs_output_dir=f".rjw-sessions/{self.session.session_id}/specs",
            decisions_output_dir=f".rjw-sessions/{self.session.session_id}/decisions"
        )
        
        trust_level_enum = TrustLevel[trust_level]
        self.governance = GovernanceManager(
            yolo_mode=yolo_mode,
            trust_level=trust_level_enum
        )
        
        # Update session context
        self.session.update_context('yolo_mode', yolo_mode)
        self.session.update_context('trust_level', trust_level)
        
        self.running = False
        
        # Special commands
        self.commands = {
            '/help': self._cmd_help,
            '/status': self._cmd_status,
            '/history': self._cmd_history,
            '/clear': self._cmd_clear,
            '/yolo': self._cmd_yolo,
            '/trust': self._cmd_trust,
            '/exit': self._cmd_exit,
            '/quit': self._cmd_exit,
        }
    
    def start(self):
        """Start the interactive REPL."""
        self.running = True
        
        # Print welcome message
        self._print_welcome()
        
        # Main loop
        while self.running:
            try:
                # Get user input
                user_input = input(self.formatter.prompt()).strip()
                
                if not user_input:
                    continue
                
                # Check for special commands
                if user_input.startswith('/'):
                    self._handle_command(user_input)
                else:
                    # Process as normal input
                    self._process_input(user_input)
                    
            except KeyboardInterrupt:
                print("\n")
                if self._confirm_exit():
                    break
            except EOFError:
                print("\n")
                break
        
        self._print_goodbye()
    
    def _print_welcome(self):
        """Print welcome message."""
        summary = self.session.get_summary()
        
        print(self.formatter.header("RJW-IDD Agent CLI"))
        print(self.formatter.info(f"Session: {self.session.session_id}"))
        
        if summary['turn_count'] > 0:
            print(self.formatter.info(f"Resuming session with {summary['turn_count']} previous turns"))
        
        print(self.formatter.info(f"Trust Level: {summary['trust_level']}"))
        print(self.formatter.info(f"YOLO Mode: {'Enabled' if summary['yolo_mode'] else 'Disabled'}"))
        print()
        print(self.formatter.dim("Type /help for available commands"))
        print(self.formatter.dim("Type /exit or press Ctrl+D to quit"))
        print()
    
    def _print_goodbye(self):
        """Print goodbye message."""
        summary = self.session.get_summary()
        
        print()
        print(self.formatter.success("✓ Session saved"))
        print(self.formatter.info(f"  Total turns: {summary['turn_count']}"))
        print(self.formatter.info(f"  Evidence: {summary['evidence_count']}"))
        print(self.formatter.info(f"  Decisions: {summary['decision_count']}"))
        print(self.formatter.info(f"  Specs: {summary['spec_count']}"))
        print()
        print(self.formatter.header("Thank you for using RJW-IDD Agent!"))
    
    def _handle_command(self, command: str):
        """
        Handle special commands.
        
        Args:
            command: Command string starting with /
        """
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd in self.commands:
            self.commands[cmd](args)
        else:
            print(self.formatter.error(f"Unknown command: {cmd}"))
            print(self.formatter.dim("Type /help for available commands"))
    
    def _process_input(self, user_input: str):
        """
        Process user input through the RJW-IDD workflow.
        
        Args:
            user_input: User's input text
        """
        try:
            # Show processing indicator
            print(self.formatter.dim("\n🔍 Processing your request..."))
            
            # Process through PromptOptimizer
            result = self.optimizer.process_user_input(user_input)
            
            # Request governance approval
            approval = self.governance.request_approval(
                action=f"Process: {user_input[:50]}...",
                phase='research',
                artifacts={'evidence_ids': result.get('evidence_ids', [])},
                risk_level='minimal'
            )
            
            # Display results
            print()
            print(self.formatter.success("✓ Research Complete"))
            print()
            
            if result.get('research_topics'):
                print(self.formatter.section("Research Topics:"))
                for topic in result['research_topics']:
                    print(self.formatter.list_item(topic))
                print()
            
            if result.get('evidence_ids'):
                print(self.formatter.section("Evidence Generated:"))
                for evd_id in result['evidence_ids']:
                    print(self.formatter.list_item(evd_id))
                print()
            
            print(self.formatter.section("Governance:"))
            print(self.formatter.list_item(f"Status: {self.formatter.bold('Approved' if approval['approved'] else 'Rejected')}"))
            print(self.formatter.list_item(f"Mode: {approval['mode']}"))
            if approval.get('reason'):
                print(self.formatter.list_item(f"Reason: {approval['reason']}"))
            print()
            
            if result.get('next_steps'):
                print(self.formatter.section("Next Steps:"))
                for step in result['next_steps']:
                    print(self.formatter.list_item(step))
                print()
            
            # Save to session
            self.session.add_turn(user_input, result)
            
        except Exception as e:
            print(self.formatter.error(f"Error: {str(e)}"))
    
    def _cmd_help(self, args: str):
        """Display help information."""
        print()
        print(self.formatter.header("Available Commands"))
        print()
        print(self.formatter.bold("/help") + "       - Show this help message")
        print(self.formatter.bold("/status") + "     - Show current session status")
        print(self.formatter.bold("/history") + "    - Show conversation history")
        print(self.formatter.bold("/clear") + "      - Clear conversation history")
        print(self.formatter.bold("/yolo") + "       - Toggle YOLO mode")
        print(self.formatter.bold("/trust") + " <level> - Set trust level (SUPERVISED, GUIDED, AUTONOMOUS, TRUSTED_PARTNER)")
        print(self.formatter.bold("/exit") + "       - Exit the CLI (also /quit or Ctrl+D)")
        print()
        print(self.formatter.section("About RJW-IDD:"))
        print("  Intelligence Driven Development - A disciplined methodology for")
        print("  AI-assisted software development with research-driven decisions.")
        print()
    
    def _cmd_status(self, args: str):
        """Display session status."""
        summary = self.session.get_summary()
        governance = self.governance.get_governance_status()
        
        print()
        print(self.formatter.header("Session Status"))
        print()
        print(self.formatter.section("Session Info:"))
        print(self.formatter.list_item(f"ID: {summary['session_id']}"))
        print(self.formatter.list_item(f"Turns: {summary['turn_count']}"))
        print(self.formatter.list_item(f"Created: {summary['created_at']}"))
        print()
        print(self.formatter.section("Artifacts:"))
        print(self.formatter.list_item(f"Evidence: {summary['evidence_count']}"))
        print(self.formatter.list_item(f"Decisions: {summary['decision_count']}"))
        print(self.formatter.list_item(f"Specifications: {summary['spec_count']}"))
        print()
        print(self.formatter.section("Governance:"))
        print(self.formatter.list_item(f"Trust Level: {governance['trust_level']}"))
        print(self.formatter.list_item(f"YOLO Mode: {'Enabled' if governance['yolo_mode'] else 'Disabled'}"))
        print(self.formatter.list_item(f"Approvals: {governance['approval_count']}"))
        print()
    
    def _cmd_history(self, args: str):
        """Display conversation history."""
        limit = 10
        if args:
            try:
                limit = int(args)
            except ValueError:
                print(self.formatter.error("Invalid limit. Using default (10)."))
        
        history = self.session.get_history(limit)
        
        print()
        print(self.formatter.header(f"Last {len(history)} Turns"))
        print()
        
        for i, turn in enumerate(history, 1):
            print(self.formatter.bold(f"Turn {i}") + f" ({turn['timestamp']})")
            print(self.formatter.dim("User:") + f" {turn['user_input'][:80]}...")
            
            response = turn.get('agent_response', {})
            if response.get('status'):
                print(self.formatter.dim("Status:") + f" {response['status']}")
            
            print()
    
    def _cmd_clear(self, args: str):
        """Clear conversation history."""
        if self._confirm("Clear all conversation history?"):
            self.session.clear_history()
            print(self.formatter.success("✓ History cleared"))
        else:
            print(self.formatter.info("Cancelled"))
    
    def _cmd_yolo(self, args: str):
        """Toggle YOLO mode."""
        current = self.governance.yolo_mode
        new_mode = not current
        
        self.governance.set_yolo_mode(new_mode)
        self.session.update_context('yolo_mode', new_mode)
        
        status = "enabled" if new_mode else "disabled"
        print(self.formatter.success(f"✓ YOLO mode {status}"))
    
    def _cmd_trust(self, args: str):
        """Set trust level."""
        if not args:
            print(self.formatter.error("Usage: /trust <level>"))
            print(self.formatter.dim("Levels: SUPERVISED, GUIDED, AUTONOMOUS, TRUSTED_PARTNER"))
            return
        
        try:
            level = TrustLevel[args.upper()]
            self.governance.set_trust_level(level)
            self.session.update_context('trust_level', args.upper())
            print(self.formatter.success(f"✓ Trust level set to {args.upper()}"))
        except KeyError:
            print(self.formatter.error(f"Invalid trust level: {args}"))
            print(self.formatter.dim("Valid levels: SUPERVISED, GUIDED, AUTONOMOUS, TRUSTED_PARTNER"))
    
    def _cmd_exit(self, args: str):
        """Exit the REPL."""
        self.running = False
    
    def _confirm(self, message: str) -> bool:
        """
        Ask for user confirmation.
        
        Args:
            message: Confirmation message
            
        Returns:
            True if user confirms
        """
        response = input(f"{message} (y/N): ").strip().lower()
        return response in ['y', 'yes']
    
    def _confirm_exit(self) -> bool:
        """Confirm exit."""
        return self._confirm("\nExit?")
