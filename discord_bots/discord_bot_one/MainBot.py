import discord
import os
from tic_tac_toe import TicTacToe

client = discord.Client()
tic_tac_toe_games = {}


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    msg = message.content.lower()
    if message.author == client.user:
        return
    if msg.startswith("$play"):
        if message.author not in tic_tac_toe_games:
            game = TicTacToe.Game(message.author, message.channel)
            await game.make_board()
            tic_tac_toe_games[game.message] = game


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    if reaction.message in tic_tac_toe_games:
        game = tic_tac_toe_games.get(reaction.message)
        await game.turn(reaction, user)
        if await game.check_win():
            tic_tac_toe_games.pop(reaction.message)

client.run(os.getenv("TOKEN"))
