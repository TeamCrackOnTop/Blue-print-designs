# Blueprint Designs Discord Bot

A Python `discord.py` starter bot for the Blueprint Designs server. It includes the setup dashboard shown in the supplied reference image, with buttons for general settings, categories, panels, XP, partnerships, economy, embeds, discounts, orders, custom commands, ranks, welcome messages, anti-raid, and applications.

## Commands

- `/setup` — opens the administrator-only setup dashboard.
- `/config <key> <value>` — saves `transcript_channel` or `log_channel` settings.
- `/ping` — checks bot latency.

The dashboard buttons currently provide safe placeholder panels. Features such as tickets, XP, economy, applications, and anti-raid can be implemented incrementally without exposing the bot token.

## Run locally

1. Install Python 3.10 or newer.
2. Create a Discord application and bot in the [Discord Developer Portal](https://discord.com/developers/applications).
3. Enable the **Server Members Intent** if you plan to use member events.
4. Invite the bot with the `bot` and `applications.commands` scopes and the permissions it needs.
5. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   # Windows: .venv\\Scripts\\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```

6. Copy `.env.example` to `.env` and add your token. Never commit `.env`.
7. Start the bot:

   ```bash
   python bot.py
   ```

Slash commands sync globally and may take a short time to appear in Discord. For development, guild-specific syncing can be added for instant updates.
