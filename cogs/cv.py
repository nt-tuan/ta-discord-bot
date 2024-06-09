""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import discord
from discord.ext import commands
from discord.ext.commands import Context
from ai import upload_file


# Here we name the cog and create a new class for the cog.
class CV(commands.Cog, name="cv"):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="cv",
        description="This is a command to upload CV",
    )
    async def upload_cv(self, context: Context) -> None:
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        # Do your stuff here
        if len(context.message.attachments) != 1:
            await context.send("Please attach one CV file")
            return

        file = await context.message.attachments[0].to_file()
        # file.fp
        json_data = upload_file(file.fp)
        name = json_data["Name"]
        phone = json_data["Phone"]
        email = json_data["Email"]
        experiences = "Experiences:\n" + "".join(
            map(lambda str: f"- {str}\n", json_data["Experiences"])
        )
        skills = "Skills:\n" + "".join(
            map(lambda str: f"- {str}\n", json_data["Skills"])
        )
        embed = discord.Embed(
            title="CV Information",
            description=f"Name: `{name}`\n"
            + f"Phone: {phone}\n"
            + f"Email: {email}\n"
            + f"Experiences: {experiences}\n"
            + f"Skills: {skills}\n",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(CV(bot))
