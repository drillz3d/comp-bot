# Pokémon Card Comp Bot

A Discord bot for saving Pokémon cards, opening eBay sold comps quickly, tracking buy prices, adding notes, searching your saved cards, and estimating profit.

## Features

- Save cards with image, eBay sold link, buy price, and notes
- Open live eBay sold listings from Discord
- Update prices and notes any time
- Rename saved card codes
- Search your saved cards by keyword
- Estimate profit after fees and postage
- Works great for personal flipping / collection tracking

---

## How It Works

Cards are stored in:

```json
cards.json
```

Each card entry contains:
code
name
image_url
ebay_link
buy_price
notes
The card code acts as the unique ID used for commands.

Example card codes:
charizard199
pikachupromo1
snorlax141

Commands

All commands use this prefix:
```
?
```

Add a card
```
?addcard code | Card Name | Image URL | eBay Sold Link | Buy Price | Notes
```
Example: 
```
?addcard charizard199 | Charizard ex 199/165 | https://image.jpg | https://www.ebay.co.uk/sch/i.html?_nkw=charizard+199&LH_Sold=1&LH_Complete=1 |_sop=13 | 12.50 | Mint pull
```
Only the first 4 parts are required.


View a saved card
```
?comp code
```
Example:
```
?comp charizard199
```

Update buy price
```
?setprice code | price
```
Example:
```
?setprice charizard199 | 15
```

Update notes
```
?setnotes code | notes
```
Example:
```
?setnotes charizard199 | PSA candidate
```

Edit a card
```
?editcard code | Card Name | Image URL | eBay Sold Link | Buy Price | Notes
```
Example:
```
?editcard charizard199 | Charizard ex 199/165 | https://image.jpg | https://ebaylink | 12 | Clean copy
```

Rename a card code
```
?renamecard oldcode | newcode
```
Example:
```
?renamecard charizard199 | charizardpaldean199
```

Delete a card
```
?delcard code
```
Example:
```
?delcard charizard199
```

List all saved cards
```
?listcards
```

Search saved cards
```
?findcard keyword
```
Example:
```
?findcard charizard
```

Profit calculator
Basic version:
```
?profit code | saleprice
```
Example:
```
?profit charizard199 | 24.99
```

Custom version:
```
?profit code | saleprice | feepercent | postage
```
Example:
```
?profit charizard199 | 24.99 | 12.8 | 2.70
```

Ping test
```
?ping
```

Help menu
```
?helpcomp
```

Default Profit Settings

The bot currently uses these defaults for the quick profit command:

eBay fee: 12.8%
Postage: £2.70
Requirements

Python 3.10+ recommended.

Install required packages:
```
pip install discord.py python-dotenv
```
Or from a requirements file:
```
pip install -r requirements.txt
Environment Variable
```
Create a .env file locally with:
```
DISCORD_TOKEN=your_bot_token_here
```
If hosting on Render, add this as an environment variable instead of uploading .env.
```
Run Locally
python bot.py
Hosting
```

This bot can run:

Locally on your PC

On Render for 24/7 uptime

On other Python-friendly cloud hosts

Recommended for personal use:

Render (Free tier)
Example Use Case

Save a card:
```
?addcard charizard199 | Charizard ex 199/165 | https://image.jpg | https://www.ebay.co.uk/sch/i.html?_nkw=charizard+199&LH_Sold=1&LH_Complete=1&_sop=13 | 12.50 | Mint pull
```
Check the card:
```
?comp charizard199
```
Update the price later:
```
?setprice charizard199 | 14.99
```
Check profit:
```
?profit charizard199 | 24.99
```

File Structure
```
comp-bot/
├── bot.py
├── cards.json
├── requirements.txt
├── README.md
└── .env
```

Future Ideas

* Possible upgrades:

* Collection value command

* ROI percentage command

* Export to CSV

* Separate sold / raw / graded tracking

* Category tags

* Admin-only command restrictions

* Sales history log


Author:
Built as a personal Discord tool for Pokémon card comp checking, price tracking, and flip profit estimation.
