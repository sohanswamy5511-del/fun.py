# ============================================================
# DEADLINE SYSTEM
# ============================================================
class DeadlineSystem:
    """
    Deadline system with 3-round progression per deadline.

    - Each deadline lasts 3 rounds
    - Display "X rounds left" (starting at 3)
    - After each set of spins, rounds decrement
    - When rounds reach 0 rounds left, payment is MANDATORY
    - After payment, reset to 3 rounds left for next deadline
    - Deadline amounts increase by 300% (4x) each payment
    """

    def __init__(self):
        self.current_deadline = 1
        self.rounds_left = 3
        self.payments_made = 0

    def get_deadline_amount(self, deadline_num):
        """Calculate deadline amount based on deadline number."""
        return int(1200 * (4 ** (deadline_num - 1)))

    def get_current_total(self):
        """Return the current amount owed."""
        return self.get_deadline_amount(self.current_deadline)

    def get_status_string(self):
        """Return display string for rounds and deadline."""
        return f"💀 DEADLINE {self.current_deadline} | {self.rounds_left} rounds left | ${self.get_current_total():,}"

    def decrement_round(self):
        """Decrement rounds after a set of spins is completed."""
        self.rounds_left -= 1

    def must_pay(self):
        """Check if payment is mandatory (rounds reached 0)."""
        return self.rounds_left == 0

    def pay_deadline(self):
        """Pay the deadline and advance to next one."""
        self.current_deadline += 1
        self.rounds_left = 3
        self.payments_made += 1

    def can_choose_phone_ability(self):
        """Check if the player can choose a phone ability (deadline 2 or higher)."""
        return self.current_deadline >= 2