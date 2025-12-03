"""
Utility functions for the RJW-IDD agent framework.
"""
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class TemplateManager:
    """
    Manages template loading and artifact generation.
    
    This class is responsible for:
    - Loading templates from the rjw-idd-methodology/templates directory
    - Filling templates with provided data
    - Generating properly formatted artifact files (EVD, DEC, SPEC, etc.)
    """
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialize the TemplateManager.
        
        Args:
            templates_dir: Path to templates directory. If None, uses default location.
        """
        if templates_dir is None:
            # Default to rjw-idd-methodology/templates
            repo_root = Path(__file__).parent.parent
            templates_dir = repo_root / "rjw-idd-methodology" / "templates"
        
        self.templates_dir = Path(templates_dir)
        if not self.templates_dir.exists():
            raise ValueError(f"Templates directory not found: {self.templates_dir}")
    
    def load_template(self, template_type: str) -> str:
        """
        Load a template file.
        
        Args:
            template_type: Type of template (e.g., 'evidence', 'decision', 'spec')
            
        Returns:
            Template content as string
        """
        template_map = {
            'evidence': 'evidence/EVD-template.md',
            'decision': 'decisions/DEC-template.md',
            'spec': 'specs/SPEC-template.md',
            'requirement': 'requirements/REQ-template.md',
            'test': 'testing/TEST-template.md',
            'context': 'context/CTX-INDEX-template.md',
        }
        
        template_path = self.templates_dir / template_map.get(template_type, f"{template_type}-template.md")
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def generate_artifact_id(self, artifact_type: str, existing_ids: list = None) -> str:
        """
        Generate the next available artifact ID.
        
        Args:
            artifact_type: Type of artifact (EVD, DEC, SPEC, etc.)
            existing_ids: List of existing IDs to avoid collisions
            
        Returns:
            Next available ID (e.g., 'EVD-0001')
        """
        if existing_ids is None:
            existing_ids = []
        
        # Extract numbers from existing IDs
        numbers = []
        pattern = rf"{artifact_type}-(\d+)"
        for aid in existing_ids:
            match = re.match(pattern, aid)
            if match:
                numbers.append(int(match.group(1)))
        
        # Get next number
        next_num = max(numbers) + 1 if numbers else 1
        return f"{artifact_type}-{next_num:04d}"
    
    def fill_evidence_template(self, 
                               evidence_id: str,
                               title: str,
                               source_type: str,
                               source_url: str,
                               summary: str,
                               key_insights: list,
                               curator: str = "Agent",
                               **kwargs) -> str:
        """
        Fill the evidence template with data.
        
        Args:
            evidence_id: ID for the evidence (e.g., 'EVD-0001')
            title: Title of the evidence
            source_type: Type of source (Forum, GitHub, Publication, etc.)
            source_url: URL of the source
            summary: Brief summary of the evidence
            key_insights: List of key insights
            curator: Name/role of curator
            **kwargs: Additional fields to fill
            
        Returns:
            Filled template content
        """
        template = self.load_template('evidence')
        
        # Replace placeholders
        date = datetime.now().strftime('%Y-%m-%d')
        
        content = template.replace('# EVD-XXXX — Evidence Title', f'# {evidence_id} — {title}')
        content = content.replace('**Harvested:** YYYY-MM-DD', f'**Harvested:** {date}')
        content = content.replace('**Curator:** Role/Name', f'**Curator:** {curator}')
        content = content.replace('**Status:** Raw | Curated | Promoted | Archived', '**Status:** Curated')
        content = content.replace('- **Source Type:** Forum | GitHub | Publication | Interview | Survey | Analytics', 
                                  f'- **Source Type:** {source_type}')
        content = content.replace('- **Source URL:** Link to original source', f'- **Source URL:** {source_url}')
        content = content.replace('- **Source Date:** YYYY-MM-DD', f'- **Source Date:** {date}')
        
        # Replace summary
        content = re.sub(
            r'## Summary\n\nBrief description of the evidence and its key insights\.',
            f'## Summary\n\n{summary}',
            content
        )
        
        # Replace key insights
        insights_text = '\n'.join([f'{i+1}. {insight}' for i, insight in enumerate(key_insights)])
        content = re.sub(
            r'## Key Insights\n\n1\. First major insight or finding\.\n2\. Second major insight or finding\.\n3\. Third major insight or finding\.',
            f'## Key Insights\n\n{insights_text}',
            content
        )
        
        return content
    
    def save_artifact(self, content: str, output_path: str) -> str:
        """
        Save an artifact to disk.
        
        Args:
            content: Content to save
            output_path: Path where to save the file
            
        Returns:
            Absolute path to saved file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(output_path.absolute())


def get_artifact_id_from_filename(filename: str) -> Optional[str]:
    """
    Extract artifact ID from filename.
    
    Args:
        filename: Filename to parse
        
    Returns:
        Artifact ID if found, None otherwise
    """
    pattern = r'(EVD|DEC|SPEC|REQ|TEST|CTX)-\d{4}'
    match = re.search(pattern, filename)
    return match.group(0) if match else None
