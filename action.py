from dataclasses import dataclass

@dataclass(frozen=True)
class Action:
    type: str          # "shell" | "file_read" | "file_write"
    payload: dict
    sender: str        # deve essere "vit"
    mode: str          # "restricted" | "sandbox"
