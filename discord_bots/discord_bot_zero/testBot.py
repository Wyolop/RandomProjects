import discord
import os

client = discord.Client()
greetings = ["yo", "hi", "hello"]
b = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
prev = "O"
x_player = None
o_player = None
win = [[0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [2, 4, 6]]


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    msg = message.content.lower()
    if message.author == client.user:
        return
    if any(msg.startswith(word) for word in greetings):
        await message.channel.send("yo")
    if msg == "!":
        await message.channel.send("<@405758393228460033>" + " Buy Sea of thieves now!\nhttps://store.steampowered.com/app/1172620/Sea_of_Thieves/")
    if "bad" in msg.replace(" ", ""):
        await message.channel.send(":(")
    if msg.split(" ")[0] == "$play":
        await tic_tac_toe(message)


async def tic_tac_toe(message):
    global b
    global prev
    global x_player
    global o_player
    if x_player is None:
        x_player = message.author
    elif o_player is None:
        o_player = message.author
    if message.author != x_player and message.author != o_player:
        await message.channel.send("You are not playing!")
        return
    turn = message.content.split(" ")[-1]
    if not turn.isdigit():
        await message.channel.send("Not an integer.")
        return
    if b[int(turn)] == " ":
        if prev == "O":
            if message.author != x_player:
                await message.channel.send("Not your turn!")
                return
            b[int(turn)] = "X"
            prev = "X"
        elif prev == "X":
            if message.author != o_player:
                await message.channel.send("Not your turn!")
                return
            b[int(turn)] = "O"
            prev = "O"
    else:
        await message.channel.send(f"Space is already occupied, try again.")
    await message.channel.send(f"```\n{b[0]}|{b[1]}|{b[2]}\n-----\n{b[3]}|{b[4]}|{b[5]}\n-----\n{b[6]}|{b[7]}|{b[8]}\n```")
    await check_win(message)


async def check_win(message):
    global b
    global prev
    global x_player
    global o_player
    for w in win:
        if b[w[0]] == b[w[1]] == b[w[2]] != " ":
            b = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
            prev = "O"
            await message.channel.send(f"@{x_player if b[w[0]] == 'X' else o_player} has won!")
            x_player = None
            o_player = None
    for space in b:
        if space == " ":
            return
    await message.channel.send("Tie game!")

client.run(os.getenv("TOKEN"))
