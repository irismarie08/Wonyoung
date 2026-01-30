import discord
from discord import app_commands
from discord.ext import commands
import json
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree

DATA_FILE = "data/cards.json"

def load_cards():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_cards(cards):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=2)

@bot.event
async def on_ready():
    try:
        await tree.sync()
    except Exception as e:
        print(f"Error syncing commands: {e}")
    print(f"✅ Wonyoung is online as {bot.user}")

# /help
@tree.command(name="help", description="Show Wonyoung commands")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**Wonyoung Bot Commands** 💗\n"
        "/help\n"
        "/draw\n"
        "/addcard\n"
        "/inventory"
    )

# /draw
@tree.command(name="draw", description="Draw a random K-pop card")
async def draw(interaction: discord.Interaction):
    idols = ["Wonyoung", "Yujin", "Sakura", "Minju", "Yena"]
    idol = idols[hash(interaction.user.id) % len(idols)]

    cards = load_cards()
    cards.append({"user": interaction.user.id, "idol": idol})
    save_cards(cards)

    await interaction.response.send_message(f"🎴 You drew **{idol}**!")

# /addcard
@tree.command(name="addcard", description="Add a custom K-pop card")
@app_commands.describe(idol="Idol name")
async def addcard(interaction: discord.Interaction, idol: str):
    cards = load_cards()
    cards.append({"user": interaction.user.id, "idol": idol})
    save_cards(cards)

    await interaction.response.send_message(f"✅ Added card: **{idol}**")

# /inventory
@tree.command(name="inventory", description="View your cards")
async def inventory(interaction: discord.Interaction):
    cards = load_cards()
    user_cards = [c["idol"] for c in cards if c["user"] == interaction.user.id]

    if not user_cards:
        await interaction.response.send_message("You have no cards yet 💔")
        return

    await interaction.response.send_message(
        "🎴 **Your Cards:**\n" + ", ".join(user_cards)
    )

bot.run(TOKEN)

