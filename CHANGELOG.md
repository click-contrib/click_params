# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2022-03-14

## Fixed

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
