import json
import os
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DATA_FILE = Path("data/settings.json")
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

PREFIX = "!"
VALID_SETTINGS = {"transcript_channel", "log_channel"}


def load_settings() -> dict:
    if not DATA_FILE.exists():
        return {}
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_settings(settings: dict) -> None:
    DATA_FILE.write_text(json.dumps(settings, indent=2), encoding="utf-8")


settings = load_settings()


class BlueprintBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix=PREFIX, intents=intents, help_command=None)

    async def setup_hook(self) -> None:
        await self.tree.sync()

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} (ID: {self.user.id})")


bot = BlueprintBot()


class SetupView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=900)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message(
                "You need the **Manage Server** permission to use the setup dashboard.",
                ephemeral=True,
            )
            return False
        return True

    async def show_panel(self, interaction: discord.Interaction, title: str, description: str) -> None:
        embed = discord.Embed(title=title, description=description, color=discord.Color.blurple())
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="General Settings", style=discord.ButtonStyle.primary, row=0)
    async def general(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "General Settings", "Use `/config set <key> <value>` or `!config <key> <value>` to update a setting.")

    @discord.ui.button(label="Categories", style=discord.ButtonStyle.primary, row=0)
    async def categories(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "Categories", "Ticket-category configuration is ready to be added here.")

    @discord.ui.button(label="Panels", style=discord.ButtonStyle.primary, row=0)
    async def panels(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "Panels", "Create and manage ticket panels from this section.")

    @discord.ui.button(label="XP System", style=discord.ButtonStyle.primary, row=1)
    async def xp(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "XP System", "XP and level configuration will be managed here.")

    @discord.ui.button(label="Partnerships", style=discord.ButtonStyle.primary, row=1)
    async def partnerships(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "Partnerships", "Partnership settings will be managed here.")

    @discord.ui.button(label="Economy & Shop", style=discord.ButtonStyle.primary, row=2)
    async def economy(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "Economy & Shop", "Currency and shop settings will be managed here.")

    @discord.ui.button(label="Custom Embeds", style=discord.ButtonStyle.primary, row=2)
    async def embeds(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "Custom Embeds", "Build reusable embeds from this section.")

    @discord.ui.button(label="Discount Codes", style=discord.ButtonStyle.primary, row=3)
    async def discounts(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "Discount Codes", "Create and manage discount codes here.")

    @discord.ui.button(label="QC & Orders", style=discord.ButtonStyle.primary, row=3)
    async def orders(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "QC & Orders", "Order and quality-control settings will be managed here.")

    @discord.ui.button(label="Custom Commands", style=discord.ButtonStyle.primary, row=4)
    async def custom_commands(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "Custom Commands", "Custom command management will be managed here.")

    @discord.ui.button(label="Ranks & Promotions", style=discord.ButtonStyle.primary, row=4)
    async def ranks(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "Ranks & Promotions", "Configure ranks and promotion requirements here.")

    @discord.ui.button(label="Welcome Messages", style=discord.ButtonStyle.primary, row=4)
    async def welcome(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "Welcome Messages", "Configure welcome messages here.")

    @discord.ui.button(label="Anti-Raid", style=discord.ButtonStyle.primary, row=5)
    async def anti_raid(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "Anti-Raid", "Anti-raid controls will be managed here.")

    @discord.ui.button(label="Applications", style=discord.ButtonStyle.primary, row=5)
    async def applications(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self.show_panel(interaction, "Applications", "Application forms and review settings will be managed here.")

    @discord.ui.button(label="Refresh", style=discord.ButtonStyle.secondary, row=5)
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.edit_message(embed=dashboard_embed(interaction.guild), view=SetupView())


def dashboard_embed(guild: discord.Guild | None) -> discord.Embed:
    guild_settings = settings.get(str(guild.id), {}) if guild else {}
    transcript = guild_settings.get("transcript_channel", "Not configured")
    log_channel = guild_settings.get("log_channel", "Not configured")
    embed = discord.Embed(
        title="⚙️ Blueprint Designs Setup Dashboard",
        description="Configure the bot from this panel. Ticketing, XP, currency, and more can be added as features are enabled.",
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Status", value="**Configured:** Yes\n**Categories:** 0\n**Panels:** 0", inline=False)
    embed.add_field(name="Transcript channel", value=transcript, inline=True)
    embed.add_field(name="Log channel", value=log_channel, inline=True)
    embed.set_footer(text="Blueprint Designs")
    return embed


@bot.tree.command(name="setup", description="Open the Blueprint Designs bot setup dashboard")
@app_commands.checks.has_permissions(manage_guild=True)
async def setup(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(embed=dashboard_embed(interaction.guild), view=SetupView(), ephemeral=True)


@bot.tree.command(name="config", description="Set a Blueprint Designs bot configuration value")
@app_commands.describe(key="Setting name", value="Setting value")
@app_commands.choices(key=[
    app_commands.Choice(name="transcript_channel", value="transcript_channel"),
    app_commands.Choice(name="log_channel", value="log_channel"),
])
@app_commands.checks.has_permissions(manage_guild=True)
async def config(interaction: discord.Interaction, key: app_commands.Choice[str], value: str) -> None:
    guild_id = str(interaction.guild_id)
    settings.setdefault(guild_id, {})[key.value] = value
    save_settings(settings)
    await interaction.response.send_message(f"Saved `{key.value}` as `{value}`.", ephemeral=True)


@bot.tree.command(name="ping", description="Check whether the bot is online")
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"Pong! `{round(bot.latency * 1000)}ms`", ephemeral=True)


@bot.command(name="setup")
@commands.has_guild_permissions(manage_guild=True)
async def prefix_setup(ctx: commands.Context) -> None:
    await ctx.send(embed=dashboard_embed(ctx.guild), view=SetupView())


@bot.command(name="config")
@commands.has_guild_permissions(manage_guild=True)
async def prefix_config(ctx: commands.Context, key: str, *, value: str) -> None:
    key = key.lower()
    if key not in VALID_SETTINGS:
        await ctx.send(f"Invalid setting. Choose one of: {', '.join(sorted(VALID_SETTINGS))}", delete_after=10)
        return
    settings.setdefault(str(ctx.guild.id), {})[key] = value
    save_settings(settings)
    await ctx.send(f"Saved `{key}` as `{value}`.")


@bot.command(name="ping")
async def prefix_ping(ctx: commands.Context) -> None:
    await ctx.send(f"Pong! `{round(bot.latency * 1000)}ms`")


@bot.command(name="help")
async def prefix_help(ctx: commands.Context) -> None:
    await ctx.send(
        "**Blueprint Designs commands**\n"
        "`!setup` — open the setup dashboard (Manage Server required)\n"
        "`!config <transcript_channel|log_channel> <value>` — save a setting (Manage Server required)\n"
        "`!ping` — check bot latency\n\n"
        "The same commands are also available as slash commands: `/setup`, `/config`, and `/ping`."
    )


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need the **Manage Server** permission to use that command.", delete_after=10)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument `{error.param.name}`. Use `!help` for usage.", delete_after=10)
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("This command can only be used in a server.", delete_after=10)
    else:
        raise error


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
    message = "You do not have permission to use this command." if isinstance(error, app_commands.MissingPermissions) else "Something went wrong while running that command."
    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing. Copy .env.example to .env and add your bot token.")

bot.run(TOKEN)
