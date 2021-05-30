import csv

class Game:

    def __init__(self, player, channel):
        self.board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        self.previous_turn = "O"
        self.x_player = player
        self.o_player = None
        self.message = None
        self.channel = channel
        self.turns = {"0️⃣": 0, "1️⃣": 1, "2️⃣": 2,
                      "3️⃣": 3, "4️⃣": 4, "5️⃣": 5,
                      "6️⃣": 6, "7️⃣": 7, "8️⃣": 8}
        self.win = [[0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [2, 4, 6]]

    async def make_board(self):
        self.message = await self.channel.send(f"{self.x_player} vs {self.o_player}\n"
                                               f"```\n{self.board[0]}|{self.board[1]}|{self.board[2]}"
                                               f"\n-----\n{self.board[3]}|{self.board[4]}|{self.board[5]}"
                                               f"\n-----\n{self.board[6]}|{self.board[7]}|{self.board[8]}\n```")
        for emoji in self.turns.keys():
            await self.message.add_reaction(emoji)

    async def turn(self, reaction, user):
        if self.o_player is None:
            self.o_player = user
        emoji = reaction.emoji
        if emoji in self.turns:
            await self.move(self.turns.get(emoji), user)

    async def move(self, move, user):
        if self.board[move] == " ":
            if self.previous_turn == "O":
                if user != self.x_player:
                    await self.channel.send("Not your turn!")
                    return
                self.board[move] = "X"
                self.previous_turn = "X"
            elif self.previous_turn == "X":
                if user != self.o_player:
                    await self.channel.send("Not your turn!")
                    return
                self.board[move] = "O"
                self.previous_turn = "O"
        else:
            await self.channel.send(f"Space is already occupied, try again.")
        await self.message.edit(content=f"{self.x_player} vs {self.o_player}\n"
                                        f"```\n{self.board[0]}|{self.board[1]}|{self.board[2]}"
                                        f"\n-----\n{self.board[3]}|{self.board[4]}|{self.board[5]}"
                                        f"\n-----\n{self.board[6]}|{self.board[7]}|{self.board[8]}\n```"
                                        f"<@{self.x_player.id if self.previous_turn == 'O' and self.x_player is not None else self.o_player.id if self.previous_turn == 'X' and self.o_player is not None else 'None yet'}> turn!")

    async def check_win(self):
        for w in self.win:
            if self.board[w[0]] == self.board[w[1]] == self.board[w[2]] != " ":
                await self.channel.send(f"<@{self.x_player.id if self.board[w[0]] == 'X' else self.o_player.id}> has won!")
                with open("standings.csv", "a", newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=",")
                    writer.writerow([self.x_player if self.board[w[0]] == 'X' else self.o_player,
                                     self.o_player if self.board[w[0]] == 'X' else self.x_player,
                                     "winner"])
                return True
        for space in self.board:
            if space == " ":
                return False
        await self.channel.send("Tie game!")
        with open("standings.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow([self.x_player, self.o_player, "tie"])
        return True
