import pyrode

bot = pyrode.Bot() # No prefix needed if it's a pure counting bot
count = 0          # This tracks the current number in the sequence

@bot.event
async def on_message(message):
    # 1. Ignore the bot's own messages to avoid infinite loops
    if message.author.is_bot:
        return

    global count
    
    try:
        # 2. Convert the message content to an integer
        # .strip() removes any accidental spaces
        num = int(message.content.strip())

        # 3. Check if the number is correct
        if num == count + 1:
            count += 1
            await message.add_reaction("✅")
        else:
            # 4. Reset on failure
            count = 0
            await message.add_reaction("❌")
            await message.reply(f"Wrong number! The count has been reset. Next number is **1**.")
            
    except ValueError:
        # 5. Handle non-number messages (optional: delete or warn)
        await message.reply("Please only send numbers in this channel!")
