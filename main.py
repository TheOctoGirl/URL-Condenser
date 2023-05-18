import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
import url_gen
import re

intent = nextcord.Intents.default()
bot = commands.Bot(intents=intent)

@bot.event
async def on_ready():
    game = nextcord.Activity(name="for /url")
    await bot.change_presence(status=nextcord.ActivityType.watching,activity=game)
    print(f"We have logged in as {bot.user}")

@bot.slash_command()
async def url(interaction: nextcord.Interaction):
    pass

@url.subcommand(description="Shorten a URL and optionally generate a QR code for it")
async def generate(interaction: nextcord.Interaction, url: str = SlashOption(description="The URL to shorten. Note the URL must include the http:// or https://", required=True), qr_code: str = SlashOption(description="Whether to generate a QR code for the shortened URL",choices=["yes", "no"], required=True)):
    if re.match(r".*[\'\"].*", url):
        await interaction.send("You entered an invalid URL")
    else:    
        if url.startswith("http://") or url.startswith("https://"):
            try:
                if qr_code == "yes":
                    short_url = url_gen.shorten(url)
                    qr_code = url_gen.qr_code(short_url)
                    await interaction.send(f"Shortened URL: {short_url}", file=nextcord.File("qr_code.png"))

                else:
                    short_url = url_gen.shorten(url)
                    await interaction.send(f"Shortened URL: {short_url}")
            
            except url_gen.InvalidURLError:
                await interaction.send("You entered an invalid URL")
            
            except url_gen.RateLimitError:
                await interaction.send("The URL shortener is currently rate limited. Please try again later.")
            
            except url_gen.UnknownError:
                await interaction.send("An unknown error occurred. Please try again later.")
        else:
            await interaction.send("Please include http:// or https:// in your URL")


@url.subcommand(description="Unshorten a URL")
async def unshorten(interaction: nextcord.Interaction, url: str = SlashOption(description="The URL to unshorten", required=True)):
    if re.match(r".*[\'\"].*", url):
        await interaction.send("You entered an invalid URL")
    else:    
        if url.startswith("http://") or url.startswith("https://"):
            try:
                unshortened_url = url_gen.unshorten(url)
                await interaction.send(f"Unshortened URL: {unshortened_url}")
            
            except url_gen.InvalidURLError:
                await interaction.send("You entered an invalid URL")
            
            except url_gen.RateLimitError:
                await interaction.send("The URL shortener is currently rate limited. Please try again later.")
            
            except url_gen.UnknownError:
                await interaction.send("An unknown error occurred. Please try again later.")
        else:
            await interaction.send("Please include http:// or https:// in your URL")

@url.subcommand(description="Generate a custom short URL")
async def custom(interaction: nextcord.Interaction, url: str = SlashOption(description="The URL to shorten. Note the URL must include the http:// or https://", required=True), custom_url: str = SlashOption(description="The custom URL to use", required=True)):
    
    if re.match(r".*[\'\"].*", url):
        await interaction.send("You entered an invalid URL")
    
    elif re.match(r".*[\'\"].*",custom_url):
        await interaction.send("You entered an invalid custom URL")
    
    else:
        if url.startswith("http://") or url.startswith("https://"):
            try:
                short_url = url_gen.custom(url, custom_url)
                await interaction.send(f"Shortened URL: {short_url}")
            
            except url_gen.InvalidURLError:
                await interaction.send("You entered an invalid URL")
            
            except url_gen.InvalidCustomURLError:
                await interaction.send("You entered an invalid custom URL")
            
            except url_gen.RateLimitError:
                await interaction.send("The URL shortener is currently rate limited. Please try again later.")
            
            except url_gen.UnknownError:
                await interaction.send("An unknown error occurred. Please try again later.")
        else:
            await interaction.send("Please include http:// or https:// in your URL")

if __name__ == "__main__":
    
    try:
        import config
        if config.discord_api_key == "DISCORD_API_KEY_HERE":
            print("Please add your Discord API key to config.py")
            quit()
        else:    
            bot.run(config.discord_api_key)
    
    except ImportError:
        print("Please rename default_config.py to config.py and add your Discord API key.")
        quit()