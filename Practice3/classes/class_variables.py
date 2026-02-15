class Player:
    # class variables
    game = "Space Adventure"
    max_health = 100
    players_count = 0

    def __init__(self, name):
        # instance variables
        self.name = name
        self.health = Player.max_health

        Player.players_count += 1

    def take_damage(self, damage):
        self.health -= damage

    def info(self):
        print(f"Name: {self.name}")
        print(f"Health: {self.health}")
        print(f"Game: {self.game}")
        print(f"Players created: {Player.players_count}")
        print("-" * 30)
