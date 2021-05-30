import csv
import discord
import os

client = discord.Client()
greetings = ["yo", "hi", "hello"]
b = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
turns = {"0️⃣": "0", "1️⃣": "1", "2️⃣": "2", "3️⃣": "3", "4️⃣": "4", "5️⃣": "5", "6️⃣": "6", "7️⃣": "7", "8️⃣": "8"}
prev = "O"
x_player = None
o_player = None
ttt_msg = None
ttt_channel = None
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
        await message.channel.send("<@{}>".format(message.author.id) + " bad")
        await message.channel.send("<@{}>".format(405758393228460033) + " Buy Sea of thieves now!\nhttps://store.steampowered.com/app/1172620/Sea_of_Thieves/")
    if "bad" in msg.replace(" ", ""):
        await message.channel.send(":(")
    if msg.split(" ")[0] == "$play":
        await tic_tac_toe_new(message)

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    emoji = reaction.emoji
    if emoji in turns:
        await tic_tac_toe(turns.get(emoji), user)


async def tic_tac_toe_new(message):
    global b
    global prev
    global x_player
    global o_player
    global ttt_msg
    global ttt_channel
    if ttt_channel is None:
        ttt_channel = message.channel
    ttt_msg = await ttt_channel.send(f"{x_player} vs {o_player}\n"
                                         f"```\n{b[0]}|{b[1]}|{b[2]}"
                                         f"\n-----\n{b[3]}|{b[4]}|{b[5]}"
                                         f"\n-----\n{b[6]}|{b[7]}|{b[8]}\n```")
    for emoji in turns.keys():
        await ttt_msg.add_reaction(emoji)


async def tic_tac_toe(turn, author):
    global ttt_msg
    global prev
    global o_player
    global x_player
    if x_player is None:
        x_player = author
    elif o_player is None:
        o_player = author
    if not turn.isdigit():
        await ttt_channel.send("Not an integer.")
        return
    if b[int(turn)] == " ":
        if prev == "O":
            if author != x_player:
                await ttt_channel.send("Not your turn!")
                return
            b[int(turn)] = "X"
            prev = "X"
        elif prev == "X":
            if author != o_player:
                await ttt_channel.send("Not your turn!")
                return
            b[int(turn)] = "O"
            prev = "O"
    else:
        await ttt_channel.send(f"Space is already occupied, try again.")
    await ttt_msg.edit(content=f"{x_player} vs {o_player}\n"
                               f"```\n{b[0]}|{b[1]}|{b[2]}"
                               f"\n-----\n{b[3]}|{b[4]}|{b[5]}"
                               f"\n-----\n{b[6]}|{b[7]}|{b[8]}\n```"
                               f"<@{x_player.id if prev == 'O' and x_player is not None else o_player.id if prev == 'X' and o_player is not None else 'None yet'}> turn!")
    await check_win()


async def check_win():
    global b
    global prev
    global x_player
    global o_player
    global ttt_msg
    for w in win:
        if b[w[0]] == b[w[1]] == b[w[2]] != " ":
            await ttt_channel.send(f"<@{x_player.id if b[w[0]] == 'X' else o_player.id}> has won!")
            with open("standings.csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                writer.writerow([x_player if b[w[0]] == 'X' else o_player,
                                 o_player if b[w[0]] == 'X' else x_player,
                                 "winner"])
            b = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
            prev = "O"
            x_player = None
            o_player = None
            ttt_msg = None
    for space in b:
        if space == " ":
            return
    await ttt_channel.send("Tie game!")
    with open("standings.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow([x_player, o_player, "tie"])

client.run(os.getenv("TOKEN"))
