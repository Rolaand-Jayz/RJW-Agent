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
