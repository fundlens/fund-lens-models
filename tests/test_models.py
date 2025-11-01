"""Basic model import and instantiation tests."""
import datetime
from decimal import Decimal

import pytest
from fund_lens_models.gold import GoldCandidate, GoldContribution
from fund_lens_models.enums import USState, Office


def test_candidate_model():
    """Test Candidate model can be instantiated."""
    candidate = GoldCandidate(
        name="Test Candidate",
        office=Office.HOUSE,
        state=USState.MD,
        party="Democratic",
        is_active=True,
        fec_candidate_id="H6MD01234"
    )
    assert candidate.name == "Test Candidate"
    assert candidate.state == USState.MD


def test_contribution_model():
    """Test Contribution model can be instantiated."""
    contrib = GoldContribution(
        source_system="FEC",
        source_transaction_id="12345",
        contribution_date=datetime.date(2024, 1, 1),
        amount=Decimal(100.00),
        contributor_id=1,
        recipient_committee_id=1,
        contribution_type="IND",
        election_year=2024,
        election_cycle=2024
    )
    assert contrib.amount == 100.00
