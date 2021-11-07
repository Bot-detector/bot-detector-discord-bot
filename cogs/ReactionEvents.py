import discord
from discord.ext import commands

from utils import CommonCog


class ReactionHandling(CommonCog):
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.member.id != self.bot.user.id:
            if payload.emoji.name == '✅':
                vote = 1
            elif payload.emoji.name == '❌':
                vote = -1
            else:
                #Thanks for the enthusiasm, but not what we're looking for.
                return

            await self.add_prediction_feedback(payload, vote)



    async def get_reaction_message(self, reaction_payload: discord.RawReactionActionEvent):
        guild = self.bot.get_guild(reaction_payload.guild_id)
        channel = guild.get_channel(reaction_payload.channel_id)
        message = await channel.fetch_message(reaction_payload.message_id)

        return message

    async def add_prediction_feedback(self, payload, vote):
        prediction_data = await self.extract_prediction(payload)

        prediction = {
            "discord_id":   payload.user_id,
            "name":         prediction_data[0],
            "prediction":   prediction_data[1],
            "confidence":   prediction_data[2],
            "vote":         vote
        }

        endpoint = "https://www.osrsbotdetector.com/dev/discord/predictionfeedback/"

        await self.bot.session.post(endpoint, json=prediction)


    async def extract_prediction(self, payload: discord.RawReactionActionEvent):
        message = await self.get_reaction_message(payload)

        name_substring = "+ Name: "
        prediction_substring = "Prediction: "
        confidence_substring = "Confidence: "

        message_lines = message.content.splitlines()

        name_line = [i for i in message_lines if name_substring in i]
        prediction_line = [i for i in message_lines if prediction_substring in i]
        confidence_line = [i for i in message_lines if confidence_substring in i]

        name = name_line[0].split(name_substring)[1]
        prediction = prediction_line[0].split(prediction_substring)[1]
        confidence_percent = confidence_line[0].split(confidence_substring)[1]

        confidence = float(confidence_percent.strip('%'))/100

        return name, prediction, confidence

def setup(bot):
    bot.add_cog(ReactionHandling(bot))
