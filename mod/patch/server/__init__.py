from . import minecraft_server, server_player_interaction_manager

def apply():
	minecraft_server.apply()
	server_player_interaction_manager.apply()

__all__ = [apply.__name__]
