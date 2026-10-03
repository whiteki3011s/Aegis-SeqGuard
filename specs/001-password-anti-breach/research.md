# Technical Research: AI Password Anti-Breaching System

## Research Decisions

### 1. AI Anomaly & Pattern Evaluation Algorithm
- **Decision**: Hybrid Statistical Pattern Analyzer + n-gram Trajectory Vector Classifier.
- **Rationale**: Real-time evaluation requires deterministic low latency (<50ms model scoring). Combining statistical Levenshtein/n-gram trajectory distance metrics across consecutive entry timestamps with a lightweight Isolation Forest / Logistic classifier provides sub-millisecond pattern scoring without external heavy model dependencies.
- **Alternatives Considered**:
  - Deep Learning Transformer Models: Rejected due to high inference latency (>100ms) and operational memory footprint.
  - Static RegEx Matching: Rejected due to inability to detect non-deterministic or fuzzy dictionary shift sequences across multiple accounts.

### 2. Anonymization & Zero-Plaintext Telemetry
- **Decision**: HMAC-SHA256 Tokenized Digest with Salted Trajectory Keys.
- **Rationale**: Complies strictly with Constitution Principle II. Plaintext passwords or raw usernames are never ingested by the AI pipeline. Entry telemetry receives double-salted HMAC hashes of account identifiers and character length/complexity bucket indicators.
- **Alternatives Considered**:
  - Reversible Encryption: Rejected because decryption keys in memory present a high-risk security breach vector.
  - Unsalted MD5/SHA1: Rejected due to vulnerability to rainbow table reversal.

### 3. Fail-Safe Backup & Lockout Orchestration
- **Decision**: Circuit Breaker Pattern with Parallel Hardcoded Sequence Rules.
- **Rationale**: Complies strictly with Constitution Principle III. If the AI model scoring pipeline exceeds a 50ms processing timeout or encounters an unhandled exception, a hardcoded rule engine (monitoring exact alphabetical and frequency bursts) assumes evaluation, defaulting to fail-closed/heightened challenge.
- **Alternatives Considered**:
  - Fail-Open Mode: Rejected due to security vulnerability during system overload attacks.

### 4. Audit Trail Persistence & Storage
- **Decision**: Structured JSON Audit Logs with SQLite / Local File Append.
- **Rationale**: Provides immutable append-only event recording for security analyst inspection without introducing complex external database dependencies for the MVP.
- **Alternatives Considered**:
  - Full relational DB cluster: Deferred to production deployment setup.
