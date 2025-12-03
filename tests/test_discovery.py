"""Tests for the Discovery & Research module."""
import pytest
import tempfile
import shutil
from pathlib import Path
from src.discovery.research import ResearchHarvester


class TestResearchHarvester:
    """Test suite for ResearchHarvester class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for tests."""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
    
    @pytest.fixture
    def harvester(self, temp_dir):
        """Create a ResearchHarvester instance."""
        return ResearchHarvester(output_dir=temp_dir)
    
    def test_harvest_creates_evidence_file(self, harvester, temp_dir):
        """Test that harvest creates an evidence file."""
        evd_id = harvester.harvest(
            topic="secure authentication",
            source_type="Research",
            curator="TestAgent"
        )
        
        # Check that evidence ID is returned
        assert evd_id.startswith("EVD-")
        
        # Check that file was created
        evd_file = Path(temp_dir) / f"{evd_id}.md"
        assert evd_file.exists()
        
        # Check that evidence is registered
        assert evd_id in harvester.evidence_registry
    
    def test_harvest_increments_id(self, harvester):
        """Test that harvest generates sequential IDs."""
        evd_id1 = harvester.harvest(topic="topic1")
        evd_id2 = harvester.harvest(topic="topic2")
        
        assert evd_id1 == "EVD-0001"
        assert evd_id2 == "EVD-0002"
    
    def test_harvest_empty_topic_raises_error(self, harvester):
        """Test that empty topic raises ValueError."""
        with pytest.raises(ValueError, match="Topic cannot be empty"):
            harvester.harvest(topic="")
    
    def test_validate_evidence_exists(self, harvester):
        """Test evidence validation."""
        evd_id = harvester.harvest(topic="test topic")
        
        # Valid evidence
        assert harvester.validate_evidence_exists(evd_id) is True
        
        # Invalid evidence
        assert harvester.validate_evidence_exists("EVD-9999") is False
    
    def test_require_evidence_for_artifact_valid(self, harvester):
        """Test that valid evidence references are accepted."""
        evd_id = harvester.harvest(topic="test topic")
        
        # Should not raise
        result = harvester.require_evidence_for_artifact("DEC", [evd_id])
        assert result is True
    
    def test_require_evidence_for_artifact_invalid(self, harvester):
        """Test that invalid evidence references are rejected."""
        with pytest.raises(ValueError, match="Invalid evidence references"):
            harvester.require_evidence_for_artifact("DEC", ["EVD-9999"])
    
    def test_require_evidence_for_artifact_missing(self, harvester):
        """Test that missing evidence references are rejected."""
        with pytest.raises(ValueError, match="Cannot create DEC without evidence references"):
            harvester.require_evidence_for_artifact("DEC", [])
    
    def test_list_evidence(self, harvester):
        """Test listing evidence."""
        evd_id1 = harvester.harvest(topic="authentication")
        evd_id2 = harvester.harvest(topic="authorization")
        
        all_evidence = harvester.list_evidence()
        assert len(all_evidence) == 2
        assert evd_id1 in all_evidence
        assert evd_id2 in all_evidence
        
        # Test filtering
        filtered = harvester.list_evidence(topic_filter="auth")
        assert len(filtered) == 2
    
    def test_get_evidence(self, harvester):
        """Test retrieving evidence by ID."""
        evd_id = harvester.harvest(topic="test topic")
        
        evidence = harvester.get_evidence(evd_id)
        assert evidence is not None
        assert evidence['topic'] == "test topic"
        
        # Non-existent evidence
        assert harvester.get_evidence("EVD-9999") is None
    
    def test_require_evidence_user_requirement_exception(self, harvester):
        """Test that user requirements don't require evidence."""
        # User requirements should NOT require evidence
        result = harvester.require_evidence_for_artifact(
            "REQ", 
            [],  # No evidence refs
            is_user_requirement=True
        )
        assert result is True
    
    def test_require_evidence_non_user_requirement_still_required(self, harvester):
        """Test that non-user requirements still require evidence."""
        # Non-user requirements should still require evidence
        with pytest.raises(ValueError, match="Cannot create REQ without evidence"):
            harvester.require_evidence_for_artifact(
                "REQ",
                [],  # No evidence refs
                is_user_requirement=False
            )


class TestUserEvidenceParser:
    """Test suite for UserEvidenceParser class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for tests."""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
    
    @pytest.fixture
    def parser(self):
        """Create a UserEvidenceParser instance."""
        from src.discovery.research import UserEvidenceParser
        return UserEvidenceParser()
    
    def test_parse_plain_text(self, parser):
        """Test parsing plain text research."""
        raw_input = """
        This is user-provided research about authentication methods.
        JWT tokens are widely used for stateless authentication.
        OAuth 2.0 provides authorization framework.
        """
        
        parsed = parser.parse_user_research(raw_input)
        assert parsed is not None
        assert 'title' in parsed
        assert 'summary' in parsed
        assert 'key_insights' in parsed
        assert 'raw_content' in parsed
        assert parsed['raw_content'] == raw_input
    
    def test_parse_markdown_format(self, parser):
        """Test parsing markdown formatted research."""
        raw_input = """
# Authentication Research

## Summary
Research on modern authentication patterns.

## Key Findings
- JWT tokens are stateless
- OAuth 2.0 is industry standard
- Multi-factor authentication improves security

## Conclusions
Modern apps should use OAuth 2.0 with JWT.
        """
        
        parsed = parser.parse_user_research(raw_input)
        assert 'Authentication Research' in parsed['title']
        assert len(parsed['key_insights']) > 0
        assert 'JWT' in str(parsed['key_insights'])
    
    def test_parse_bullet_points(self, parser):
        """Test parsing bullet point lists."""
        raw_input = """
User Research Findings:
* First important finding about the system
* Second critical insight for implementation
* Third observation from user feedback
        """
        
        parsed = parser.parse_user_research(raw_input)
        assert len(parsed['key_insights']) >= 3
    
    def test_parse_with_urls(self, parser):
        """Test extracting URLs from research."""
        raw_input = """
Research from https://example.com/auth shows that JWT is preferred.
See also: https://oauth.net/2/ for OAuth details.
        """
        
        parsed = parser.parse_user_research(raw_input)
        assert len(parsed['sources']) > 0
        assert any('https://example.com/auth' in str(s) for s in parsed['sources'])
    
    def test_parse_empty_input_raises_error(self, parser):
        """Test that empty input raises error."""
        with pytest.raises(ValueError, match="User research input cannot be empty"):
            parser.parse_user_research("")
    
    def test_reformat_to_evidence_standard_priority(self, parser):
        """Test reformatting to EVD template with standard priority."""
        parsed_data = {
            'title': 'Test Research',
            'summary': 'Test summary',
            'key_insights': ['Insight 1', 'Insight 2'],
            'sources': [{'type': 'URL', 'reference': 'https://example.com'}],
            'methodology': 'User observation',
            'conclusions': 'Test conclusions',
            'raw_content': 'Original content',
            'parsed_date': '2024-01-01'
        }
        
        evd_content = parser.reformat_to_evidence(parsed_data, user_priority=False)
        
        assert 'EVD-####' in evd_content
        assert 'Test Research' in evd_content
        assert 'User-Provided' in evd_content
        assert 'Standard (equal weight to agent research)' in evd_content
        assert 'Original content' in evd_content
    
    def test_reformat_to_evidence_elevated_priority(self, parser):
        """Test reformatting with explicit user priority."""
        parsed_data = {
            'title': 'Priority Research',
            'summary': 'Important findings',
            'key_insights': ['Critical insight'],
            'sources': [],
            'methodology': '',
            'conclusions': '',
            'raw_content': 'Priority content',
            'parsed_date': '2024-01-01'
        }
        
        evd_content = parser.reformat_to_evidence(parsed_data, user_priority=True)
        
        assert 'elevated priority' in evd_content.lower() or 'Elevated' in evd_content
        assert 'Priority content' in evd_content
    
    def test_harvest_user_research(self, temp_dir):
        """Test end-to-end user research harvesting."""
        from src.discovery.research import ResearchHarvester
        
        harvester = ResearchHarvester(output_dir=temp_dir)
        
        user_research = """
# Performance Optimization Research

Key findings from load testing:
- System handles 1000 req/sec
- Database is the bottleneck
- Caching reduces load by 60%
        """
        
        evd_id = harvester.harvest_user_research(user_research, user_priority=False)
        
        assert evd_id.startswith("EVD-")
        assert evd_id in harvester.evidence_registry
        assert harvester.evidence_registry[evd_id]['user_provided'] is True
        assert harvester.evidence_registry[evd_id]['user_priority'] is False
    
    def test_harvest_user_research_with_priority(self, temp_dir):
        """Test user research with explicit priority."""
        from src.discovery.research import ResearchHarvester
        
        harvester = ResearchHarvester(output_dir=temp_dir)
        
        evd_id = harvester.harvest_user_research(
            "Critical security finding from audit",
            user_priority=True,
            curator="Security Team"
        )
        
        assert harvester.evidence_registry[evd_id]['user_priority'] is True
        assert harvester.evidence_registry[evd_id]['curator'] == "Security Team"
