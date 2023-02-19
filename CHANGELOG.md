# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.1] - 2023-02-19

### Fixed

- Fixed `ListParamType` to be able to parse the same input multiple times in a row (#23).

## [0.4.0] - 2022-08-13

### Added

- All `ListParamType` subclasses have a new parameter `ignore_empty` that defaults to False.

### Changed

- Renamed `UnionParamType` to `FirstOf` and changed its signature.

## [0.3.0] - 2022-03-14

### Fixed

- An issue when a user is prompted a value for a type inheriting `ListParamType`.

### Removed

- Support for python3.6

## [0.2.0] - 2022-03-04

### Added

- A new base type: `UnionParamType`.

## [0.1.2] - 2021-05-16

### Changed

- Updated code to be compatible with Click 8.X

## [0.1.1] - 2020-01-06

### Added
- Added usage of nox package for test automation.
- Added poetry package to better manage package dependencies

### Changed
- Changed .travis.yml and appveyor.yml to take in account nox.

### Removed
- Removed pipenv in favor of poetry.

## [0.1.0] - 2019-07-21

### Added
- First release of the package.
