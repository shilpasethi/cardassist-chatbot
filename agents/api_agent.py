# agents/api_agent.py

"""
APIAgent: Handles card activation/deactivation logic and communicates with simulated API.
"""
import re
from api.card_management import activate_card_backend, deactivate_card_backend

class APIAgent:
    """
    The APIAgent (CardManager) handles card-related operations by interacting with a backend API (simulated).
    """
    def __init__(self):
        pass

    def activate_card(self, user_input: str) -> str:
        """
        Extract card number from user input and attempt to activate the card.
        Returns a response message.
        """
        card_number = self._extract_card_number(user_input)
        if not card_number:
            return "Error: No valid 9-digit card number found in the input."
        result = activate_card_backend(card_number)
        return result

    def deactivate_card(self, user_input: str) -> str:
        """
        Extract card number from user input and attempt to deactivate the card.
        Returns a response message.
        """
        card_number = self._extract_card_number(user_input)
        if not card_number:
            return "Error: No valid 9-digit card number found in the input."
        result = deactivate_card_backend(card_number)
        return result

    def _extract_card_number(self, text: str) -> str:
        """
        Helper method to extract a 9-digit card number from text using regex.
        """
        match = re.search(r"\b\d{9}\b", text)
        return match.group(0) if match else None
    