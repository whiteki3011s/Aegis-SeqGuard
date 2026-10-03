# Tasks: AI Password Anti-Breaching System

**Feature Branch**: `001-password-anti-breach`

## Phase 1: Setup

- [x] **T-101**: Create Python project setup, requirements.txt (`pydantic`, `fastapi`, `uvicorn`, `pytest`, `numpy`, `httpx`), and project `.gitignore` file <!-- id: T-101 -->
- [x] **T-102**: Create package directory structure (`src/models`, `src/services`, `src/api`, `tests/unit`, `tests/integration`) <!-- id: T-102 -->

## Phase 2: Tests (TDD First)

- [x] **T-201**: Write unit tests for Telemetry Anonymizer (`tests/unit/test_anonymizer.py`) verifying HMAC hashing, zero-plaintext enforcement, and salt keying <!-- id: T-201 -->
- [x] **T-202**: Write unit tests for AI Anomaly Detector (`tests/unit/test_anomaly_detector.py`) verifying pattern score calculations for alphabetical and dictionary trajectory sequences <!-- id: T-202 -->
- [x] **T-203**: Write unit tests for Security Lockup Service (`tests/unit/test_lockup_service.py`) verifying threshold triggers, session isolation, and recovery status <!-- id: T-203 -->
- [x] **T-204**: Write integration tests for end-to-end Sequential Attack Simulation (`tests/integration/test_sequential_attack.py`) <!-- id: T-204 -->

## Phase 3: Core Implementation

- [x] **T-301**: Implement Data Models (`src/models/telemetry.py`, `src/models/trajectory.py`, `src/models/lockup.py`) using Pydantic schemas <!-- id: T-301 -->
- [x] **T-302**: Implement Anonymizer Service (`src/services/anonymizer.py`) for zero-knowledge HMAC entry digest generation <!-- id: T-302 -->
- [x] **T-303**: Implement AI Anomaly Detector (`src/services/anomaly_detector.py`) with trajectory n-gram distance analysis and deterministic backup rules <!-- id: T-303 -->
- [x] **T-304**: Implement Security Lockup Service (`src/services/lockup_service.py`) for active vector lockdown and recovery state tracking <!-- id: T-304 -->
- [x] **T-305**: Implement Audit Logger Service (`src/services/audit_logger.py`) for structured append-only JSON event logging <!-- id: T-305 -->

## Phase 4: Integration & API Server

- [x] **T-401**: Implement FastAPI ingestion & incident API endpoints (`src/api/routes.py`, `src/api/server.py`) <!-- id: T-401 -->
- [x] **T-402**: Implement main execution entrypoint (`src/main.py`) for starting the anti-breach service and CLI simulation <!-- id: T-402 -->

## Phase 5: Polish & Validation

- [x] **T-501**: Run full pytest test suite and verify 100% test pass rate for normal and attack scenarios <!-- id: T-501 -->
- [x] **T-502**: Validate performance latency (<500ms lockout response) and verify zero-plaintext compliance <!-- id: T-502 -->
