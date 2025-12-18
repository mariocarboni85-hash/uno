from typing import Dict

from .action import Action


class ActionNormalizer:
    REQUIRED_FIELDS = {"type", "payload", "sender", "mode"}

    @staticmethod
    def normalize(raw_action: Dict) -> Action:
        if not isinstance(raw_action, dict):
            raise ValueError("Azione non strutturata")

        if not ActionNormalizer.REQUIRED_FIELDS.issubset(raw_action.keys()):
            raise ValueError("Campi azione mancanti")

        return Action(
            type=raw_action["type"],
            payload=raw_action["payload"],
            sender=raw_action["sender"],
            mode=raw_action["mode"]
        )
