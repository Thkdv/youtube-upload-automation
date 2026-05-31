# YouTube Automation Upload & Scheduling Automation Engine

A robust Python-based backend automation pipeline that programmatically authenticates, batches, and schedules video content deployments via the **YouTube Data API v3**.

## Key Features
* **Secure OAuth 2.0 Integration:** Utilizes credential caching (`token.pickle`) to establish persistent, secure programmatic handshakes with Google Cloud Console.
* **Automated Directory Parsing:** Dynamically scans user-defined local directories to batch-process `.mp4` media streams.
* **Algorithmic Calendar Scheduling:** Leverages mathematical floor division and modulo operators to cleanly distribute large backlogs of content across a structured daily release calendar (e.g., locking a maximum of 3 uploads per day at optimized time slots).
* **Object-Oriented Architecture:** Designed with highly reusable and decoupled `YouTubeVideo` and `AutomationEngine` class abstractions.

## Tech Stack
* Python 3
* Google API Client Libraries (`google-api-python-client`, `google-auth-oauthlib`)
* Object-Oriented Programming (OOP)