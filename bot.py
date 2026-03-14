import os
import json
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

# =========================
# LOAD TOKEN FROM .env FILE
# =========================
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# =========================
# CONFIG
# =========================
PREFIX = "?"
CARDS_FILE = "cards.json"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)


# =========================
# FILE HELPERS
# =========================
def load_cards() -> dict:
    path = Path(CARDS_FILE)

    if not path.exists():
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cards(cards: dict) -> None:
    with open(CARDS_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=4, ensure_ascii=False)


def format_price(value) -> str:
    if value is None or value == "":
        return "Not set"

    try:
        number = float(str(value).replace("£", "").strip())
        return f"£{number:.2f}"
    except ValueError:
        return str(value)


# =========================
# EVENTS
# =========================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready.")


# =========================
# COMMANDS
# =========================
@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.reply(f"Pong! `{round(bot.latency * 1000)}ms`", mention_author=False)


@bot.command(name="addcard")
async def addcard(ctx: commands.Context, *, args: str):
    """
    Usage:
    ?addcard code | Card Name | Image URL | eBay Sold Link | Buy Price | Notes

    Buy Price and Notes are optional.
    """
    parts = [part.strip() for part in args.split("|")]

    if len(parts) < 4 or len(parts) > 6:
        await ctx.reply(
            "Use this format:\n"
            "`?addcard code | Card Name | Image URL | eBay Sold Link | Buy Price | Notes`\n"
            "Only the first 4 parts are required. Buy Price and Notes are optional.",
            mention_author=False
        )
        return

    code = parts[0].lower()
    name = parts[1]
    image_url = parts[2]
    ebay_link = parts[3]
    buy_price = parts[4] if len(parts) >= 5 else ""
    notes = parts[5] if len(parts) >= 6 else ""

    cards = load_cards()

    cards[code] = {
        "name": name,
        "image_url": image_url,
        "ebay_link": ebay_link,
        "buy_price": buy_price,
        "notes": notes
    }

    save_cards(cards)

    embed = discord.Embed(
        title="Card saved",
        description=f"Saved comp entry for **{name}**",
    )
    embed.add_field(name="Code", value=code, inline=True)
    embed.add_field(name="Paid", value=format_price(buy_price), inline=True)

    if notes:
        embed.add_field(name="Notes", value=notes[:1024], inline=False)

    if image_url:
        embed.set_image(url=image_url)

    await ctx.reply(embed=embed, mention_author=False)


@bot.command(name="comp")
async def comp(ctx: commands.Context, *, code: str):
    """
    Usage:
    ?comp charizard199
    """
    code = code.strip().lower()
    cards = load_cards()

    if code not in cards:
        await ctx.reply(
            f"No saved card found for code: **{code}**",
            mention_author=False
        )
        return

    card = cards[code]

    name = card.get("name", "Unknown card")
    image_url = card.get("image_url", "")
    ebay_link = card.get("ebay_link", "")
    buy_price = card.get("buy_price", "")
    notes = card.get("notes", "")

    embed = discord.Embed(
        title=name,
        url=ebay_link
    )

    embed.add_field(name="Code", value=code, inline=True)
    embed.add_field(name="Paid", value=format_price(buy_price), inline=True)

    if notes:
        embed.add_field(name="Notes", value=notes[:1024], inline=False)

    if image_url:
        embed.set_image(url=image_url)

    await ctx.reply(embed=embed, mention_author=False)


@bot.command(name="setprice")
async def setprice(ctx: commands.Context, *, args: str):
    """
    Usage:
    ?setprice charizard199 | 12.50
    """
    parts = [part.strip() for part in args.split("|")]

    if len(parts) != 2:
        await ctx.reply(
            "Use this format:\n`?setprice code | price`",
            mention_author=False
        )
        return

    code = parts[0].lower()
    price = parts[1]

    cards = load_cards()

    if code not in cards:
        await ctx.reply(
            f"No saved card found for code: **{code}**",
            mention_author=False
        )
        return

    cards[code]["buy_price"] = price
    save_cards(cards)

    await ctx.reply(
        f"Updated **{cards[code]['name']}** (`{code}`) paid price to **{format_price(price)}**",
        mention_author=False
    )


@bot.command(name="setnotes")
async def setnotes(ctx: commands.Context, *, args: str):
    """
    Usage:
    ?setnotes charizard199 | Mint raw copy from bundle
    """
    parts = [part.strip() for part in args.split("|", 1)]

    if len(parts) != 2:
        await ctx.reply(
            "Use this format:\n`?setnotes code | your notes here`",
            mention_author=False
        )
        return

    code = parts[0].lower()
    notes = parts[1]

    cards = load_cards()

    if code not in cards:
        await ctx.reply(
            f"No saved card found for code: **{code}**",
            mention_author=False
        )
        return

    cards[code]["notes"] = notes
    save_cards(cards)

    await ctx.reply(
        f"Updated notes for **{cards[code]['name']}** (`{code}`)",
        mention_author=False
    )


@bot.command(name="editcard")
async def editcard(ctx: commands.Context, *, args: str):
    """
    Usage:
    ?editcard code | Card Name | Image URL | eBay Sold Link | Buy Price | Notes
    """
    parts = [part.strip() for part in args.split("|")]

    if len(parts) < 4 or len(parts) > 6:
        await ctx.reply(
            "Use this format:\n"
            "`?editcard code | Card Name | Image URL | eBay Sold Link | Buy Price | Notes`\n"
            "Only the first 4 parts are required. Buy Price and Notes are optional.",
            mention_author=False
        )
        return

    code = parts[0].lower()
    name = parts[1]
    image_url = parts[2]
    ebay_link = parts[3]
    buy_price = parts[4] if len(parts) >= 5 else ""
    notes = parts[5] if len(parts) >= 6 else ""

    cards = load_cards()

    if code not in cards:
        await ctx.reply(
            f"No saved card found for code: **{code}**",
            mention_author=False
        )
        return

    cards[code]["name"] = name
    cards[code]["image_url"] = image_url
    cards[code]["ebay_link"] = ebay_link
    cards[code]["buy_price"] = buy_price
    cards[code]["notes"] = notes

    save_cards(cards)

    embed = discord.Embed(
        title="Card updated",
        description=f"Updated comp entry for **{name}**",
    )
    embed.add_field(name="Code", value=code, inline=True)
    embed.add_field(name="Paid", value=format_price(buy_price), inline=True)

    if notes:
        embed.add_field(name="Notes", value=notes[:1024], inline=False)

    if image_url:
        embed.set_image(url=image_url)

    await ctx.reply(embed=embed, mention_author=False)


@bot.command(name="renamecard")
async def renamecard(ctx: commands.Context, *, args: str):
    """
    Usage:
    ?renamecard oldcode | newcode
    """
    parts = [part.strip() for part in args.split("|")]

    if len(parts) != 2:
        await ctx.reply(
            "Use this format:\n`?renamecard oldcode | newcode`",
            mention_author=False
        )
        return

    old_code = parts[0].lower()
    new_code = parts[1].lower()

    cards = load_cards()

    if old_code not in cards:
        await ctx.reply(
            f"No saved card found for code: **{old_code}**",
            mention_author=False
        )
        return

    if new_code in cards:
        await ctx.reply(
            f"A card with code **{new_code}** already exists.",
            mention_author=False
        )
        return

    cards[new_code] = cards.pop(old_code)
    save_cards(cards)

    await ctx.reply(
        f"Renamed card code from **{old_code}** to **{new_code}**",
        mention_author=False
    )


@bot.command(name="delcard")
async def delcard(ctx: commands.Context, *, code: str):
    """
    Usage:
    ?delcard charizard199
    """
    code = code.strip().lower()
    cards = load_cards()

    if code not in cards:
        await ctx.reply(
            f"No saved card found for code: **{code}**",
            mention_author=False
        )
        return

    deleted_name = cards[code].get("name", code)
    del cards[code]
    save_cards(cards)

    await ctx.reply(
        f"Deleted saved card: **{deleted_name}** (`{code}`)",
        mention_author=False
    )


@bot.command(name="listcards")
async def listcards(ctx: commands.Context):
    cards = load_cards()

    if not cards:
        await ctx.reply("No cards saved yet.", mention_author=False)
        return

    lines = []
    for code, card in sorted(cards.items()):
        paid = format_price(card.get("buy_price", ""))
        lines.append(f"`{code}` — {card.get('name', 'Unknown card')} — Paid: {paid}")

    text = "\n".join(lines)

    if len(text) > 1900:
        text = text[:1900] + "\n..."

    embed = discord.Embed(
        title="Saved cards",
        description=text
    )

    await ctx.reply(embed=embed, mention_author=False)


@bot.command(name="helpcomp")
async def helpcomp(ctx: commands.Context):
    embed = discord.Embed(
        title="Comp bot commands",
        description=(
            "`?addcard code | Card Name | Image URL | eBay Sold Link | Buy Price | Notes`\n"
            "`?comp code`\n"
            "`?setprice code | price`\n"
            "`?setnotes code | notes`\n"
            "`?editcard code | Card Name | Image URL | eBay Sold Link | Buy Price | Notes`\n"
            "`?renamecard oldcode | newcode`\n"
            "`?delcard code`\n"
            "`?listcards`\n"
            "`?ping`"
        )
    )
    await ctx.reply(embed=embed, mention_author=False)


# =========================
# START BOT
# =========================
if not DISCORD_TOKEN:
    raise ValueError("No DISCORD_TOKEN found in .env file. Put it in your .env like: DISCORD_TOKEN=your_token_here")

bot.run(DISCORD_TOKEN)