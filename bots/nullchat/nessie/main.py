import pyrode
import random
import time
import json
import difflib
import asyncio

bot = pyrode.Bot(prefix="!")

# ─────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────

ALL_ITEMS = [
    "Hammer","Wrench","Screwdriver","Tape","Saw","Nail","Drill","Pliers",
    "Flashlight","Glue","Scissors","Level","Ladder","Bucket","Rope","Hook",
    "Shovel","Crowbar","Binoculars","Compass","Helmet","Wheel","Pulley","Crank",
    "Battery","Whistle","Parachute","Umbrella","Balloon","Mirror","Goggles",
    "Tablet","Marker","Cable","Sensor","Wrenchset","Chain","Button","Clipper",
    "Handle","Panel","Belt","Rod","Valve","Screen","Knob","Hose","Pin","Plug",
    "Brick","Spanner","Torch","Screws","Nuts","Bolts","Springs","Gears","Magnets",
    "Wire","Fuse","Switch","Timer","Thermometer","Scale","Ruler","Protractor",
    "Pencil","Eraser","Calculator","Clock","Camera","Microphone","Speaker",
    "Headphones","Keyboard","Mouse","Monitor","Printer","Scanner","Router","Modem",
    "Antenna","Satellite","Solar-Panel","Generator","Turbine","Engine","Motor",
    "Pump","Filter","Valve-Handle","Gauge","Dial","Lever","Pulley-System",
    "Conveyor","Crane","Forklift","Jack","Winch",
    "Apple","Ice-cream","Bread","Steak","Berries","Mushroom","Corn","Carrot",
    "Potato","Fish","Egg","Cheese","Milk","Honey","Chocolate","Cookie","Cake",
    "Sandwich","Soup","Pizza","Burger","Taco","Sushi","Donut","Muffin","Candy",
    "Lollipop","Gummy-Bear","Chips","Popcorn",
    "Healing-Potion","Energy-Drink","Strength-Potion","Speed-Potion","Luck-Potion",
    "Invisibility-Potion","Fire-Resistance-Potion","Night-Vision-Potion",
    "Water-Breathing-Potion","Levitation-Potion",
    "Potion-Of-Badluck","Potion-Of-Badluck-II","Potion-Of-Badluck-III",
    "Potion-Of-Badluck-IV","Potion-Of-Badluck-V",
    "Knife","Sword","Iron-Sword","Golden-Sword","Diamond-Sword","Bow","Arrow",
    "Crossbow","Spear","Axe","Dagger","Mace","Flail","Halberd","Katana","Scythe",
    "Trident","Whip","Mickey's-Glove","Gun","Fire-Sword","Ice-Staff","Lightning-Rod",
    "Double-Sword","Berserker-Axe","Life-Steal-Dagger","Golden-Wrench","Diamond-Drill",
    "Magic-Hammer","Poison-Dart","Shield","Iron-Shield","Golden-Shield","Diamond-Shield",
    "Iron-Armor","Golden-Armor","Diamond-Armor","Invisibility-Cloak",
    "Coal","Iron-Ore","Gold-Ore","Diamond","Emerald","Ruby","Sapphire","Amethyst",
    "Obsidian","Quartz","Lapis","Redstone","Netherite","Crystal-Shard","Soul-Gem",
    "Chaos-Gem","Mana-Crystal","Magic-Wand","Spell-Book","Rune-Stone","Amulet",
    "Talisman","Orb-Of-Power","Staff-Of-Life","Void-Crystal","Time-Stop-Watch",
    "Teleporter","Luck-Charm","Magnet-Glove","Revival-Crystal","Smoke-Bomb",
    "Enchanting-Table","Jetpack","Laser-Pointer","Hologram-Projector","EMP-Device",
    "Nano-Bot","Drone","Hacking-Device","Cloaking-Device","Energy-Shield",
    "Plasma-Cutter","Gravity-Gun","Portal-Gun","String","Leather","Wool","Silk",
    "Feather","Bone","Clay","Sand","Gravel","Wood","Stone","Iron-Ingot","Gold-Ingot",
    "Diamond-Ingot","Gunpowder","Blaze-Rod","Ender-Pearl","Dragon-Scale",
    "Phoenix-Feather","Unicorn-Horn","Troll-Blood","Excalibur","Mjolnir",
    "Poseidons-Trident","Zeus-Bolt","Philosophers-Stone","Holy-Grail","Pandoras-Box",
    "Infinity-Gem","First-Aid","Lockpick","Perfume","Mystery-box","Money-Box",
    "Taser","Adminjuice","Killspray","Super-weapon","Ultimate-armor","Metal-Detector",
    "C4-Charge","Business-License","Golden-Apple","Nuclear-Bomb"
]

ITEM_PRICES = {
    "Hammer":15,"Wrench":12,"Screwdriver":10,"Tape":8,"Saw":18,"Nail":5,"Drill":25,
    "Pliers":14,"Flashlight":20,"Glue":10,"Scissors":12,"Level":16,"Ladder":30,
    "Bucket":15,"Rope":18,"Hook":10,"Shovel":22,"Binoculars":35,"Compass":25,
    "Wheel":50,"Pulley":30,"Crank":20,"Battery":25,"Whistle":8,"Parachute":75,
    "Umbrella":20,"Balloon":5,"Mirror":15,"Goggles":30,"Tablet":100,"Marker":6,
    "Cable":12,"Sensor":45,"Wrenchset":40,"Chain":25,"Button":8,"Clipper":18,
    "Handle":10,"Panel":30,"Rod":15,"Valve":20,"Screen":60,"Knob":8,"Hose":25,
    "Pin":3,"Plug":10,"Brick":12,"Spanner":16,"Torch":22,"Screws":4,"Nuts":3,
    "Bolts":5,"Springs":8,"Gears":15,"Magnets":12,"Wire":6,"Fuse":10,"Switch":14,
    "Timer":18,"Thermometer":20,"Scale":25,"Ruler":5,"Protractor":8,"Pencil":2,
    "Eraser":1,"Calculator":30,"Clock":35,"Camera":80,"Microphone":45,"Speaker":50,
    "Headphones":40,"Keyboard":60,"Mouse":25,"Monitor":150,"Printer":120,"Scanner":100,
    "Router":75,"Modem":60,"Antenna":30,"Satellite":200,"Solar-Panel":180,
    "Generator":300,"Turbine":250,"Engine":400,"Motor":150,"Pump":80,"Filter":25,
    "Valve-Handle":15,"Gauge":35,"Dial":20,"Lever":18,"Pulley-System":45,
    "Conveyor":120,"Crane":500,"Forklift":400,"Jack":60,"Winch":85,
    "Apple":5,"Ice-cream":2,"Bread":10,"Steak":50,"Berries":4,"Mushroom":5,
    "Corn":3,"Carrot":2,"Potato":2,"Fish":8,"Egg":1,"Cheese":6,"Milk":3,
    "Honey":10,"Chocolate":8,"Cookie":4,"Cake":20,"Sandwich":7,"Soup":6,
    "Pizza":18,"Burger":15,"Taco":10,"Sushi":25,"Donut":5,"Muffin":4,"Candy":2,
    "Lollipop":1,"Gummy-Bear":1,"Chips":3,"Popcorn":2,
    "Healing-Potion":200,"Energy-Drink":60,"Strength-Potion":150,"Speed-Potion":120,
    "Luck-Potion":180,"Invisibility-Potion":300,"Fire-Resistance-Potion":200,
    "Night-Vision-Potion":100,"Water-Breathing-Potion":100,"Levitation-Potion":250,
    "Potion-Of-Badluck":80,"Potion-Of-Badluck-II":0,"Potion-Of-Badluck-III":0,
    "Potion-Of-Badluck-IV":0,"Potion-Of-Badluck-V":0,
    "Knife":150,"Sword":80,"Iron-Sword":150,"Golden-Sword":300,"Diamond-Sword":600,
    "Bow":100,"Arrow":5,"Crossbow":200,"Spear":120,"Axe":90,"Dagger":70,"Mace":110,
    "Flail":130,"Halberd":180,"Katana":400,"Scythe":350,"Trident":450,"Whip":80,
    "Mickey's-Glove":150,"Gun":200,"Fire-Sword":400,"Ice-Staff":350,"Lightning-Rod":500,
    "Double-Sword":550,"Berserker-Axe":420,"Life-Steal-Dagger":320,"Golden-Wrench":500,
    "Diamond-Drill":800,"Magic-Hammer":350,"Poison-Dart":120,"Iron-Shield":200,
    "Golden-Shield":400,"Diamond-Shield":700,"Iron-Armor":300,"Golden-Armor":600,
    "Diamond-Armor":1200,"Invisibility-Cloak":380,"Shield":250,
    "Coal":5,"Iron-Ore":15,"Gold-Ore":40,"Diamond":200,"Emerald":250,"Ruby":300,
    "Sapphire":280,"Amethyst":150,"Obsidian":50,"Quartz":30,"Lapis":20,"Redstone":10,
    "Netherite":800,"Crystal-Shard":100,"Soul-Gem":500,"Chaos-Gem":1000,
    "Mana-Crystal":300,"Magic-Wand":200,"Spell-Book":350,"Rune-Stone":150,
    "Amulet":180,"Talisman":160,"Orb-Of-Power":600,"Staff-Of-Life":700,
    "Void-Crystal":900,"Time-Stop-Watch":600,"Teleporter":450,"Luck-Charm":180,
    "Magnet-Glove":220,"Revival-Crystal":750,"Smoke-Bomb":90,"Enchanting-Table":500,
    "Jetpack":1000,"Laser-Pointer":150,"Hologram-Projector":400,"EMP-Device":300,
    "Nano-Bot":500,"Drone":350,"Hacking-Device":450,"Cloaking-Device":600,
    "Energy-Shield":400,"Plasma-Cutter":550,"Gravity-Gun":800,"Portal-Gun":1200,
    "String":5,"Leather":10,"Wool":8,"Silk":20,"Feather":3,"Bone":5,"Clay":4,
    "Sand":2,"Gravel":2,"Wood":3,"Stone":4,"Iron-Ingot":20,"Gold-Ingot":50,
    "Diamond-Ingot":150,"Gunpowder":15,"Blaze-Rod":40,"Ender-Pearl":60,
    "Dragon-Scale":500,"Phoenix-Feather":600,"Unicorn-Horn":700,"Troll-Blood":400,
    "Excalibur":5000,"Mjolnir":5000,"Poseidons-Trident":4500,"Zeus-Bolt":4500,
    "Philosophers-Stone":6000,"Holy-Grail":5500,"Pandoras-Box":3000,"Infinity-Gem":10000,
    "First-Aid":80,"Lockpick":85,"Perfume":40,"Mystery-box":120,"Belt":120,
    "Crowbar":111,"Taser":350,"Adminjuice":400,"Killspray":750,"Metal-Detector":1000,
    "C4-Charge":5000,"Business-License":25000,"Golden-Apple":500,"Nuclear-Bomb":12000000
}

FOOD_HEALS = {
    "Apple":1,"Steak":5,"Bread":2,"Fish":3,"Cake":4,
    "Healing-Potion":10,"Energy-Drink":3
}

DURABILITIES = {
    "Mickey's-Glove":2,"First-Aid":1,"Gun":5,"Belt":2,"Crowbar":1,
    "Golden-Wrench":5,"Diamond-Drill":10,"Shield":5,"Fire-Sword":3,
    "Ice-Staff":2,"Lightning-Rod":1,"Knife":10,"Bodyguard":3
}

CRAFTABLE = {
    "taser":    {"req":["Screwdriver","Button","Gun","Cable","Battery"],  "result":"Taser",      "msg":"You've crafted a Taser!"},
    "adminjuice":{"req":["Glue","Torch","Battery","Marker","First-Aid"],  "result":"Adminjuice", "msg":"You've mixed AdminJuice!"},
    "killspray":{"req":["Bucket","Hose","Button","Battery","Adminjuice"], "result":"Killspray",  "msg":"You've crafted KillSpray!"},
    "mystery-box":{"req":["Bucket","Panel","Button","Sensor","Battery"],  "result":"Mystery-box","msg":"You've crafted a Mystery Box!"}
}

ENCHANT_COSTS = {
    "Potion-Of-Badluck":    {"next":"Potion-Of-Badluck-II",  "cost":500},
    "Potion-Of-Badluck-II": {"next":"Potion-Of-Badluck-III", "cost":1000},
    "Potion-Of-Badluck-III":{"next":"Potion-Of-Badluck-IV",  "cost":2500},
    "Potion-Of-Badluck-IV": {"next":"Potion-Of-Badluck-V",   "cost":5000},
}

CURSE_EFFECTS = {
    "Potion-Of-Badluck":    {"money_loss":(10,50)},
    "Potion-Of-Badluck-II": {"money_loss":(50,200),  "cant_work":1800},
    "Potion-Of-Badluck-III":{"money_loss":(100,500), "cant_work":3600,  "remove_item":True},
    "Potion-Of-Badluck-IV": {"money_loss":(200,800), "health_drain":2, "cant_work":7200, "remove_item":True},
    "Potion-Of-Badluck-V":  {"money_loss":(500,2000),"health_drain":4, "cant_work":14400,"remove_item":True,"remove_items_count":3},
}

PROPERTIES = {
    "Launching-Facility":{"cost":1000000,"desc":"Required to launch nukes","emoji":"🚀"},
    "Workplace":         {"cost":500000, "desc":"Earns $500/hr for all members","emoji":"🏢","income":500},
    "Skyscraper":        {"cost":2000000,"desc":"Increases max capacity to 20","emoji":"🏙️","capacity":20},
    "Bodyguard-Deployer":{"cost":750000, "desc":"Deploys a bodyguard with 3 HP","emoji":"🛡️","bodyguard_hp":3},
    "Casino":            {"cost":3000000,"desc":"Earns $1000/hr for all members","emoji":"🎰","income":1000},
    "Factory":           {"cost":1500000,"desc":"Earns $750/hr for all members","emoji":"🏭","income":750},
    "Farm":              {"cost":250000, "desc":"Earns $200/hr for all members","emoji":"🌾","income":200},
    "Mine":              {"cost":800000, "desc":"Random ore drops hourly","emoji":"⛏️"},
    "Bank":              {"cost":5000000,"desc":"Protects home money from nukes","emoji":"🏦"},
    "Gym":               {"cost":400000, "desc":"Bonus to workout gains","emoji":"🏋️","workout_bonus":2},
}

STRENGTH_LEVELS = [
    (50,"💀 Elite",5,25,25),(35,"⚡ Very Strong",4,20,20),(20,"🔥 Strong",3,15,15),
    (10,"💪 Average",2,10,10),(5,"🏋️ Beginner",1,5,5),(0,"💪 Weak",0,0,0)
]

NUMBER_EMOJIS = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
WORKOUT_EMOJIS = ['💪','🏋️','🤸','🏃','🧘','🤼','🤾','🏊','🚴','🧗']
ADMIN_IDS = {"745618132118405161","1378378350544031947"}

# ─────────────────────────────────────────────────────────────
# DB HELPERS  (backed by bot.files as JSON)
# ─────────────────────────────────────────────────────────────

async def _load(filename):
    raw = await bot.files.read(filename)
    if raw is None:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}

async def _save(filename, data):
    await bot.files.write(filename, json.dumps(data))

async def get_user(uid):
    uid = str(uid)
    db = await _load("users.json")
    if uid not in db:
        db[uid] = {
            "health":10,"money":50,"level":1,"exp":0,"wins":0,"losses":0,
            "wanted":0,"wanted_timer":0,"jail":0,"jail_until":0,"married_to":None,
            "security":0,"last_daily":0,"cant_work_until":0,"bounty":0,
            "banned":0,"strength":0,"bodyguard":0,"items":{},"box_amounts":[]
        }
        await _save("users.json", db)
    u = db[uid]
    # ensure new fields on old accounts
    for k,v in [("items",{}),("box_amounts",[]),("bounty",0),("strength",0),
                ("bodyguard",0),("cant_work_until",0),("wanted_timer",0),("banned",0)]:
        u.setdefault(k,v)
    return u, db

async def save_user(uid, db):
    await _save("users.json", db)

async def get_home(uid):
    uid = str(uid)
    homes = await _load("homes.json")
    for hid, h in homes.items():
        members = [m for m in h.get("members","").split(",") if m]
        if uid == h.get("owner") or uid in members:
            return h, homes
    return None, homes

async def save_homes(homes):
    await _save("homes.json", homes)

def fuzzy_find(query, items_list, limit=5):
    query = query.lower().strip()
    exact = [i for i in items_list if query in i.lower()]
    if exact:
        return exact[:limit]
    matches = difflib.get_close_matches(query, [i.lower() for i in items_list], n=limit, cutoff=0.3)
    result = []
    for m in matches:
        for i in items_list:
            if i.lower() == m:
                result.append(i); break
    return result

def strength_info(s):
    for threshold,name,bb,rb,pp in STRENGTH_LEVELS:
        if s >= threshold:
            return name,bb,rb,pp
    return "💪 Weak",0,0,0

def fmt_items(items_dict):
    lines = []
    for item,qty in sorted(items_dict.items()):
        if item in DURABILITIES:
            lines.append(f"**{item}**: {qty} (Dur: {qty*DURABILITIES[item]})")
        else:
            lines.append(f"**{item}**: {qty}")
    return lines

async def check_player(ctx):
    u, _ = await get_user(ctx.author.id)
    if u.get("banned"):
        await ctx.send("🚫 You are banned.")
        return False
    if u["health"] <= 0:
        await ctx.send("💀 You are dead! Use `!revive`.")
        return False
    if u["jail"] and time.time() < u["jail_until"]:
        rem = int(u["jail_until"] - time.time())
        await ctx.send(f"🔒 Jailed for {rem}s!")
        return False
    return True

# In-memory cooldowns / state
_knife_cd = {}
_workout_cd = {}
_active_nessie = set()
_passive_task_started = False

# ─────────────────────────────────────────────────────────────
# ON READY
# ─────────────────────────────────────────────────────────────

@bot.event
async def on_ready():
    global _passive_task_started
    print(f"Nessie ready: {bot.name}")
    if not _passive_task_started:
        _passive_task_started = True
        asyncio.ensure_future(_passive_income_loop())

async def _passive_income_loop():
    while True:
        await asyncio.sleep(3600)
        homes = await _load("homes.json")
        for hid, h in homes.items():
            props = [p for p in h.get("properties","").split(",") if p]
            income = sum(PROPERTIES[p].get("income",0) for p in props if p in PROPERTIES)
            if income > 0:
                h["money"] = h.get("money",0) + income
        await save_homes(homes)

# ─────────────────────────────────────────────────────────────
# ON MESSAGE  (Nessie trigger + process commands)
# ─────────────────────────────────────────────────────────────

@bot.event
async def on_message(message):
    if message.author.is_bot:
        return
    content = message.content.lower().strip()
    await bot.process_commands(message)

    nessie_triggers = {"hey nessie","ohh nessie","ohhh nessie","sup nessie!","wheres nessie","whos nessie"}
    if content in nessie_triggers:
        uid = str(message.author.id)
        if uid in _active_nessie:
            await bot.channel.send(f"{message.author.display}, you're already choosing!")
            return
        u, db = await get_user(message.author.id)
        if u["health"] <= 0:
            await bot.channel.send(f"{message.author.display}, you are dead! Use `!revive` first.")
            return
        _active_nessie.add(uid)
        chosen = random.choices(ALL_ITEMS, k=4)
        lines = "\n".join(f"{NUMBER_EMOJIS[i]} {item}" for i,item in enumerate(chosen))
        await bot.channel.send(
            f"🐉 **Nessie has arrived!** React with a number to choose your item:\n\n{lines}\n\n"
            f"*(Type 1, 2, 3 or 4 within 30 seconds)*"
        )
        def pick_check(m):
            return (m.author.id == message.author.id and
                    m.content.strip() in ["1","2","3","4"])
        try:
            reply = await bot.wait_for("message", check=pick_check, timeout=30)
            idx = int(reply.content.strip()) - 1
            item = chosen[idx]
            u["items"][item] = u["items"].get(item,0) + 1
            await save_user(message.author.id, db)
            await bot.channel.send(f"🎉 {message.author.display} chose **{item}**!")
        except asyncio.TimeoutError:
            await bot.channel.send(f"🕐 {message.author.display} took too long! Nessie swam away.")
        finally:
            _active_nessie.discard(uid)

    elif content == "nessie":
        await message.reply("🐉")

# ─────────────────────────────────────────────────────────────
# ECONOMY
# ─────────────────────────────────────────────────────────────

@bot.command()
async def balance(ctx, *, target_name: str = None):
    """Check balance. !balance or !balance username"""
    if target_name:
        u, _ = await get_user(ctx.author.id)
        await ctx.send(f"💰 Balance lookup: use `!balance` for yourself (can't look up others by name in Pyrode).")
        return
    u, _ = await get_user(ctx.author.id)
    await ctx.send(f"💰 **{ctx.author.display}'s Balance: ${u['money']:,}**")

@bot.command()
async def work(ctx):
    """Type the words to earn money."""
    if not await check_player(ctx): return
    u, db = await get_user(ctx.author.id)
    if time.time() < u.get("cant_work_until",0):
        rem = int(u["cant_work_until"] - time.time())
        await ctx.send(f"😵 You're cursed! Can't work for {rem}s."); return
    words = ["nessie","lake","monster","hoover","crystal","diamond","water","ancient",
             "magic","dragon","sword","shield","potion","battle","treasure"]
    target = " ".join(random.choices(words, k=random.randint(3,5)))
    await ctx.send(f"📝 Type this in 10 seconds:\n\n`{target}`")
    def chk(m): return m.author.id == ctx.author.id
    try:
        msg = await bot.wait_for("message", check=chk, timeout=10)
        if msg.content.strip().lower() == target:
            bonus = min(100, u.get("strength",0)//2)
            base = random.randint(100,250)
            total = base + bonus
            u["money"] += total
            await save_user(ctx.author.id, db)
            await ctx.send(f"✅ Correct! Earned **${total}** (${base} base + ${bonus} strength bonus)")
        else:
            await ctx.send("❌ Incorrect! No payment.")
    except asyncio.TimeoutError:
        await ctx.send("⌛ Too slow! No payment.")

@bot.command()
async def daily(ctx):
    """Claim your daily reward."""
    if not await check_player(ctx): return
    u, db = await get_user(ctx.author.id)
    now = time.time()
    if now - u["last_daily"] < 86400:
        rem = int(86400 - (now - u["last_daily"]))
        h,m = rem//3600,(rem%3600)//60
        await ctx.send(f"⏰ Daily ready in {h}h {m}m!"); return
    base = random.randint(300,700)
    bonus = min(200, u.get("strength",0))
    total = base + bonus
    bonus_item = None
    if random.random() < 0.3:
        bonus_item = random.choice(ALL_ITEMS)
        u["items"][bonus_item] = u["items"].get(bonus_item,0) + 1
    u["money"] += total
    u["last_daily"] = now
    await save_user(ctx.author.id, db)
    msg = f"🎁 **Daily Reward!** +${total:,}"
    if bonus_item: msg += f" + 1x {bonus_item}"
    await ctx.send(msg)

@bot.command()
async def pay(ctx, amount: int, *, target_name: str):
    """Pay someone. !pay 100 username"""
    if not await check_player(ctx): return
    if amount < 1: await ctx.send("❌ Pay at least $1!"); return
    u, db = await get_user(ctx.author.id)
    if u["money"] < amount: await ctx.send(f"❌ You only have ${u['money']:,}!"); return
    # Find member by display name from server members
    members = bot.server.get("members", []) if hasattr(bot, "server") and bot.server else []
    target_id = None
    for m in members:
        if m.get("display","").lower() == target_name.lower() or m.get("username","").lower() == target_name.lower():
            target_id = m["id"]; break
    if not target_id:
        await ctx.send(f"❌ User '{target_name}' not found."); return
    u2, db2 = await get_user(target_id)
    u["money"] -= amount
    u2["money"] += amount
    db[str(ctx.author.id)] = u
    db[str(target_id)] = u2
    await _save("users.json", db)
    await ctx.send(f"💸 Paid **${amount:,}** to **{target_name}**!")

@bot.command()
async def shop(ctx, *, query: str = None):
    """Browse the shop. !shop or !shop sword"""
    if not await check_player(ctx): return
    items = {k:v for k,v in ITEM_PRICES.items() if v > 0}
    if query:
        matches = fuzzy_find(query, list(items.keys()), 15)
        if not matches: await ctx.send(f"❌ No items found for '{query}'"); return
        lines = [f"**{i}** — ${items[i]:,}" for i in matches]
        await ctx.send(f"🔍 **Results for '{query}':**\n" + "\n".join(lines))
        return
    # Show first 20 items paginated as text
    keys = list(items.keys())
    page = [f"**{k}** — ${items[k]:,}" for k in keys[:25]]
    await ctx.send(
        f"🛒 **Nessie's Shop** (showing first 25 of {len(keys)} items — use `!shop <name>` to search)\n\n" +
        "\n".join(page)
    )

@bot.command()
async def buy(ctx, *, item_name: str):
    """Buy an item from the shop."""
    if not await check_player(ctx): return
    purchasable = {k:v for k,v in ITEM_PRICES.items() if v > 0}
    # exact match
    match = next((k for k in purchasable if k.lower() == item_name.lower()), None)
    if not match:
        results = fuzzy_find(item_name, list(purchasable.keys()), 1)
        if not results: await ctx.send(f"❌ Item '{item_name}' not found!"); return
        match = results[0]
        await ctx.send(f"🔍 Did you mean **{match}**? Type `yes` to confirm or anything else to cancel.")
        def chk(m): return m.author.id == ctx.author.id
        try:
            r = await bot.wait_for("message", check=chk, timeout=15)
            if r.content.strip().lower() != "yes": await ctx.send("❌ Cancelled."); return
        except asyncio.TimeoutError: await ctx.send("⌛ Timed out."); return
    price = purchasable[match]
    u, db = await get_user(ctx.author.id)
    if u["money"] < price: await ctx.send(f"❌ Need ${price:,}! You have ${u['money']:,}"); return
    await ctx.send(f"Buy **{match}** for **${price:,}**? (yes/no)")
    def chk(m): return m.author.id == ctx.author.id
    try:
        r = await bot.wait_for("message", check=chk, timeout=30)
        if r.content.strip().lower() != "yes": await ctx.send("❌ Cancelled."); return
        u["money"] -= price
        u["items"][match] = u["items"].get(match,0) + 1
        await save_user(ctx.author.id, db)
        await ctx.send(f"✅ Bought **{match}** for **${price:,}**! Balance: ${u['money']:,}")
    except asyncio.TimeoutError:
        await ctx.send("⌛ Timed out.")

@bot.command()
async def sell(ctx, item_name: str, count: int = 1):
    """Sell an item for half price."""
    if not await check_player(ctx): return
    u, db = await get_user(ctx.author.id)
    found = next((k for k in u["items"] if k.lower() == item_name.lower()), None)
    if not found: await ctx.send(f"❌ You don't have '{item_name}'!"); return
    if u["items"][found] < count: await ctx.send(f"❌ You only have {u['items'][found]}x {found}!"); return
    sell_price = max(1, ITEM_PRICES.get(found,10)//2)
    total = sell_price * count
    u["items"][found] -= count
    if u["items"][found] <= 0: del u["items"][found]
    u["money"] += total
    await save_user(ctx.author.id, db)
    await ctx.send(f"💵 Sold **{count}x {found}** for **${total:,}** (${sell_price} each)")

@bot.command()
async def leaderboard(ctx, stat: str = "money"):
    """View leaderboard. !leaderboard money/health/wins/level/strength"""
    valid = ["money","health","wins","level","strength"]
    if stat not in valid: await ctx.send(f"❌ Valid stats: {', '.join(valid)}"); return
    db = await _load("users.json")
    rows = sorted(db.items(), key=lambda x: x[1].get(stat,0), reverse=True)[:10]
    medals = ["🥇","🥈","🥉"]
    lines = []
    for i,(uid,u) in enumerate(rows):
        m = medals[i] if i < 3 else f"{i+1}."
        val = f"${u[stat]:,}" if stat == "money" else str(u.get(stat,0))
        lines.append(f"{m} <@{uid}> — {val}")
    await ctx.send(f"🏆 **Leaderboard — {stat.title()}**\n\n" + "\n".join(lines))

# ─────────────────────────────────────────────────────────────
# ITEMS
# ─────────────────────────────────────────────────────────────

@bot.command(name="items")
async def cmd_items(ctx):
    """View your inventory."""
    if not await check_player(ctx): return
    u, _ = await get_user(ctx.author.id)
    if not u["items"]: await ctx.send("📦 You have no items."); return
    lines = fmt_items(u["items"])
    total = sum(u["items"].values())
    # split into chunks of 20
    for i in range(0,len(lines),20):
        chunk = "\n".join(lines[i:i+20])
        pg = f" (Page {i//20+1})" if len(lines) > 20 else ""
        await ctx.send(f"📦 **{ctx.author.display}'s Items{pg}** (Total: {total})\n\n{chunk}")

@bot.command()
async def inspect(ctx, *, item_name: str):
    """Inspect an item's details."""
    matches = fuzzy_find(item_name, ALL_ITEMS, 1)
    if not matches: await ctx.send(f"❌ Item '{item_name}' not found!"); return
    item = matches[0]
    price = ITEM_PRICES.get(item,0)
    lines = [f"🔍 **{item}**"]
    lines.append(f"Buy: ${price:,} | Sell: ${max(1,price//2):,}" if price > 0 else "Not for sale")
    if item in DURABILITIES: lines.append(f"Durability: {DURABILITIES[item]} uses per item")
    if item in FOOD_HEALS: lines.append(f"Food: +{FOOD_HEALS[item]} HP")
    key = item.lower()
    if key in CRAFTABLE: lines.append(f"Craft recipe: {', '.join(CRAFTABLE[key]['req'])}")
    if item in ENCHANT_COSTS:
        e = ENCHANT_COSTS[item]
        lines.append(f"Enchant → {e['next']} for ${e['cost']:,} + Adminjuice")
    await ctx.send("\n".join(lines))

@bot.command()
async def craftlist(ctx):
    """Show all craftable items."""
    lines = ["🔧 **Crafting Recipes**\n"]
    for item,data in CRAFTABLE.items():
        lines.append(f"**{item.capitalize()}** — Needs: {', '.join(data['req'])}")
    await ctx.send("\n".join(lines) + "\n\nUse `!make <item>` to craft.")

@bot.command()
async def make(ctx, *, item_name: str):
    """Craft an item. !make taser"""
    if not await check_player(ctx): return
    key = next((k for k in CRAFTABLE if k.lower() == item_name.lower()), None)
    if not key: await ctx.send(f"❌ Can't craft '{item_name}'. Use `!craftlist`."); return
    recipe = CRAFTABLE[key]
    u, db = await get_user(ctx.author.id)
    missing = [r for r in recipe["req"] if u["items"].get(r,0) < 1]
    if missing: await ctx.send(f"❌ Missing: {', '.join(missing)}"); return
    for r in recipe["req"]:
        u["items"][r] -= 1
        if u["items"][r] <= 0: del u["items"][r]
    result = recipe["result"]
    u["items"][result] = u["items"].get(result,0) + 1
    await save_user(ctx.author.id, db)
    await ctx.send(f"🔧 {recipe['msg']}")

@bot.command()
async def enchant(ctx):
    """Enchant a Potion-Of-Badluck."""
    if not await check_player(ctx): return
    u, db = await get_user(ctx.author.id)
    enchantable = [p for p in ENCHANT_COSTS if u["items"].get(p,0) > 0]
    if not enchantable: await ctx.send("❌ No enchantable potions. Buy Potion-Of-Badluck from shop."); return
    if u["items"].get("Adminjuice",0) < 1: await ctx.send("❌ Need Adminjuice! Craft it with `!make adminjuice`."); return
    options = "\n".join(f"{i+1}. {p} → {ENCHANT_COSTS[p]['next']} (${ENCHANT_COSTS[p]['cost']:,})" for i,p in enumerate(enchantable))
    await ctx.send(f"🧪 **Enchant Potion**\n\n{options}\n\nType a number to select:")
    def chk(m): return m.author.id == ctx.author.id and m.content.strip().isdigit()
    try:
        r = await bot.wait_for("message", check=chk, timeout=30)
        idx = int(r.content.strip()) - 1
        if idx < 0 or idx >= len(enchantable): await ctx.send("❌ Invalid."); return
        sel = enchantable[idx]
        cost = ENCHANT_COSTS[sel]["cost"]
        nxt  = ENCHANT_COSTS[sel]["next"]
        u, db = await get_user(ctx.author.id)
        if u["money"] < cost: await ctx.send(f"❌ Need ${cost:,}!"); return
        u["money"] -= cost
        u["items"][sel] -= 1
        if u["items"][sel] <= 0: del u["items"][sel]
        u["items"]["Adminjuice"] -= 1
        if u["items"]["Adminjuice"] <= 0: del u["items"]["Adminjuice"]
        u["items"][nxt] = u["items"].get(nxt,0) + 1
        await save_user(ctx.author.id, db)
        await ctx.send(f"✨ **Enchanted!** {sel} → {nxt} | Cost: ${cost:,}")
    except asyncio.TimeoutError:
        await ctx.send("⌛ Timed out.")

@bot.command()
async def makebox(ctx, amount: int):
    """Seal money in a Money-Box."""
    if not await check_player(ctx): return
    if amount < 1: await ctx.send("❌ At least $1!"); return
    u, db = await get_user(ctx.author.id)
    if u["money"] < amount: await ctx.send(f"❌ Only have ${u['money']:,}!"); return
    u["money"] -= amount
    u["items"]["Money-Box"] = u["items"].get("Money-Box",0) + 1
    u["box_amounts"].append(amount)
    await save_user(ctx.author.id, db)
    await ctx.send(f"📦 Created a Money-Box with **${amount:,}** sealed inside!")

@bot.command(name="open")
async def cmd_open(ctx):
    """Open a Money-Box."""
    if not await check_player(ctx): return
    u, db = await get_user(ctx.author.id)
    if u["items"].get("Money-Box",0) < 1: await ctx.send("❌ No Money-Boxes!"); return
    boxes = u.get("box_amounts",[])
    if not boxes: await ctx.send("❌ Money-Boxes have no amounts!"); return
    if len(boxes) == 1:
        amount = boxes[0]
        u["box_amounts"] = []; u["items"]["Money-Box"] -= 1
        if u["items"]["Money-Box"] <= 0: del u["items"]["Money-Box"]
        u["money"] += amount
        await save_user(ctx.author.id, db)
        await ctx.send(f"📦 Opened Money-Box! You received **${amount:,}**!")
        return
    lines = "\n".join(f"{i+1}. Box #{i+1} — ${boxes[i]:,}" for i in range(min(10,len(boxes))))
    await ctx.send(f"📦 **Your Money-Boxes:**\n{lines}\n\nType the box number to open:")
    def chk(m): return m.author.id == ctx.author.id and m.content.strip().isdigit()
    try:
        r = await bot.wait_for("message", check=chk, timeout=30)
        idx = int(r.content.strip()) - 1
        if idx < 0 or idx >= len(boxes): await ctx.send("❌ Invalid."); return
        amount = boxes[idx]
        u["box_amounts"].pop(idx)
        u["items"]["Money-Box"] -= 1
        if u["items"]["Money-Box"] <= 0: del u["items"]["Money-Box"]
        u["money"] += amount
        await save_user(ctx.author.id, db)
        await ctx.send(f"📦 Opened Box #{idx+1}! Got **${amount:,}**!")
    except asyncio.TimeoutError:
        await ctx.send("⌛ Timed out.")

@bot.command(name="openbox")
async def cmd_openbox(ctx):
    """Open a Mystery-box."""
    if not await check_player(ctx): return
    u, db = await get_user(ctx.author.id)
    if u["items"].get("Mystery-box",0) < 1: await ctx.send("❌ No Mystery-Boxes! Craft one with `!make mystery-box`."); return
    u["items"]["Mystery-box"] -= 1
    if u["items"]["Mystery-box"] <= 0: del u["items"]["Mystery-box"]
    special = ["Golden-Wrench","Diamond-Drill","Magic-Hammer","Shield","Energy-Drink",
               "Healing-Potion","Revival-Crystal","Excalibur","Mjolnir","Infinity-Gem"]
    r = random.random()
    if r < 0.03:    sel=random.choice(special); qty=random.randint(1,2); rarity="✨ LEGENDARY"; money=random.randint(500,2000)
    elif r < 0.15:  sel=random.choice(special); qty=random.randint(1,3); rarity="💎 Rare";      money=random.randint(200,500)
    elif r < 0.8:   sel=random.choice(ALL_ITEMS); qty=random.randint(1,10); rarity="🔹 Common"; money=random.randint(50,200)
    else:
        sel=list(CRAFTABLE.values())[random.randint(0,len(CRAFTABLE)-1)]["result"]
        qty=random.randint(1,3); rarity="🌟 ULTRA RARE"; money=random.randint(100,400)
    u["money"] += money
    u["items"][sel] = u["items"].get(sel,0) + qty
    await save_user(ctx.author.id, db)
    await ctx.send(f"📦 **MYSTERY BOX OPENED!**\n{rarity}\n\n**+{qty}x {sel}**\n**+${money:,}**")

@bot.command()
async def eat(ctx):
    """Eat food to restore health."""
    if not await check_player(ctx): return
    u, db = await get_user(ctx.author.id)
    edible = [i for i in u["items"] if i in FOOD_HEALS]
    if not edible: await ctx.send("❌ No food! Buy some from the shop."); return
    lines = "\n".join(f"{i+1}. **{edible[i]}** — +{FOOD_HEALS[edible[i]]} HP" for i in range(min(10,len(edible))))
    await ctx.send(f"🍽️ **What do you want to eat?**\n\n{lines}\n\nType a number:")
    def chk(m): return m.author.id == ctx.author.id and m.content.strip().isdigit()
    try:
        r = await bot.wait_for("message", check=chk, timeout=30)
        idx = int(r.content.strip()) - 1
        if idx < 0 or idx >= len(edible): await ctx.send("❌ Invalid."); return
        food = edible[idx]
        u, db = await get_user(ctx.author.id)
        if u["items"].get(food,0) < 1: await ctx.send("❌ No longer have that food!"); return
        u["items"][food] -= 1
        if u["items"][food] <= 0: del u["items"][food]
        old_hp = u["health"]
        heal = FOOD_HEALS[food]
        u["health"] = min(10, u["health"] + heal)
        actual = u["health"] - old_hp
        await save_user(ctx.author.id, db)
        await ctx.send(f"🍽️ Ate **{food}** and recovered **{actual} HP**! Health: {u['health']}/10")
    except asyncio.TimeoutError:
        await ctx.send("⌛ Timed out.")

@bot.command()
async def heal(ctx, *, target_name: str = None):
    """Heal yourself or someone with First-Aid."""
    if not await check_player(ctx): return
    u, db = await get_user(ctx.author.id)
    if u["items"].get("First-Aid",0) < 1: await ctx.send("❌ Need First-Aid to heal!"); return
    target_id = ctx.author.id
    target_display = ctx.author.display
    if target_name:
        await ctx.send("Healing yourself (can't look up others by name in Pyrode).")
    u2, db2 = await get_user(target_id)
    u["items"]["First-Aid"] -= 1
    if u["items"]["First-Aid"] <= 0: del u["items"]["First-Aid"]
    heal_amt = 6 if u.get("married_to") and u["married_to"] == str(target_id) else 5
    old = u2["health"]; u2["health"] = min(10, u2["health"] + heal_amt)
    actual = u2["health"] - old
    db[str(ctx.author.id)] = u
    db[str(target_id)] = u2
    await _save("users.json", db)
    await ctx.send(f"💚 Healed **{target_display}** for **{actual} HP**! HP: {u2['health']}/10")

@bot.command()
async def revive(ctx):
    """Revive yourself with First-Aid."""
    u, db = await get_user(ctx.author.id)
    if u["health"] > 0: await ctx.send("❌ You're not dead!"); return
    if u["items"].get("First-Aid",0) < 1: await ctx.send("❌ Need First-Aid to revive!"); return
    u["items"]["First-Aid"] -= 1
    if u["items"]["First-Aid"] <= 0: del u["items"]["First-Aid"]
    u["health"] = 1
    await save_user(ctx.author.id, db)
    await ctx.send(f"💫 {ctx.author.display} self-revived with 1 HP!")

@bot.command()
async def health(ctx):
    """Check your health."""
    u, _ = await get_user(ctx.author.id)
    hp = u["health"]
    bar = "❤️"*max(0,hp) + "🖤"*max(0,10-hp)
    if hp <= 0: status = "💀 DEAD"
    elif hp <= 3: status = "🩸 Critical"
    elif hp <= 6: status = "⚠️ Injured"
    else: status = "✅ Healthy"
    await ctx.send(f"❤️ **{ctx.author.display}'s Health: {hp}/10**\n{bar}\n{status}")

@bot.command()
async def give(ctx, item_name: str, count: int, *, target_name: str):
    """Give items to another user. !give Sword 1 username"""
    if not await check_player(ctx): return
    if count < 1: await ctx.send("❌ At least 1 item!"); return
    u, db = await get_user(ctx.author.id)
    found = next((k for k in u["items"] if k.lower() == item_name.lower()), None)
    if not found: await ctx.send(f"❌ You don't have '{item_name}'!"); return
    if u["items"][found] < count: await ctx.send(f"❌ Only have {u['items'][found]}x {found}!"); return
    # find target by searching all users by display name - approximate via stored member list
    await ctx.send("❌ Can't look up other users by name directly in Pyrode (no member list API). Use their user ID if available.")

# ─────────────────────────────────────────────────────────────
# COMBAT
# ─────────────────────────────────────────────────────────────

async def _use_durability(uid, item, db):
    u = db.get(str(uid), {})
    items = u.get("items", {})
    if item in items:
        items[item] -= 1
        if items[item] <= 0: del items[item]

@bot.command()
async def slap(ctx, *, target_name: str):
    """Slap someone with Mickey's-Glove."""
    if not await check_player(ctx): return
    u, db = await get_user(ctx.author.id)
    if u["items"].get("Mickey's-Glove",0) < 1: await ctx.send("❌ Need Mickey's-Glove!"); return
    # find target in db by searching members
    members_data = [(uid, ud) for uid, ud in db.items() if uid != str(ctx.author.id)]
    target_entry = None
    for uid, ud in members_data:
        pass  # we can't look up display names without member API; handle gracefully
    # In Pyrode we get member list from bot.server — use message context to find @mention
    await ctx.send("💡 Tip: mention the user. Usage: Pyrode doesn't support name lookup — ping them or use `!battle`.")

# Combat commands that work on message author vs mentioned user are tricky in Pyrode
# since we can't parse @mentions. We handle the most common ones with a best-effort approach.

@bot.command()
async def duel(ctx, amount: int, *, target_name: str = "someone"):
    """Quick money duel. !duel 100"""
    if not await check_player(ctx): return
    if amount <= 0: await ctx.send("❌ Bet at least $1!"); return
    u, db = await get_user(ctx.author.id)
    if u["money"] < amount: await ctx.send(f"❌ You don't have ${amount}!"); return
    await ctx.send(
        f"⚔️ **{ctx.author.display}** challenges the channel to a **${amount:,}** duel!\n"
        f"Type `accept` within 30 seconds to accept!"
    )
    def chk(m): return m.content.strip().lower() == "accept" and m.author.id != ctx.author.id
    try:
        r = await bot.wait_for("message", check=chk, timeout=30)
        challenger = r.author
        u2, db2 = await get_user(challenger.id)
        if u2["money"] < amount: await ctx.send(f"❌ {challenger.display} doesn't have ${amount}!"); return
        winner = random.choice([ctx.author, challenger])
        loser = challenger if winner.id == ctx.author.id else ctx.author
        wu, _ = await get_user(winner.id); lu, _ = await get_user(loser.id)
        wu["money"] += amount; lu["money"] -= amount
        db[str(winner.id)] = wu; db[str(loser.id)] = lu
        await _save("users.json", db)
        await ctx.send(f"⚔️ **Duel Result!** 🏆 {winner.display} wins **${amount:,}**!")
    except asyncio.TimeoutError:
        await ctx.send("⌛ No one accepted the duel.")

@bot.command()
async def battle(ctx):
    """Challenge the channel to a turn-based battle. !battle"""
    if not await check_player(ctx): return
    await ctx.send(
        f"⚔️ **{ctx.author.display}** is looking for a battle!\n"
        f"Type `fight` within 30s to accept!"
    )
    def chk(m): return m.content.strip().lower() == "fight" and m.author.id != ctx.author.id
    try:
        r = await bot.wait_for("message", check=chk, timeout=30)
        opponent = r.author
        p1, db = await get_user(ctx.author.id)
        p2, _ = await get_user(opponent.id)
        if p1["health"] <= 0 or p2["health"] <= 0:
            await ctx.send("❌ One of you is dead!"); return
        await ctx.send(f"⚔️ **BATTLE!** {ctx.author.display} vs {opponent.display}")
        p1hp = p1["health"]; p2hp = p2["health"]
        while p1hp > 0 and p2hp > 0:
            dmg = random.randint(1,4)
            p2hp = max(0, p2hp - dmg)
            await ctx.send(f"💥 {ctx.author.display} hits for {dmg}! ({opponent.display}: {p2hp} HP)")
            if p2hp <= 0: break
            await asyncio.sleep(1)
            dmg = random.randint(1,4)
            p1hp = max(0, p1hp - dmg)
            await ctx.send(f"💥 {opponent.display} hits for {dmg}! ({ctx.author.display}: {p1hp} HP)")
            await asyncio.sleep(1)
        winner_obj = ctx.author if p2hp <= 0 else opponent
        loser_obj  = opponent if p2hp <= 0 else ctx.author
        reward = random.randint(100,200)
        wu, _ = await get_user(winner_obj.id); lu, _ = await get_user(loser_obj.id)
        wu["money"] += reward; wu["wins"] = wu.get("wins",0)+1
        wu["exp"] = wu.get("exp",0)+50
        lu["health"] = 0; lu["losses"] = lu.get("losses",0)+1
        if wu["exp"] >= wu["level"]*100:
            wu["level"] += 1; wu["exp"] = 0
            await ctx.send(f"🌟 {winner_obj.display} leveled up to Level {wu['level']}!")
        if lu.get("bounty",0) > 0:
            wu["items"]["Money-Box"] = wu["items"].get("Money-Box",0)+1
            wu.setdefault("box_amounts",[]).append(lu["bounty"])
            lu["bounty"] = 0
            await ctx.send(f"🎯 {winner_obj.display} collected the bounty!")
        db[str(winner_obj.id)] = wu; db[str(loser_obj.id)] = lu
        await _save("users.json", db)
        await ctx.send(f"🏆 **{winner_obj.display}** wins! +50 EXP +${reward}! {loser_obj.display} is knocked out.")
    except asyncio.TimeoutError:
        await ctx.send("⌛ No challenger appeared.")

# ─────────────────────────────────────────────────────────────
# SOCIAL
# ─────────────────────────────────────────────────────────────

@bot.command()
async def steal(ctx):
    """Attempt to steal from the next person who talks."""
    if not await check_player(ctx): return
    u, db = await get_user(ctx.author.id)
    await ctx.send(
        f"🤫 **{ctx.author.display}** is ready to steal! The next person to type will be pickpocketed!\n"
        f"*(Target: type anything in 19s to cancel the steal)*"
    )
    def chk(m): return m.author.id != ctx.author.id
    try:
        r = await bot.wait_for("message", check=chk, timeout=19)
        victim = r.author
        u2, _ = await get_user(victim.id)
        if u2["money"] <= 0: await ctx.send(f"❌ {victim.display} has no money!"); return
        amt = random.randint(1, max(1, u2["money"]//4))
        u["money"] += amt; u2["money"] -= amt
        u["wanted"] = min(5, u.get("wanted",0)+1)
        u["wanted_timer"] = time.time()
        db[str(ctx.author.id)] = u; db[str(victim.id)] = u2
        await _save("users.json", db)
        await ctx.send(f"💰 {ctx.author.display} stole **${amt:,}** from {victim.display}!")
    except asyncio.TimeoutError:
        await ctx.send(f"✅ Nobody showed up — {ctx.author.display} gets away clean.")

@bot.command()
async def pickpocket(ctx):
    """Attempt to pickpocket the next person who talks."""
    if not await check_player(ctx): return
    if random.random() < 0.4:
        u, db = await get_user(ctx.author.id)
        u["jail"]=1; u["jail_until"]=time.time()+60
        loss = max(0, int(u["money"]*0.25)); u["money"] -= loss
        await save_user(ctx.author.id, db)
        await ctx.send(f"🚔 {ctx.author.display} got caught! **JAILED** 60s and lost **${loss:,}**!")
    else:
        await ctx.send(f"🤏 {ctx.author.display} is going for a pickpocket! Next person to type gets pickpocketed...")
        def chk(m): return m.author.id != ctx.author.id
        try:
            r = await bot.wait_for("message", check=chk, timeout=15)
            victim = r.author
            u, db = await get_user(ctx.author.id); u2, _ = await get_user(victim.id)
            amt = random.randint(1, max(1, min(50, u2["money"])))
            u2["money"] -= amt; u["money"] += amt
            u["wanted"] = min(5, u.get("wanted",0)+1)
            db[str(ctx.author.id)] = u; db[str(victim.id)] = u2
            await _save("users.json", db)
            await ctx.send(f"🤏 {ctx.author.display} pickpocketed **${amt:,}** from {victim.display}!")
        except asyncio.TimeoutError:
            await ctx.send("Nobody around to pickpocket.")

@bot.command()
async def wanted(ctx):
    """Check your wanted level."""
    u, db = await get_user(ctx.author.id)
    now = time.time()
    decay = int((now - u.get("wanted_timer",now)) // 1800)
    if decay > 0:
        u["wanted"] = max(0, u.get("wanted",0) - decay)
        u["wanted_timer"] = now
        await save_user(ctx.author.id, db)
    w = u.get("wanted",0)
    stars = "⭐"*w + "☆"*(5-w)
    if w == 0: status = "✅ Clean record"
    elif w <= 2: status = "⚠️ Minor offender"
    elif w <= 4: status = "🚨 Dangerous criminal"
    else: status = "💀 MOST WANTED"
    await ctx.send(f"🚔 **{ctx.author.display}'s Wanted Level**\n{stars} ({w}/5)\n{status}")

@bot.command()
async def bounty(ctx):
    """Place a bounty on the channel's most wanted."""
    if not await check_player(ctx): return
    db = await _load("users.json")
    top = sorted(db.items(), key=lambda x: x[1].get("wanted",0), reverse=True)
    for uid, ud in top:
        if ud.get("wanted",0) > 0 and uid != str(ctx.author.id):
            w = ud["wanted"]
            bounty_range = {1:(50,200),2:(200,500),3:(500,1000),4:(1000,2500),5:(2500,5000)}
            lo,hi = bounty_range.get(w,(50,200))
            amt = random.randint(lo,hi)
            ud["bounty"] = ud.get("bounty",0) + amt
            await _save("users.json", db)
            await ctx.send(f"🎯 **BOUNTY PLACED!** ${amt:,} on <@{uid}> ({'⭐'*w}) — knock them out to collect a Money-Box!")
            return
    await ctx.send("❌ No wanted players to bounty!")

@bot.command()
async def marry(ctx):
    """Propose marriage to the next person who types 'yes'."""
    if not await check_player(ctx): return
    u, db = await get_user(ctx.author.id)
    if u.get("married_to"): await ctx.send("❌ Already married! Use `!divorce` first."); return
    await ctx.send(f"💍 **{ctx.author.display}** is proposing! Type `yes` to accept within 30s!")
    def chk(m): return m.content.strip().lower() == "yes" and m.author.id != ctx.author.id
    try:
        r = await bot.wait_for("message", check=chk, timeout=30)
        partner = r.author
        u2, _ = await get_user(partner.id)
        if u2.get("married_to"): await ctx.send(f"❌ {partner.display} is already married!"); return
        u["married_to"] = str(partner.id); u2["married_to"] = str(ctx.author.id)
        db[str(ctx.author.id)] = u; db[str(partner.id)] = u2
        await _save("users.json", db)
        await ctx.send(f"🎉 {ctx.author.display} and {partner.display} are married! 💑")
    except asyncio.TimeoutError:
        await ctx.send("💔 Nobody accepted the proposal.")

@bot.command()
async def divorce(ctx):
    """Divorce your current partner."""
    u, db = await get_user(ctx.author.id)
    if not u.get("married_to"): await ctx.send("❌ You're not married!"); return
    partner_id = u["married_to"]
    u["married_to"] = None
    if partner_id in db: db[partner_id]["married_to"] = None
    await _save("users.json", db)
    await ctx.send(f"💔 {ctx.author.display} filed for divorce.")

@bot.command()
async def hug(ctx):
    """Hug the next person who talks."""
    responses = ["🤗 {a} gives {b} a warm hug!","💛 {a} wraps {b} in a bear hug!","🫂 {a} hugs {b} tightly!"]
    def chk(m): return m.author.id != ctx.author.id
    try:
        r = await bot.wait_for("message", check=chk, timeout=15)
        await ctx.send(random.choice(responses).format(a=ctx.author.display, b=r.author.display))
    except asyncio.TimeoutError:
        await ctx.send(f"🤗 {ctx.author.display} hugs the air... nobody was there.")

@bot.command()
async def kiss(ctx):
    """Kiss the next person who talks."""
    responses = ["💋 {a} kisses {b}!","😘 {a} gives {b} a kiss on the cheek!","💏 {a} and {b} share a kiss!"]
    def chk(m): return m.author.id != ctx.author.id
    try:
        r = await bot.wait_for("message", check=chk, timeout=15)
        await ctx.send(random.choice(responses).format(a=ctx.author.display, b=r.author.display))
    except asyncio.TimeoutError:
        await ctx.send("Nobody to kiss...")

@bot.command()
async def ship(ctx):
    """Ship yourself with the next person who talks."""
    def chk(m): return m.author.id != ctx.author.id
    try:
        r = await bot.wait_for("message", check=chk, timeout=15)
        score = random.randint(0,100)
        bar = "❤️"*(score//10) + "🖤"*(10-score//10)
        if score>=80: verdict="💞 Soulmates!"
        elif score>=60: verdict="💕 Great match!"
        elif score>=40: verdict="🤔 Could work..."
        elif score>=20: verdict="😬 Unlikely..."
        else: verdict="💀 Never gonna happen"
        await ctx.send(f"💘 **{ctx.author.display}** + **{r.author.display}**\n\n{bar}\n**{score}% compatible!** {verdict}")
    except asyncio.TimeoutError:
        await ctx.send("Nobody to ship with...")

# ─────────────────────────────────────────────────────────────
# FUN
# ─────────────────────────────────────────────────────────────

@bot.command()
async def gaymeter(ctx):
    """Measure how gay you are."""
    pct = random.randint(0,100)
    bar = "🏳️‍🌈"*(pct//5) + "⬜"*(20-pct//5)
    await ctx.send(f"🌈 **Gay Meter**\n{ctx.author.display} is **{pct}% Gay!**\n`{bar}`")

@bot.command()
async def rizzmeter(ctx):
    """Measure your rizz."""
    pct = random.randint(0,100)
    bar = "😎"*(pct//5) + "⬜"*(20-pct//5)
    await ctx.send(f"😎 **Rizz Meter**\n{ctx.author.display} has **{pct}% Rizz!**\n`{bar}`")

@bot.command()
async def iq(ctx):
    """Measure your IQ."""
    score = random.randint(1,200)
    if score<70: v="💀 Certified brainrot"
    elif score<100: v="😐 Below average"
    elif score<130: v="✅ Average"
    elif score<160: v="🌟 Above average"
    else: v="🧬 Galaxy brain"
    await ctx.send(f"🧠 **IQ Test**\n{ctx.author.display}'s IQ is **{score}**! {v}")

@bot.command()
async def coinflip(ctx):
    """Flip a coin."""
    await ctx.send(f"🪙 **Coin Flip:** {'Heads' if random.random() < 0.5 else 'Tails'}!")

@bot.command()
async def roll(ctx, sides: int = 6):
    """Roll a die. !roll 20"""
    if sides < 2: await ctx.send("❌ At least 2 sides!"); return
    await ctx.send(f"🎲 **D{sides} Roll:** You rolled a **{random.randint(1,sides)}**!")

@bot.command()
async def roast(ctx):
    """Roast the next person who talks."""
    roasts = [
        "{t} you're the reason they put instructions on shampoo bottles.",
        "{t} I'd roast you but my mom said I'm not allowed to burn trash.",
        "{t} you have your whole life to be an idiot. Take the day off.",
        "{t} I've seen better heads on a pimple.",
        "{t} some day you'll go far. I hope you stay there.",
        "{t} you have the same energy as a participation trophy.",
        "{t} you're proof that even evolution can go backwards.",
        "{t} I'd call you a tool but that implies you're at least useful.",
    ]
    def chk(m): return m.author.id != ctx.author.id
    try:
        r = await bot.wait_for("message", check=chk, timeout=20)
        await ctx.send(random.choice(roasts).format(t=r.author.display))
    except asyncio.TimeoutError:
        await ctx.send("Nobody to roast!")

@bot.command(name="8ball")
async def eightball(ctx, *, question: str = "?"):
    """Ask the magic 8-ball. !8ball will I win"""
    responses = [
        "🎱 It is certain.","🎱 Without a doubt.","🎱 Yes definitely.",
        "🎱 Most likely.","🎱 Outlook good.","🎱 Signs point to yes.",
        "🎱 Reply hazy, try again.","🎱 Ask again later.",
        "🎱 Don't count on it.","🎱 My reply is no.","🎱 Very doubtful.",
    ]
    await ctx.send(f"🎱 **Q:** {question}\n**A:** {random.choice(responses)}")

# ─────────────────────────────────────────────────────────────
# MISC / INFO
# ─────────────────────────────────────────────────────────────

@bot.command()
async def ping(ctx):
    """Check bot latency."""
    await ctx.send("🏓 Pong! Nessie is alive and well.")

@bot.command()
async def credits(ctx):
    """Show bot credits."""
    await ctx.send(
        "🎉 **Nessie Bot Credits**\n\n"
        "👑 **Aadamgaming (Hoover CEO)** — Code, Commands\n"
        "💡 **SSILP** — Idea and some commands\n"
        "📛 **Ivo** — The new name of the bot\n"
        "🥇 **Elite** — First bot user\n"
        "🛠️ **Toodles** — Old bot, started with it\n\n"
        "*Ported to Nullchat Pyrode*"
    )

@bot.command()
async def toodles(ctx):
    """Memorial for Toodles."""
    await ctx.send(
        "🛠️ **In Memory of Toodles**\n\n"
        "*Toodles — The original bot.*\n*2025 - 2025*\n\nRest easy. Nessie carries your legacy."
    )

@bot.command()
async def userinfo(ctx):
    """Show your game stats."""
    u, _ = await get_user(ctx.author.id)
    hp = u["health"]; w = u.get("wanted",0)
    stars = "⭐"*w + "☆"*(5-w)
    jail_str = ""
    if u.get("jail") and time.time() < u.get("jail_until",0):
        jail_str = f"\n🔒 In Jail ({int(u['jail_until']-time.time())}s)"
    married = f"\n💍 Married to <@{u['married_to']}>" if u.get("married_to") else ""
    await ctx.send(
        f"👤 **{ctx.author.display}**\n"
        f"❤️ Health: {hp}/10 | 💰 Money: ${u['money']:,}\n"
        f"⭐ Level {u['level']} | EXP: {u['exp']}\n"
        f"🏆 Wins: {u['wins']} | Losses: {u['losses']}\n"
        f"🚔 Wanted: {stars}\n"
        f"💪 Strength: {u.get('strength',0)}"
        f"{jail_str}{married}"
    )

@bot.command()
async def stats(ctx):
    """Alias for userinfo."""
    await userinfo(ctx)

@bot.command()
async def nessiehelp(ctx, *, cmd: str = None):
    """Show all commands."""
    await ctx.send(
        "🐉 **Nessie Commands** (prefix: `!`)\n\n"
        "💰 **Economy:** `balance` `work` `daily` `pay` `shop` `buy` `sell` `leaderboard`\n"
        "🎒 **Items:** `items` `inspect` `craftlist` `make` `enchant` `give` `eat` `heal` `revive` `health`\n"
        "📦 **Boxes:** `makebox` `open` `openbox`\n"
        "⚔️ **Combat:** `battle` `duel`\n"
        "🔒 **Crime:** `steal` `pickpocket` `wanted` `bounty`\n"
        "💑 **Social:** `marry` `divorce` `hug` `kiss` `ship`\n"
        "🎉 **Fun:** `gaymeter` `rizzmeter` `iq` `coinflip` `roll` `roast` `8ball`\n"
        "🏠 **Homes:** `home` `home make` `home invite` `home kick` `home leave` `home sell` `home name` `home upgrade` `home deposit` `home buyprop` `home props` `nukehouse`\n"
        "💪 **Strength:** `workout` `strength`\n"
        "📊 **Info:** `userinfo` `stats` `ping` `credits` `toodles`\n"
        "🔧 **Admin:** `setmoney` `sethealth` `jailuser` `bypass`\n\n"
        "Use `!nessiehelp <command>` for details on any command.\n"
        "-# Nessie by Hoover Creations | Pyrode port"
    )

@bot.command()
async def bypass(ctx, action: str = None, item: str = None, amount: int = 1, *, target_name: str = ""):
    """Admin: give/remove items. !bypass give Sword 1"""
    if str(ctx.author.id) not in ADMIN_IDS: await ctx.send("❌ Not allowed."); return
    if not action or action not in ["give","remove"] or not item:
        await ctx.send("Usage: `!bypass give/remove ItemName amount`"); return
    u, db = await get_user(ctx.author.id)
    if action == "give":
        u["items"][item] = u["items"].get(item,0) + max(amount,1)
        await save_user(ctx.author.id, db)
        await ctx.send(f"✅ Granted **{amount}x {item}** to yourself.")
    elif action == "remove":
        if u["items"].get(item,0) <= 0: await ctx.send(f"❌ You don't have {item}."); return
        u["items"][item] = max(0, u["items"].get(item,0) - max(amount,1))
        if u["items"][item] == 0: del u["items"][item]
        await save_user(ctx.author.id, db)
        await ctx.send(f"✅ Removed **{amount}x {item}**.")

# ─────────────────────────────────────────────────────────────
# ADMIN
# ─────────────────────────────────────────────────────────────

@bot.command()
async def setmoney(ctx, amount: int):
    """Admin: set your money. !setmoney 10000"""
    if str(ctx.author.id) not in ADMIN_IDS: return
    u, db = await get_user(ctx.author.id)
    u["money"] = amount
    await save_user(ctx.author.id, db)
    await ctx.send(f"✅ Set money to ${amount:,}")

@bot.command()
async def sethealth(ctx, amount: int):
    """Admin: set your health. !sethealth 10"""
    if str(ctx.author.id) not in ADMIN_IDS: return
    u, db = await get_user(ctx.author.id)
    u["health"] = amount
    await save_user(ctx.author.id, db)
    await ctx.send(f"✅ Set health to {amount}")

@bot.command()
async def jailuser(ctx, seconds: int):
    """Admin: jail yourself for testing. !jailuser 60"""
    if str(ctx.author.id) not in ADMIN_IDS: return
    u, db = await get_user(ctx.author.id)
    u["jail"]=1; u["jail_until"]=time.time()+seconds
    await save_user(ctx.author.id, db)
    await ctx.send(f"✅ Jailed for {seconds}s")

# ─────────────────────────────────────────────────────────────
# HOMES
# ─────────────────────────────────────────────────────────────

@bot.command()
async def home(ctx, subcommand: str = None, *, args: str = ""):
    """Home management. !home, !home make, !home invite, etc."""
    sub = (subcommand or "").lower()

    if not sub or sub == "show":
        h, homes = await get_home(ctx.author.id)
        if not h: await ctx.send("🏠 No home! Use `!home make` to create one."); return
        members = [m for m in h.get("members","").split(",") if m]
        props = [p for p in h.get("properties","").split(",") if p]
        member_pings = " ".join(f"<@{m}>" for m in members[:10])
        prop_text = ", ".join(f"{PROPERTIES.get(p,{}).get('emoji','🏠')} {p}" for p in props) or "None"
        await ctx.send(
            f"🏠 **{h['name']}**\n"
            f"Owner: <@{h['owner']}> | Money: ${h.get('money',0):,}\n"
            f"Capacity: {len(members)}/{h.get('capacity_max',5)}\n"
            f"Members: {member_pings or 'None'}\n"
            f"Properties: {prop_text}"
        )

    elif sub == "make":
        if not await check_player(ctx): return
        u, db = await get_user(ctx.author.id)
        if u["money"] < 349000: await ctx.send(f"❌ Need $349,000! You have ${u['money']:,}"); return
        existing, _ = await get_home(ctx.author.id)
        if existing: await ctx.send("❌ Already in a home! Leave first."); return
        hid = f"home_{ctx.author.id}_{int(time.time())}"
        homes = await _load("homes.json")
        homes[hid] = {"id":hid,"name":f"{ctx.author.display}'s Home","owner":str(ctx.author.id),
                      "money":0,"capacity_max":5,"members":str(ctx.author.id),"properties":""}
        await save_homes(homes)
        u["money"] -= 349000
        await save_user(ctx.author.id, db)
        await ctx.send(f"🏠 **Home Created!** Capacity: 5 members. Invite with `!home invite username`.")

    elif sub == "invite":
        if not await check_player(ctx): return
        h, homes = await get_home(ctx.author.id)
        if not h or h["owner"] != str(ctx.author.id): await ctx.send("❌ You don't own a home!"); return
        members = [m for m in h.get("members","").split(",") if m]
        if len(members) >= h.get("capacity_max",5): await ctx.send("❌ Home is full!"); return
        await ctx.send("The next person to type will be invited to your home. (30s)")
        def chk(m): return m.author.id != ctx.author.id
        try:
            r = await bot.wait_for("message", check=chk, timeout=30)
            target_id = str(r.author.id)
            if target_id in members: await ctx.send(f"❌ {r.author.display} is already a member!"); return
            existing2, _ = await get_home(r.author.id)
            if existing2: await ctx.send(f"❌ {r.author.display} is already in another home!"); return
            members.append(target_id)
            h["members"] = ",".join(members)
            await save_homes(homes)
            await ctx.send(f"✅ {r.author.display} invited to **{h['name']}**!")
        except asyncio.TimeoutError:
            await ctx.send("⌛ Timed out.")

    elif sub == "leave":
        if not await check_player(ctx): return
        h, homes = await get_home(ctx.author.id)
        if not h: await ctx.send("❌ Not in a home!"); return
        if h["owner"] == str(ctx.author.id): await ctx.send("❌ You're the owner! Use `!home sell`."); return
        members = [m for m in h.get("members","").split(",") if m]
        share = h.get("money",0)//len(members) if members else 0
        members = [m for m in members if m != str(ctx.author.id)]
        h["members"] = ",".join(members); h["money"] = h.get("money",0) - share
        await save_homes(homes)
        if share > 0:
            u, db = await get_user(ctx.author.id); u["money"] += share
            await save_user(ctx.author.id, db)
        await ctx.send(f"👋 Left the home and received ${share:,}.")

    elif sub == "sell":
        if not await check_player(ctx): return
        h, homes = await get_home(ctx.author.id)
        if not h or h["owner"] != str(ctx.author.id): await ctx.send("❌ You don't own a home!"); return
        await ctx.send("⚠️ Sell your home? Type `yes` to confirm:")
        def chk(m): return m.author.id == ctx.author.id
        try:
            r = await bot.wait_for("message", check=chk, timeout=30)
            if r.content.strip().lower() != "yes": await ctx.send("❌ Cancelled."); return
            members = [m for m in h.get("members","").split(",") if m]
            share = h.get("money",0)//len(members) if members else 0
            if share > 0:
                db = await _load("users.json")
                for mid in members:
                    if mid: db.setdefault(mid,{})["money"] = db.get(mid,{}).get("money",0) + share
                await _save("users.json", db)
            del homes[h["id"]]
            await save_homes(homes)
            await ctx.send(f"🏠 Home sold! Each member received ${share:,}.")
        except asyncio.TimeoutError:
            await ctx.send("⌛ Timed out.")

    elif sub == "name":
        if not await check_player(ctx): return
        h, homes = await get_home(ctx.author.id)
        if not h or h["owner"] != str(ctx.author.id): await ctx.send("❌ You don't own a home!"); return
        if not args: await ctx.send("Usage: `!home name NewName`"); return
        if len(args) > 32: await ctx.send("❌ Name max 32 chars."); return
        h["name"] = args
        await save_homes(homes)
        await ctx.send(f"✅ Home renamed to **{args}**!")

    elif sub == "upgrade":
        if not await check_player(ctx): return
        u, db = await get_user(ctx.author.id)
        if u["money"] < 50000: await ctx.send(f"❌ Need $50,000!"); return
        h, homes = await get_home(ctx.author.id)
        if not h or h["owner"] != str(ctx.author.id): await ctx.send("❌ You don't own a home!"); return
        h["capacity_max"] = h.get("capacity_max",5) + 1
        await save_homes(homes)
        u["money"] -= 50000
        await save_user(ctx.author.id, db)
        await ctx.send(f"✅ Home upgraded! New capacity: {h['capacity_max']}")

    elif sub == "deposit":
        if not await check_player(ctx): return
        try: amount = int(args)
        except: await ctx.send("Usage: `!home deposit 1000`"); return
        if amount < 1: await ctx.send("❌ At least $1!"); return
        u, db = await get_user(ctx.author.id)
        if u["money"] < amount: await ctx.send(f"❌ Only have ${u['money']:,}!"); return
        h, homes = await get_home(ctx.author.id)
        if not h: await ctx.send("❌ Not in a home!"); return
        h["money"] = h.get("money",0) + amount
        u["money"] -= amount
        await save_homes(homes)
        await save_user(ctx.author.id, db)
        await ctx.send(f"💰 Deposited ${amount:,}! Home balance: ${h['money']:,}")

    elif sub == "buyprop":
        if not await check_player(ctx): return
        if not args:
            lines = [f"{d['emoji']} **{p}** — ${d['cost']:,}: {d['desc']}" for p,d in PROPERTIES.items()]
            await ctx.send("🏠 **Available Properties**\n\n" + "\n".join(lines) + "\n\nUse `!home buyprop PropertyName`")
            return
        matched = next((p for p in PROPERTIES if args.lower() in p.lower()), None)
        if not matched:
            lines = [f"{d['emoji']} **{p}** — ${d['cost']:,}" for p,d in PROPERTIES.items()]
            await ctx.send("❌ Property not found.\n\n" + "\n".join(lines)); return
        h, homes = await get_home(ctx.author.id)
        if not h or h["owner"] != str(ctx.author.id): await ctx.send("❌ You don't own a home!"); return
        props = [p for p in h.get("properties","").split(",") if p]
        if matched in props: await ctx.send(f"❌ Already own {matched}!"); return
        cost = PROPERTIES[matched]["cost"]
        u, db = await get_user(ctx.author.id)
        if u["money"] < cost: await ctx.send(f"❌ Need ${cost:,}!"); return
        props.append(matched); h["properties"] = ",".join(props)
        await save_homes(homes)
        u["money"] -= cost
        await save_user(ctx.author.id, db)
        if matched == "Bodyguard-Deployer":
            u["bodyguard"] = PROPERTIES[matched]["bodyguard_hp"]
            await save_user(ctx.author.id, db)
        await ctx.send(f"✅ Purchased **{matched}** for ${cost:,}!")

    elif sub == "props":
        lines = [f"{d['emoji']} **{p}** — ${d['cost']:,}: {d['desc']}" for p,d in PROPERTIES.items()]
        await ctx.send("🏠 **Available Properties**\n\n" + "\n".join(lines))

    elif sub == "kick":
        if not await check_player(ctx): return
        h, homes = await get_home(ctx.author.id)
        if not h or h["owner"] != str(ctx.author.id): await ctx.send("❌ You don't own a home!"); return
        await ctx.send("The next person to type will be kicked from your home. (20s)")
        def chk(m): return m.author.id != ctx.author.id
        try:
            r = await bot.wait_for("message", check=chk, timeout=20)
            members = [m for m in h.get("members","").split(",") if m]
            target_id = str(r.author.id)
            if target_id not in members: await ctx.send(f"❌ {r.author.display} is not in your home!"); return
            share = h.get("money",0)//len(members) if members else 0
            members = [m for m in members if m != target_id]
            h["members"] = ",".join(members); h["money"] = h.get("money",0) - share
            await save_homes(homes)
            if share > 0:
                u2, db2 = await get_user(r.author.id); u2["money"] += share
                await save_user(r.author.id, db2)
            await ctx.send(f"👋 Kicked {r.author.display}. They received ${share:,}.")
        except asyncio.TimeoutError:
            await ctx.send("⌛ Timed out.")
    else:
        await ctx.send("Unknown subcommand. Use `!nessiehelp` for help.")

@bot.command()
async def nukehouse(ctx):
    """Launch a nuclear strike on the channel's most-homed target. Requires Nuclear-Bomb + Launching-Facility."""
    if not await check_player(ctx): return
    u, db = await get_user(ctx.author.id)
    if u["items"].get("Nuclear-Bomb",0) < 1: await ctx.send("❌ Need a Nuclear-Bomb! ($12,000,000)"); return
    my_home, homes = await get_home(ctx.author.id)
    if not my_home or "Launching-Facility" not in my_home.get("properties",""):
        await ctx.send("❌ Need a Launching Facility in your home!"); return
    # Find another home to nuke
    other_homes = [h for hid,h in homes.items() if h["owner"] != str(ctx.author.id)]
    if not other_homes: await ctx.send("❌ No other homes to nuke!"); return
    target_home = random.choice(other_homes)
    u["items"]["Nuclear-Bomb"] -= 1
    if u["items"]["Nuclear-Bomb"] <= 0: del u["items"]["Nuclear-Bomb"]
    await save_user(ctx.author.id, db)
    target_members = [m for m in target_home.get("members","").split(",") if m]
    has_bank = "Bank" in target_home.get("properties","")
    userdb = await _load("users.json")
    hit_list = []
    for mid in target_members:
        if mid:
            userdb.setdefault(mid,{})
            userdb[mid]["health"] = max(-39, userdb[mid].get("health",10) - 39)
            hit_list.append(f"<@{mid}>")
    if not has_bank:
        target_home["money"] = 0
        await save_homes(homes)
    await _save("users.json", userdb)
    victims = " ".join(hit_list[:5])
    await ctx.send(
        f"☢️ **NUCLEAR STRIKE!**\n\n"
        f"Target: **{target_home['name']}**\n"
        f"Damage: -39 HP to all members\n"
        f"Bank: {'✅ Protected' if has_bank else '❌ Money destroyed'}\n"
        f"Victims: {victims or 'nobody home'}"
    )

# ─────────────────────────────────────────────────────────────
# STRENGTH / WORKOUT
# ─────────────────────────────────────────────────────────────

@bot.command()
async def workout(ctx):
    """Workout to gain strength — find the matching emoji."""
    if not await check_player(ctx): return
    uid = str(ctx.author.id)
    now = time.time()
    if uid in _workout_cd and now - _workout_cd[uid] < 600:
        rem = int(600 - (now - _workout_cd[uid]))
        await ctx.send(f"💪 Recovering! Wait {rem//60}m {rem%60}s."); return
    target_emoji = random.choice(WORKOUT_EMOJIS)
    grid = [random.choice(WORKOUT_EMOJIS) for _ in range(9)]
    grid[4] = target_emoji
    rows = [" ".join(grid[i:i+3]) for i in range(0,9,3)]
    await ctx.send(
        f"💪 **WORKOUT!** Find **{target_emoji}** and type its position (1-9)!\n\n"
        + "\n".join(rows) +
        "\n\nPositions:\n1 2 3\n4 5 6\n7 8 9\n\nYou have 15 seconds!"
    )
    def chk(m): return m.author.id == ctx.author.id and m.content.strip().isdigit() and 1 <= int(m.content.strip()) <= 9
    try:
        r = await bot.wait_for("message", check=chk, timeout=15)
        pos = int(r.content.strip()) - 1
        if grid[pos] == target_emoji:
            u, db = await get_user(ctx.author.id)
            h, _ = await get_home(ctx.author.id)
            gym_bonus = 2 if h and "Gym" in h.get("properties","") else 0
            gain = random.randint(1,3) + gym_bonus
            u["strength"] = u.get("strength",0) + gain
            await save_user(ctx.author.id, db)
            _workout_cd[uid] = now
            sname,_,_,_ = strength_info(u["strength"])
            await ctx.send(f"✅ **Workout success!** +{gain} strength! Total: {u['strength']} — {sname}")
        else:
            correct = grid.index(target_emoji) + 1
            await ctx.send(f"❌ Wrong! Correct position was {correct}.")
    except asyncio.TimeoutError:
        await ctx.send("⌛ Too slow!")

@bot.command()
async def strength(ctx):
    """Check your strength level."""
    u, _ = await get_user(ctx.author.id)
    s = u.get("strength",0)
    name,bb,rb,pp = strength_info(s)
    filled = min(20, int((s/50)*20))
    bar = "█"*filled + "░"*(20-filled)
    await ctx.send(
        f"💪 **{ctx.author.display}'s Strength**\n"
        f"Level: {name} | Points: {s}/50\n"
        f"`{bar}`\n"
        f"Battle bonus: +{bb} dmg | Rob bonus: +{rb}% | Pickpocket defense: -{pp}%"
    )

