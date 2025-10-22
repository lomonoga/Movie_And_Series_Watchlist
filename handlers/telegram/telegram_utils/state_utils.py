from typing import Any, Dict, List


def reset_user_state(context, state_keys: List[str] = None):
    if state_keys is None:
        state_keys = _get_state_keys()

    for key in state_keys:
        context.user_data.pop(key, None)

    service_keys = ["original_message_id", "original_chat_id", "current_state"]
    for key in service_keys:
        context.user_data.pop(key, None)


def set_user_state(context, state_data: Dict[str, Any]):
    for key, value in state_data.items():
        context.user_data[key] = value


def get_user_state(context, key: str, default=None):
    return context.user_data.get(key, default)


def is_user_waiting_input(context) -> bool:
    return any(context.user_data.get(flag, False) for flag in _get_state_keys())


def _get_state_keys():
    return [
        "waiting_playlist_create_name",
        "waiting_movie_add_name",
        "playlists_add_movie_playlist_id"
    ]
