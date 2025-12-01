"""Bronze layer models for Maryland campaign finance data."""

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from fund_lens_models.base import Base, SourceMetadataMixin, TimestampMixin


class BronzeMarylandContribution(Base, TimestampMixin, SourceMetadataMixin):
    """
    Raw Maryland contribution data from MDCRIS.

    Since Maryland contributions don't have a unique transaction ID,
    we use a content hash for deduplication.
    """

    __tablename__ = "bronze_md_contribution"

    # Surrogate primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Content hash for deduplication (no natural key in source)
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    # Raw fields from CSV (preserve exactly as received)
    receiving_committee: Mapped[str] = mapped_column(String(255), index=True)
    filing_period: Mapped[str] = mapped_column(String(100))
    contribution_date: Mapped[str] = mapped_column(String(20))  # Keep as string in bronze
    contributor_name: Mapped[str] = mapped_column(String(255))
    contributor_address: Mapped[str] = mapped_column(String(500))  # Unparsed address
    contributor_type: Mapped[str] = mapped_column(String(100))
    contribution_type: Mapped[str] = mapped_column(String(100))
    contribution_amount: Mapped[str] = mapped_column(String(50))  # Keep as string in bronze
    employer_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    employer_occupation: Mapped[str | None] = mapped_column(String(255), nullable=True)
    office: Mapped[str | None] = mapped_column(String(255), nullable=True)  # e.g., "Governor (SBE)"
    fund_type: Mapped[str | None] = mapped_column(String(100), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<BronzeMarylandContribution("
            f"id={self.id}, "
            f"committee={self.receiving_committee[:30]}..., "
            f"amount={self.contribution_amount}"
            f")>"
        )


class BronzeMarylandCommittee(Base, TimestampMixin, SourceMetadataMixin):
    """
    Raw Maryland committee data from MDCRIS.

    Committees have a unique CCF ID which serves as the primary key.
    """

    __tablename__ = "bronze_md_committee"

    # Surrogate primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Natural key from source
    ccf_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)

    # Raw fields from CSV
    committee_type: Mapped[str] = mapped_column(String(100))  # e.g., "Candidate Committee"
    committee_name: Mapped[str] = mapped_column(String(255), index=True)
    committee_status: Mapped[str] = mapped_column(String(50))  # e.g., "Active"
    citation_violations: Mapped[str | None] = mapped_column(Text, nullable=True)
    election_type: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )  # e.g., "Gubernatorial Presidential"
    registered_date: Mapped[str | None] = mapped_column(String(20), nullable=True)  # Keep as string
    amended_date: Mapped[str | None] = mapped_column(String(20), nullable=True)
    chairperson_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    chairperson_address: Mapped[str | None] = mapped_column(String(500), nullable=True)  # Unparsed
    treasurer_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    treasurer_address: Mapped[str | None] = mapped_column(String(500), nullable=True)  # Unparsed

    def __repr__(self) -> str:
        return (
            f"<BronzeMarylandCommittee("
            f"ccf_id={self.ccf_id}, "
            f"name={self.committee_name[:30]}..."
            f")>"
        )


class BronzeMarylandCandidate(Base, TimestampMixin, SourceMetadataMixin):
    """
    Raw Maryland candidate data from State Board of Elections.

    Candidates don't have a unique ID in the source, so we use a content hash.
    """

    __tablename__ = "bronze_md_candidate"

    # Surrogate primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Content hash for deduplication
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    # Raw fields from CSV
    office_name: Mapped[str] = mapped_column(String(255), index=True)
    district: Mapped[str | None] = mapped_column(String(255), nullable=True)
    candidate_last_name: Mapped[str] = mapped_column(String(255))
    candidate_first_name: Mapped[str] = mapped_column(String(255))
    additional_info: Mapped[str | None] = mapped_column(String(255), nullable=True)
    party: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    jurisdiction: Mapped[str | None] = mapped_column(String(255), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(100), index=True)  # e.g., "Active", "Withdrawn"
    filing_type_and_date: Mapped[str | None] = mapped_column(String(255), nullable=True)
    campaign_address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    campaign_city_state_zip: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    facebook: Mapped[str | None] = mapped_column(String(500), nullable=True)
    twitter: Mapped[str | None] = mapped_column(String(500), nullable=True)
    other_social: Mapped[str | None] = mapped_column(String(500), nullable=True)
    committee_name: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )  # Links to committee

    # Election metadata
    election_year: Mapped[int] = mapped_column(Integer, index=True)
    election_type: Mapped[str] = mapped_column(String(50), index=True)  # Primary, General, Special

    def __repr__(self) -> str:
        return (
            f"<BronzeMarylandCandidate("
            f"id={self.id}, "
            f"name={self.candidate_first_name} {self.candidate_last_name}, "
            f"office={self.office_name}"
            f")>"
        )


class BronzeMarylandExtractionState(Base, TimestampMixin):
    """
    Track extraction state for Maryland incremental loads.

    Unlike FEC which tracks per-committee, Maryland tracks at the
    data source level (contributions, committees, candidates).
    """

    __tablename__ = "bronze_md_extraction_state"

    # Composite primary key
    data_type: Mapped[str] = mapped_column(
        String(50), primary_key=True
    )  # 'contributions', 'committees', 'candidates'
    filing_year: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Last extraction info
    last_extraction_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    last_extraction_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # Extraction statistics
    total_records_extracted: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Date range that was extracted
    extraction_start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    extraction_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Status
    is_complete: Mapped[bool] = mapped_column(default=True, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<BronzeMarylandExtractionState("
            f"data_type={self.data_type}, "
            f"filing_year={self.filing_year}, "
            f"last_date={self.last_extraction_date}"
            f")>"
        )
