"""Gold layer models - unified cross-source analytical models."""

from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from fund_lens_models.base import Base, TimestampMixin


class GoldContributor(Base, TimestampMixin):
    """Unified contributor entity across all sources."""

    __tablename__ = "gold_contributor"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Contributor identity (deduplicated)
    name: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    first_name: Mapped[str | None] = mapped_column(String(255))
    last_name: Mapped[str | None] = mapped_column(String(255))

    # Location
    city: Mapped[str | None] = mapped_column(String(255), index=True)
    state: Mapped[str | None] = mapped_column(String(2), index=True)
    zip: Mapped[str | None] = mapped_column(String(5))

    # Employment
    employer: Mapped[str | None] = mapped_column(String(500), index=True)
    occupation: Mapped[str | None] = mapped_column(String(255))

    # Type
    entity_type: Mapped[str | None] = mapped_column(String(20))  # INDIVIDUAL, COMMITTEE, ORG, etc.

    # Deduplication metadata
    match_confidence: Mapped[float | None] = mapped_column(
        Numeric(3, 2)
    )  # 0.0-1.0 confidence score

    def __repr__(self) -> str:
        return f"<GoldContributor(id={self.id}, name={self.name})>"


class GoldCandidate(Base, TimestampMixin):
    """Unified candidate entity across all sources."""

    __tablename__ = "gold_candidate"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Candidate identity
    name: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    office: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True
    )  # US_HOUSE, US_SENATE, STATE_HOUSE, STATE_SENATE, GOVERNOR, COUNTY_EXEC, etc.
    office_raw: Mapped[str | None] = mapped_column(
        String(200)
    )  # Original office name from source (e.g., "County Commissioner President")
    state: Mapped[str | None] = mapped_column(String(2), index=True)
    district: Mapped[str | None] = mapped_column(String(100))  # Supports state district names

    # Jurisdiction level - for easy filtering by level of government
    # FEDERAL (US House, US Senate, President), STATE (Governor, State Legislature, etc),
    # COUNTY (County Council, Sheriff, etc), CITY (Baltimore City offices)
    jurisdiction_level: Mapped[str | None] = mapped_column(String(20), index=True)

    # Office location for local candidates (where the office is, not candidate address)
    office_county: Mapped[str | None] = mapped_column(
        String(100), index=True
    )  # For COUNTY jurisdiction candidates only
    office_city: Mapped[str | None] = mapped_column(
        String(100), index=True
    )  # For CITY jurisdiction candidates only (e.g., Baltimore)

    # Political affiliation
    party: Mapped[str | None] = mapped_column(String(50), index=True)

    # Election history tracking
    # For FEC: from election_years field; For MD: from bronze election_year values
    first_election_year: Mapped[int | None] = mapped_column(
        Integer, index=True
    )  # Earliest year filed
    last_election_year: Mapped[int | None] = mapped_column(
        Integer, index=True
    )  # Most recent year filed

    # Status - is_active means currently filed for upcoming/current election cycle
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    # Source references (for tracking)
    fec_candidate_id: Mapped[str | None] = mapped_column(String(20), unique=True)
    state_candidate_id: Mapped[str | None] = mapped_column(String(64))  # SHA-256 content hash

    def __repr__(self) -> str:
        return f"<GoldCandidate(id={self.id}, name={self.name}, office={self.office})>"


class GoldCommittee(Base, TimestampMixin):
    """Unified committee entity across all sources."""

    __tablename__ = "gold_committee"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Committee identity (name can be NULL in rare cases)
    name: Mapped[str | None] = mapped_column(String(500), index=True)
    committee_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # CANDIDATE, PAC, PARTY, SUPER_PAC, etc.

    # Political affiliation (NEW)
    party: Mapped[str | None] = mapped_column(String(50), index=True)

    # Location
    state: Mapped[str | None] = mapped_column(String(2), index=True)
    city: Mapped[str | None] = mapped_column(String(255))

    # Affiliated candidate (if applicable)
    candidate_id: Mapped[int | None] = mapped_column(Integer, index=True)

    # Source references
    fec_committee_id: Mapped[str | None] = mapped_column(String(20), unique=True)
    state_committee_id: Mapped[str | None] = mapped_column(
        String(64)
    )  # SHA-256 content hash or state ID

    # Status
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<GoldCommittee(id={self.id}, name={self.name})>"


class GoldContribution(Base, TimestampMixin):
    """Unified contribution record across all sources."""

    __tablename__ = "gold_contribution"
    __table_args__ = (
        UniqueConstraint("source_system", "source_sub_id", name="uq_source_transaction"),
    )

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Source tracking
    source_system: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # FEC, MD_STATE, VA_STATE, etc.
    source_sub_id: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # Unique record ID (FEC sub_id)
    source_transaction_id: Mapped[str | None] = mapped_column(
        String(255), index=True
    )  # Links related records (e.g., earmark pairs) - nullable for API data without transaction_id

    # Contribution details
    contribution_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    # Relationships (foreign keys to gold entities)
    contributor_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    recipient_committee_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    recipient_candidate_id: Mapped[int | None] = mapped_column(Integer, index=True)

    # Earmark tracking - for contributions made via a conduit (ActBlue, WinRed, etc.)
    conduit_committee_id: Mapped[int | None] = mapped_column(Integer, index=True)
    is_earmark_receipt: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, index=True
    )  # True for 15E records that have a matching earmark - should be excluded from stats

    # Transaction classification
    contribution_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # DIRECT, EARMARKED, IN_KIND, etc.
    election_type: Mapped[str | None] = mapped_column(String(20))  # PRIMARY, GENERAL, SPECIAL, etc.

    # Election context
    election_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    election_cycle: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    # Additional context
    memo_text: Mapped[str | None] = mapped_column(Text)

    def __repr__(self) -> str:
        return (
            f"<GoldContribution(id={self.id}, amount={self.amount}, date={self.contribution_date})>"
        )
