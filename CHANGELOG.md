# Changelog

All notable changes to this project will be documented in this file.

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
