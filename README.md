# RimAlertBot

RimAlertBot is a cloud-hosted Telegram bot built with Python and deployed on AWS EC2 (Ubuntu).  
It provides NBA scores, live game updates, team-specific schedules, and upcoming match information using the balldontlie API.

---

## Features

- `/start` – Displays bot information and available commands
- `/score` – Shows completed NBA games today
- `/score YYYY-MM-DD` – Shows completed games for a specific date
- `/live` – Displays currently live NBA games
- `/team <team_name>` – Shows next scheduled game for a specific team
- `/schedule` – Shows NBA schedule for the next 7 days
- Input validation and error handling
- Optimized API usage to reduce unnecessary requests

---

## Architecture

- Telegram User -> RimAlerBot (Python - async) -> balldontlie API -> Telegram Response.

---

## Cloud Deployment

- Hosted on AWS EC2 (Ubuntu 24.04)
- SSH key-based authentication
- Python virtual environment isolation
- Environment variables managed via `.env`
- Manual lifecycle management (start/stop/terminate EC2)

---

## Screenshots

### Bot Running on AWS EC2
![SSH Running](screenshots/your-ssh-screenshot-name.png)

### EC2 Instance Status
![EC2 Instance](screenshots/your-ec2-screenshot-name.png)

### Telegram Bot Features
![Start Command](screenshots/your-start-screenshot-name.png)
![Score Command](screenshots/your-score-screenshot-name.png)
![Team Command](screenshots/your-team-screenshot-name.png)
![Schedule Command](screenshots/your-schedule-screenshot-name.png)

---

## Technical Challenges Solved

- Refactored multi-request team lookup into a single optimized API call
- Implemented ISO date validation
- Handled async Telegram command architecture
- Managed EC2 lifecycle and persistence
- Secured API keys using environment variables

---

## Installation (Local)

```bash
git clone https://github.com/RDC4321/RimAlertBot.git
cd RimAlertBot
python -m venv venv
pip install -r requirements.txt
create .env file with BOT_TOKEN and BALLDONTLIE_API_KEY
python bot.py

