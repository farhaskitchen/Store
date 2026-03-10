import pyrode
import json

bot = pyrode.Bot()

async def get_state():
    raw = await bot.files.read("state.json")
    if raw is None:
        return {"count": 0, "last_user_id": None, "high_score": 0}
    return json.loads(raw)

async def set_state(count, user_id, high_score):
    data = {
        "count": count, 
        "last_user_id": user_id, 
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
        last_user = state["last_user_id"]
        high_score = state["high_score"]

        # 1. Anti-Spam Check
        if message.author.id == last_user:
            await set_state(0, None, high_score)
            await message.add_reaction("🚫")
            await message.reply(f"Double counting! Reset to 1. (High Score: **{high_score}**)")
            return

        # 2. Correct Number Check
        if num == count + 1:
            new_count = num
            # Update high score if broken
            if new_count > high_score:
                high_score = new_count
                await message.add_reaction("👑") # New Record!
            
            await set_state(new_count, message.author.id, high_score)
            await message.add_reaction("✅")
        else:
            # 3. Wrong Number - Reset
            await set_state(0, None, high_score)
            await message.add_reaction("❌")
            await message.reply(f"Wrong! Reset to 1. The High Score remains **{high_score}**.")
            
    except ValueError:
        # Ignore non-numbers
        pass
