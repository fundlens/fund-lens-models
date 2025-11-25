# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2025-11-25

### Added
- Added `conduit_committee_id` field to `GoldContribution` to track contributions made via conduits (ActBlue, WinRed, etc.)
- Added `is_earmark_receipt` boolean field to `GoldContribution` to mark 15E receipt records that should be excluded from contribution statistics
  - When `is_earmark_receipt=TRUE`, the record represents a receipt notification and should not be counted in totals
  - This prevents double-counting of earmarked contributions which appear twice in FEC data

### Notes
- Earmarked contributions in FEC data appear as two records:
  1. A 15E receipt record (type `15E`) when the committee receives notification
  2. The actual earmark record (transaction_id ending with `E`) representing the contribution
- The `is_earmark_receipt` flag allows filtering out the duplicate 15E records
- The `conduit_committee_id` field enables reporting on contributions by conduit/payment processor

## [0.2.4] - 2025-11-23

### Added
- Added `candidate_id` field to `BronzeFECScheduleA` for committee-to-candidate contributions (present in both API and pas2 bulk files)
- Added `image_number` field to `BronzeFECScheduleA` for FEC document/image reference (present in both API and bulk files)
- Added `other_id` field to `BronzeFECScheduleA` for other committee/candidate ID references (bulk files only)
- Added `is_individual` field to `BronzeFECScheduleA` to flag individual contributors (API: direct field, Bulk: derived from entity_type == 'IND')
- Added `line_number` field to `BronzeFECScheduleA` for FEC form line number (API only)
- Added `pdf_url` field to `BronzeFECScheduleA` for direct link to filing PDF (API only)
- Added `original_sub_id` field to `BronzeFECScheduleA` to track original submission ID for amendments (API only)

### Fixed
- Removed incorrect `transaction_type` field that was creating data inconsistency between API and bulk sources
  - Bulk files use `TRANSACTION_TP` column which maps to existing `receipt_type` field (same as API)
  - This ensures consistent field naming between API and bulk data sources

### Notes
- These additions enable complete data capture from both FEC API and bulk file sources
- Supports all three bulk contribution file types: indiv (individual→committee), pas2 (committee→candidate), oth (committee→committee)
- Fields are clearly documented as source-specific (API-only, bulk-only) or universal (both sources)

## [0.2.3] - 2025-11-22

### Changed
- Made `name` nullable in both `SilverFECCommittee` and `GoldCommittee` to handle rare cases where committee name is not provided in source data

## [0.2.2] - 2025-11-22

### Changed
- Made `entity_type` nullable in both `SilverFECContribution` and `GoldContributor` to handle records with missing entity type data
- Added validation in silver transformation to filter out records missing critical required fields (contribution_date, contribution_amount, contributor_name, committee_id)
  - Invalid records are now logged and filtered out rather than causing transformation failures

### Fixed
- Fixed NOT NULL constraint violations on `entity_type` field
- Fixed transformation failures from records with null values in critical fields by adding pre-insert validation

## [0.2.1] - 2025-11-22

### Changed
- Made `transaction_id` nullable in `SilverFECContribution` to support both API and bulk file sources
  - API-sourced records may not have `transaction_id` populated
  - Bulk file records reliably include `transaction_id`
- Made `source_transaction_id` nullable in `GoldContribution` to accept silver records without `transaction_id`
- Made `entity_type` nullable in both `SilverFECContribution` and `GoldContributor` to handle records with missing entity type data
- Added validation in silver transformation to filter out records missing critical required fields (contribution_date, contribution_amount, contributor_name, committee_id)
  - Invalid records are now logged and filtered out rather than causing transformation failures

### Fixed
- Fixed schema compatibility issue preventing transformation of API-sourced records that lack `transaction_id`
- Fixed NOT NULL constraint violations on `entity_type` field
- Fixed transformation failures from records with null values in critical fields by adding pre-insert validation

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
