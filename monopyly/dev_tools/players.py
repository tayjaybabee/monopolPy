from faker import Faker
from monopyly.models.player import Player
from monopyly.models.turns.counter import TurnCounter


FAKE = Faker()


def get_fake_player_list(fake = FAKE, num_players = 4):
    players = []
    for i in range(num_players):
        player = Player()
        player.name = fake.first_name()

        players.append(player)

    return players


def get_fake_turn_counter(fake = FAKE, num_players = 4):
    players = get_fake_player_list(fake, num_players)

    return TurnCounter(players)


