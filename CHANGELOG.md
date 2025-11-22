# Changelog

All notable changes to this project will be documented in this file.

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
