#🚨 Server Uptime Monitor

A lightweight, real-time website monitoring system that tracks the uptime of multiple URLs and sends instant email alerts when services go down or come back online.

##✨ Features

🔄 Real-time Monitoring: Continuously checks the status of configured URLs at customizable intervals

🛡️ Smart False-Positive Detection: Retries failed connections twice before confirming downtime

📧 Email Notifications: Instant Gmail alerts for both downtime and recovery events

💾 Persistent History: SQLite database tracks all status changes with timestamps

⚡ Latency Tracking: Monitors response times for working services

🔌 REST API: Adjust monitoring intervals on the fly via HTTP endpoint

🧵 Multi-threaded: Non-blocking Flask server runs alongside monitoring loop

##🛠️ Tech Stack

🐍 Python 3.x

🌐 Flask: REST API server

🗄️ SQLite: Local database for historical data

📮 SMTP: Gmail integration for alerts

🌍 Requests: HTTP client for URL checking

⚙️ Threading: Concurrent monitoring and API server

