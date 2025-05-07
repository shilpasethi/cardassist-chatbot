# api/card_management.py

"""
Simulated backend API functions for card management.
"""
from utils.validators import Validators

# Simulated in-memory "database" of active cards
_active_cards = set()

def activate_card_backend(card_number: str) -> str:
    """
    Simulates activation of a card.
    """
    if not Validators.is_valid_card_number(card_number):
        return "Invalid card number. Activation failed."
    if card_number in _active_cards:
        return f"Card {card_number} is already activated."
    _active_cards.add(card_number)
    return f"Card {card_number} has been successfully activated."

def deactivate_card_backend(card_number: str) -> str:
    """
    Simulates deactivation of a card.
    """
    if not Validators.is_valid_card_number(card_number):
        return "Invalid card number. Deactivation failed."
    if card_number not in _active_cards:
        return f"Card {card_number} is not currently active."
    _active_cards.remove(card_number)
    return f"Card {card_number} has been successfully deactivated."
