# FundLens Models

Shared SQLAlchemy models for FundLens ETL pipeline and API.

## Installation

```bash
# From Git (development)
poetry add git+https://github.com/youruser/fund-lens-models.git@v0.1.0

# From package registry (production)
poetry add fund-lens-models
```
## Usage

```python
from fund_lens_models.gold import Candidate, Contribution
from fund_lens_models.enums import USState
from fund_lens_models.database import get_session

# Query candidates
candidates = session.query(Candidate).filter(
  Candidate.state == USState.MD
).all()
```

## Development

Note: This package contains models only. Database migrations are managed
by the fund-lens-etl repository.
