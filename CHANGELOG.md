# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-11-20

### Added
- Added `memo_code` field to `SilverFECContribution` to support earmark detection
- Added `source_sub_id` field to `GoldContribution` for unique record identification
- Added index on `source_transaction_id` in `GoldContribution` for efficient earmark pair queries

### Changed
- Updated `GoldContribution` unique constraint to use `source_sub_id` instead of `source_transaction_id`
- Enhanced `source_transaction_id` field documentation to clarify it links related records (earmark pairs)

### Fixed
- Corrected field usage: `source_sub_id` (unique ID) vs `source_transaction_id` (links pairs)

## [0.1.1] - 2025-11-03

### Changed
- Updated silver model to preserve bronze data that was previously lost
- Added `party` field to SilverFECCommittee model to track committee party affiliation
- Added `candidate_id` field to SilverFECCommittee model to track affiliated candidate from bronze data

## [0.1.0] - 2025-11-01

### Added
- Initial release with bronze, silver, and gold models
- Support for FEC campaign finance data
- Bronze layer: raw FEC Schedule A data
- Silver layer: normalized contributions and committees
- Gold layer: candidate, contributor, committee, and contribution analytics
