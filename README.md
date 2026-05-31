# YouTube Automation Upload & Scheduling Automation Engine

A robust Python-based backend automation pipeline that programmatically authenticates, batches, and schedules video content deployments via the **YouTube Data API v3**.

## Security & Deployment Architecture
For strict security compliance, this repository functions entirely as a **clean, production-ready template**. 

* **Credential Redaction:** The `client_secret.json` (Google Developer credentials) and `token.pickle` (authenticated session token) have been intentionally excluded from this public repository using a `.gitignore` configuration.
* **Access Control:** The backend OAuth consent architecture has been set back to private. To execute or test this pipeline, authorized users must provision their own client secrets via the Google Cloud Console or request specific access permissions from the me (developer).

## Key Features
* **Secure OAuth 2.0 Integration:** Utilizes credential caching (`token.pickle`) to establish persistent, secure programmatic handshakes with Google Cloud Console.
* **Automated Directory Parsing:** Dynamically scans user-defined local directories to batch-process `.mp4` media streams.
* **Algorithmic Calendar Scheduling:** Leverages mathematical floor division and modulo operators to cleanly distribute large backlogs of content across a structured daily release calendar (e.g., locking a maximum of 3 uploads per day at optimized time slots).
* **Object-Oriented Architecture:** Designed with highly reusable and decoupled `YouTubeVideo` and `AutomationEngine` class abstractions.

## Tech Stack
* Python 3
* Google API Client Libraries (`google-api-python-client`, `google-auth-oauthlib`)
* Object-Oriented Programming (OOP)
