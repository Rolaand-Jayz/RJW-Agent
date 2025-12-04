"""
Main CLI entry point for RJW-IDD Agent.

Provides command-line interface similar to Google Gemini, Claude, and other AI CLIs.
"""
import argparse
import sys
from pathlib import Path

from . import __version__
from .interactive import InteractiveREPL
from .session import Session
from .formatter import Formatter
from ..interaction.optimizer import PromptOptimizer
from ..governance.manager import GovernanceManager, TrustLevel


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='rjw',
        description='RJW-IDD Agent - Intelligence Driven Development CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  rjw                          # Start interactive session
  rjw chat                     # Start interactive session (alias)
  rjw --yolo                   # Start with YOLO mode enabled
  rjw --trust AUTONOMOUS       # Start with specific trust level
  rjw --session my_session     # Resume or create named session
  rjw sessions                 # List all sessions
  rjw sessions --delete old_id # Delete a session
  rjw run "Add authentication" # One-shot command
  rjw version                  # Show version

For more information, visit: https://github.com/Rolaand-Jayz/RJW-Agent
        """
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'rjw {__version__}'
    )
    
    parser.add_argument(
        '--provider',
        choices=['openai', 'gemini', 'vscode'],
        default=None,
        help='LLM provider to use (default: openai or RJW_PROVIDER env var)'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Chat command (default/interactive mode)
    chat_parser = subparsers.add_parser(
        'chat',
        help='Start interactive chat session (default)'
    )
    chat_parser.add_argument(
        '--session', '-s',
        help='Session ID to resume or create',
        default=None
    )
    chat_parser.add_argument(
        '--yolo',
        action='store_true',
        help='Enable YOLO mode (auto-approval)'
    )
    chat_parser.add_argument(
        '--trust',
        choices=['SUPERVISED', 'GUIDED', 'AUTONOMOUS', 'TRUSTED_PARTNER'],
        default='SUPERVISED',
        help='Trust level (default: SUPERVISED)'
    )
    chat_parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    # Run command (one-shot)
    run_parser = subparsers.add_parser(
        'run',
        help='Execute a single command'
    )
    run_parser.add_argument(
        'input',
        help='Command to execute'
    )
    run_parser.add_argument(
        '--yolo',
        action='store_true',
        help='Enable YOLO mode'
    )
    run_parser.add_argument(
        '--trust',
        choices=['SUPERVISED', 'GUIDED', 'AUTONOMOUS', 'TRUSTED_PARTNER'],
        default='SUPERVISED',
        help='Trust level'
    )
    run_parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    # Sessions command
    sessions_parser = subparsers.add_parser(
        'sessions',
        help='Manage sessions'
    )
    sessions_parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all sessions'
    )
    sessions_parser.add_argument(
        '--delete', '-d',
        metavar='SESSION_ID',
        help='Delete a session'
    )
    sessions_parser.add_argument(
        '--info', '-i',
        metavar='SESSION_ID',
        help='Show session information'
    )
    
    # Version command
    version_parser = subparsers.add_parser(
        'version',
        help='Show version information'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'version' or (not args.command and len(sys.argv) > 1 and sys.argv[1] == 'version'):
        print(f"RJW-IDD Agent CLI version {__version__}")
        print("Intelligence Driven Development - Disciplined AI-assisted development")
        return 0
    
    elif args.command == 'sessions':
        return handle_sessions(args)
    
    elif args.command == 'run':
        return handle_run(args)
    
    elif args.command == 'chat' or args.command is None:
        # Default to interactive mode
        return handle_chat(args)
    
    return 0


def handle_chat(args):
    """
    Handle interactive chat mode.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code
    """
    # Get arguments with defaults
    session_id = getattr(args, 'session', None)
    yolo_mode = getattr(args, 'yolo', False)
    trust_level = getattr(args, 'trust', 'SUPERVISED')
    no_color = getattr(args, 'no_color', False)
    provider = getattr(args, 'provider', None)
    
    # Create and start REPL
    repl = InteractiveREPL(
        session_id=session_id,
        yolo_mode=yolo_mode,
        trust_level=trust_level,
        provider=provider
    )
    
    # Disable colors if requested
    if no_color:
        repl.formatter.use_colors = False
    
    try:
        repl.start()
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_run(args):
    """
    Handle one-shot run command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code
    """
    formatter = Formatter(use_colors=not args.no_color)
    
    try:
        provider = getattr(args, 'provider', None)
        
        # Initialize components
        optimizer = PromptOptimizer(
            research_output_dir=".rjw-output/research",
            specs_output_dir=".rjw-output/specs",
            decisions_output_dir=".rjw-output/decisions",
            provider=provider
        )
        
        trust_level_enum = TrustLevel[args.trust]
        governance = GovernanceManager(
            yolo_mode=args.yolo,
            trust_level=trust_level_enum
        )
        
        # Process input
        print(formatter.dim("Processing..."))
        result = optimizer.process_user_input(args.input)
        
        # Request approval
        approval = governance.request_approval(
            action=f"Process: {args.input[:50]}...",
            phase='research',
            artifacts={'evidence_ids': result.get('evidence_ids', [])},
            risk_level='minimal'
        )
        
        # Display results
        print()
        print(formatter.success("✓ Complete"))
        print()
        
        if result.get('research_topics'):
            print(formatter.section("Topics:"))
            for topic in result['research_topics']:
                print(formatter.list_item(topic))
            print()
        
        if result.get('evidence_ids'):
            print(formatter.section("Evidence:"))
            for evd_id in result['evidence_ids']:
                print(formatter.list_item(evd_id))
            print()
        
        print(formatter.section("Governance:"))
        print(formatter.list_item(f"Approved: {approval['approved']}"))
        print(formatter.list_item(f"Mode: {approval['mode']}"))
        print()
        
        return 0
        
    except Exception as e:
        print(formatter.error(f"Error: {e}"), file=sys.stderr)
        return 1


def handle_sessions(args):
    """
    Handle session management commands.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code
    """
    formatter = Formatter()
    
    try:
        # Delete session
        if args.delete:
            Session.delete_session(args.delete)
            print(formatter.success(f"✓ Deleted session: {args.delete}"))
            return 0
        
        # Show session info
        if args.info:
            session = Session(session_id=args.info)
            summary = session.get_summary()
            
            print()
            print(formatter.header(f"Session: {args.info}"))
            print()
            print(formatter.format_dict(summary))
            print()
            return 0
        
        # List sessions (default)
        sessions = Session.list_sessions()
        
        if not sessions:
            print(formatter.info("No sessions found"))
            return 0
        
        print()
        print(formatter.header("Available Sessions"))
        print()
        
        for session_id in sessions:
            session = Session(session_id=session_id)
            summary = session.get_summary()
            
            print(formatter.bold(session_id))
            print(formatter.dim(f"  Created: {summary['created_at']}"))
            print(formatter.dim(f"  Turns: {summary['turn_count']}, Evidence: {summary['evidence_count']}"))
            print()
        
        return 0
        
    except Exception as e:
        print(formatter.error(f"Error: {e}"), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
