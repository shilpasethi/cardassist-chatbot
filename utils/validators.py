# utils/validators.py

"""
Validators: Helper methods for data validation.
"""
class Validators:
    @staticmethod
    def is_valid_card_number(card_number: str) -> bool:
        """
        Validates that the card number is exactly 9 digits (numeric).
        """
        return card_number.isdigit() and len(card_number) == 9
