import pyrode
import json

bot = pyrode.Bot()

async def get_state():
    raw = await bot.files.read("state.json")
    if raw is None:
        return {"count": 0, "high_score": 0}
    return json.loads(raw)

async def set_state(count, high_score):
    data = {
        "count": count, 
        "high_score": high_score
    }
    await bot.files.write("state.json", json.dumps(data))

@bot.event
async def on_message(message):
    if message.author.is_bot:
        return

    try:
        num = int(message.content.strip())
        state = await get_state()
        
        count = state["count"]
        high_score = state["high_score"]

        # Correct Number Check
        if num == count + 1:
            new_count = num
            if new_count > high_score:
                high_score = new_count
                await message.add_reaction("👑") # New Record!
            
            await set_state(new_count, high_score)
            await message.add_reaction("✅")
        else:
            # Wrong Number - Reset
            await set_state(0, high_score)
            await message.add_reaction("❌")
            await message.reply(f"Wrong! Reset to 1. The High Score remains **{high_score}**.")
            
    except ValueError:
        # Ignore non-numbers
        pass
