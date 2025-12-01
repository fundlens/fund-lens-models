"""Silver layer models - cleaned and standardized Maryland data."""

from datetime import date

from sqlalchemy import Date, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from fund_lens_models.base import Base, TimestampMixin


class SilverMarylandContribution(Base, TimestampMixin):
    """Cleaned and standardized Maryland contribution data."""

    __tablename__ = "silver_md_contribution"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Source reference (content hash from bronze)
    source_content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    # Contribution details (cleaned)
    contribution_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    contribution_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    contribution_type: Mapped[str] = mapped_column(String(100), nullable=False)
    fund_type: Mapped[str | None] = mapped_column(String(100))

    # Contributor information (cleaned)
    contributor_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    contributor_type: Mapped[str] = mapped_column(String(100), nullable=False)

    # Parsed address fields (extracted from contributor_address)
    contributor_address: Mapped[str | None] = mapped_column(String(500))
    contributor_city: Mapped[str | None] = mapped_column(String(255), index=True)
    contributor_state: Mapped[str | None] = mapped_column(String(2), index=True)
    contributor_zip: Mapped[str | None] = mapped_column(String(10))

    # Employment info
    employer_name: Mapped[str | None] = mapped_column(String(255))
    employer_occupation: Mapped[str | None] = mapped_column(String(255))

    # Committee information (receiving committee)
    committee_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    committee_ccf_id: Mapped[str | None] = mapped_column(String(20), index=True)
    committee_type: Mapped[str | None] = mapped_column(String(100))

    # Filing info
    filing_period: Mapped[str] = mapped_column(String(100), nullable=False)
    office: Mapped[str | None] = mapped_column(String(255))

    def __repr__(self) -> str:
        return (
            f"<SilverMarylandContribution("
            f"id={self.id}, "
            f"amount={self.contribution_amount}, "
            f"date={self.contribution_date}"
            f")>"
        )


class SilverMarylandCommittee(Base, TimestampMixin):
    """Cleaned and standardized Maryland committee data."""

    __tablename__ = "silver_md_committee"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Source reference (CCF ID is unique in source)
    source_ccf_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)

    # Committee information
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    committee_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Election info
    election_type: Mapped[str | None] = mapped_column(String(255))

    # Registration dates (cleaned to proper dates)
    registered_date: Mapped[date | None] = mapped_column(Date)
    amended_date: Mapped[date | None] = mapped_column(Date)

    # Officers
    chairperson_name: Mapped[str | None] = mapped_column(String(255))
    treasurer_name: Mapped[str | None] = mapped_column(String(255))

    # Violations
    has_violations: Mapped[bool] = mapped_column(default=False, nullable=False)
    citation_violations: Mapped[str | None] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"<SilverMarylandCommittee(id={self.id}, name={self.name})>"


class SilverMarylandCandidate(Base, TimestampMixin):
    """Cleaned and standardized Maryland candidate data."""

    __tablename__ = "silver_md_candidate"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Source reference (content hash from bronze)
    source_content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    # Candidate information
    name: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    party: Mapped[str | None] = mapped_column(String(100), index=True)
    gender: Mapped[str | None] = mapped_column(String(50))

    # Office sought
    office: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    district: Mapped[str | None] = mapped_column(String(255))
    jurisdiction: Mapped[str | None] = mapped_column(String(255))

    # Status
    status: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Election info
    election_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    election_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Committee link (name-based, since MD doesn't have committee IDs in candidate data)
    committee_name: Mapped[str | None] = mapped_column(String(255), index=True)
    committee_ccf_id: Mapped[str | None] = mapped_column(String(20), index=True)

    # Contact info (cleaned)
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50))
    website: Mapped[str | None] = mapped_column(String(500))

    def __repr__(self) -> str:
        return (
            f"<SilverMarylandCandidate("
            f"id={self.id}, "
            f"name={self.name}, "
            f"office={self.office}"
            f")>"
        )
