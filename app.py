import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.members = True 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print("✅ Slash-команды синхронизированы.")
    except Exception as e:
        print(f"Ошибка при синхронизации: {e}")

    print(f"🤖 Бот запущен как {bot.user}")

@bot.tree.command(name="reset", description="Сбросить никнеймы 'ЧЕ С ЕБАЛОМ?' до стандартных")
@app_commands.checks.has_permissions(manage_nicknames=True)
async def reset_nicknames(interaction: discord.Interaction):
    await interaction.response.send_message("🔄 Начинаю сброс никнеймов...", ephemeral=True)

    count = 0
    for member in interaction.guild.members:
        if member.nick == "ЧЕ С ЕБАЛОМ?": #Тут ник, который у участников всех, и он это слово на обычный ник юзера
            try:
                await member.edit(nick=None, reason="Неприемлемый никнейм")
                print(f"🟢 Сброшен ник: {member.name}#{member.discriminator}")
                count += 1
            except discord.Forbidden:
                print(f"🔴 Нет прав изменить ник: {member.name}#{member.discriminator}")
            except Exception as e:
                print(f"⚠️ Ошибка с {member.name}: {e}")

    await interaction.followup.send(f"✅ Сброшено никнеймов: {count}")

@reset_nicknames.error
async def reset_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("❌ У тебя нет прав на управление никнеймами.", ephemeral=True)
    else:
        await interaction.response.send_message(f"⚠️ Ошибка: {error}", ephemeral=True)

bot.run("СЮДА ТОКЕН БОТА") #токен бота сюда