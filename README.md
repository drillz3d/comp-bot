Pokémon Card Comp Bot

A simple Discord bot for tracking Pokémon card purchases and checking eBay sold listings quickly.

Designed for card sellers and collectors who want a fast way to store cards, check comps, and estimate profit directly inside Discord.

The bot stores cards in a local JSON database and provides commands to:

Save cards

View eBay sold listings

Track buy prices

Add notes

Search your collection

Estimate profit after eBay fees and postage

Features
Card Tracking

Store cards with:

Card name

Image

eBay sold listings search link

Buy price

Notes

eBay Sold Listings

Each card stores a live eBay sold search link so you can instantly check current market value.

Profit Estimation

Calculate estimated profit after:

eBay fees

Postage

Your buy price

Search System

Quickly find saved cards by:

code

card name

notes

How It Works

Cards are stored in:

cards.json

Each card entry contains:

code
name
image_url
ebay_link
buy_price
notes

The card code acts as a unique ID used for commands.

Example:

charizard199
pikachuPromo1
snorlax141
Bot Commands

All commands use the prefix:

?
Add a Card
?addcard code | Card Name | Image URL | eBay Sold Link | Buy Price | Notes

Example:

?addcard charizard199 | Charizard ex 199/165 | https://image.jpg | https://www.ebay.co.uk/sch/i.html?_nkw=charizard+199&LH_Sold=1&LH_Complete=1 | 12.50 | Mint pull

Only the first 4 fields are required.

View a Card
?comp code

Example:

?comp charizard199

Shows:

card image

buy price

notes

clickable title that opens eBay sold listings

Update Buy Price
?setprice code | price

Example:

?setprice charizard199 | 15
Update Notes
?setnotes code | notes

Example:

?setnotes charizard199 | PSA candidate
Edit Card Details
?editcard code | Card Name | Image URL | eBay Sold Link | Buy Price | Notes

Example:

?editcard charizard199 | Charizard ex 199/165 | https://image.jpg | https://ebaylink | 12 | Clean copy
Rename Card Code
?renamecard oldcode | newcode

Example:

?renamecard charizard199 | charizardPaldean199
Delete Card
?delcard code

Example:

?delcard charizard199
List All Saved Cards
?listcards

Shows every saved card with buy price.

Search Cards
?findcard keyword

Searches:

card code

name

notes

Example:

?findcard charizard
Profit Calculator

Estimate profit after fees and postage.

Basic Version
?profit code | saleprice

Example:

?profit charizard199 | 24.99

Uses default values:

eBay Fee: 12.8%
Postage: £2.70
Custom Version
?profit code | saleprice | feepercent | postage

Example:

?profit charizard199 | 24.99 | 12.8 | 2.70
Ping Test
?ping

Returns bot latency.

Help Menu
?helpcomp

Displays all available commands.

Hosting

The bot can run:

locally on your PC

on cloud services such as Render

Recommended hosting:

Render (Free tier)

This allows the bot to run 24/7 even when your PC is off.

Requirements

Python 3.10+

Required packages:

discord.py
python-dotenv

Install with:

pip install discord.py python-dotenv
Environment Variables

Create a .env file:

DISCORD_TOKEN=your_bot_token_here
Start the Bot
python bot.py
Future Ideas

Possible upgrades:

automatic eBay sold scraping

price averaging

PSA grading tracker

portfolio value tracking

profit history

sales tracking

Author

Created for Pokémon card collectors and sellers who want fast comp checking directly inside Discord.
