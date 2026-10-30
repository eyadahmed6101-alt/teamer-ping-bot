import discord
from discord import app_commands
from discord.ext import commands

# ----------------- Settings -----------------
TARGET_CHANNEL_ID = 1562744636890423378  # حط هنا ID الروم بتاعتك
TEAMER_ROLE_ID = 1565070098215993455     # حط هنا ID رتبة teamer ping
# --------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class RequestModal(discord.ui.Modal, title="Submit a New Request"):
    
    vs_input = discord.ui.TextInput(
        label="VS",
        placeholder="Enter VS details here...",
        style=discord.TextStyle.short,
        required=True
    )
    
    user_input = discord.ui.TextInput(
        label="User",
        placeholder="Enter username...",
        style=discord.TextStyle.short,
        required=True
    )
    
    code_input = discord.ui.TextInput(
        label="Code Server",
        placeholder="Enter server code...",
        style=discord.TextStyle.short,
        required=True
    )
    
    link_input = discord.ui.TextInput(
        label="Link Server",
        placeholder="Enter server link...",
        style=discord.TextStyle.short,
        required=True
    )

    def __init__(self, bot_message):
        super().__init__()
        self.bot_message = bot_message

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Your request has been sent successfully!", ephemeral=True)
        
        # إرسال الطلب النهائي في الروم
        embed = discord.Embed(
            title="New Request 📝",
            color=discord.Color.blue()
        )
        embed.add_field(name="Requested By", value=interaction.user.mention, inline=False)
        embed.add_field(name="1. VS", value=self.vs_input.value, inline=False)
        embed.add_field(name="2. User", value=self.user_input.value, inline=False)
        embed.add_field(name="3. Code Server", value=self.code_input.value, inline=False)
        embed.add_field(name="4. Link Server", value=self.link_input.value, inline=False)

        teamer_mention = f"<@&{TEAMER_ROLE_ID}>"
        await interaction.channel.send(content=f"{teamer_mention} - New request from {interaction.user.mention}", embed=embed)

        # مسح رسالة البوت اللي فيها الزرار نهائياً بعد إرسال الطلب
        try:
            await self.bot_message.delete()
        except:
            pass

@bot.event
async def on_ready():
    print(f'Bot is online as: {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == TARGET_CHANNEL_ID and bot.user in message.mentions:
        user_id = message.author.id

        class OpenModalView(discord.ui.View):
            def __init__(self, bot_msg):
                super().__init__(timeout=60)
                self.bot_msg = bot_msg

            @discord.ui.button(label="Click here to fill out the form 📝", style=discord.ButtonStyle.primary)
            async def open_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != user_id:
                    await interaction.response.send_message("This button is only for the person who requested the bot!", ephemeral=True)
                    return
                # تمرير رسالة البوت للـ Modal عشان تتقفل وتتمسح
                await interaction.response.send_modal(RequestModal(self.bot_msg))

            async def on_timeout(self):
                # لو خلص الوقت وما ضغطش، الزرار بيتلغي أو الرسالة ممكن تتمسح
                try:
                    await self.bot_msg.delete()
                except:
                    pass

        # إرسال رسالة البوت وحفظها في متغير عشان نعرف نتحكم فيها ونمسحها
        sent_message = await message.channel.send(
            content=f"Hello {message.author.mention}, click the button below to fill out your request:",
            view=None
        )
        # تحديث الرسالة وإضافة الزار ليها بعد إرسالها
        await sent_message.edit(view=OpenModalView(sent_message))

    await bot.process_commands(message)

import os
# باقي الكود...
bot.run(os.getenv('MTU2NTcxNTIyMjA3NTgwMTYxMA.GcMDmK.5jk_eDhO2OsN-XxmACncwm42Ix6zQsr7pZKN3E'))