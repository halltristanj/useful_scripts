"""
Give a gift to a person who is not in your family.

A totally unscallable solution [TM].
"""

import random

# List possible receivers of gifts from single person. Cannot give a gift to an SO.
FAMILY_MEMBERS = [
    ["Kaili"],
    ["A.J.", "Rachel"],
    ["Tristan", "Catherine"],
]


class GiftGiver:
    def __init__(self, family_members):
        self.family_members = family_members
        self.family_members_flat = self.flatten_family()
        self.giver_dict = {}

    def flatten_family(self):
        """
        Take the list of tuples (a family of families) and make it
        one long family

        Returns
        -------
        list
          A list of all family members
        """
        return [member for family in self.family_members for member in family]

    def giver_alg(self):
        """Create a gift-giving dictionary and fill self.giver_dict"""
        # Shuffle family members so always get random first instance (FIFO)
        random.shuffle(self.family_members)
        # Shuffle flat family member list so we randomize that (FIFO)
        random.shuffle(self.family_members_flat)
        for family in self.family_members:
            # Loop through each Sig Other
            for member in family:
                # Loop through all possible recipients in family_members_flat
                # Assign member to that recipient.
                for recipient in self.family_members_flat:
                    if recipient != member and recipient not in family and member not in \
                            self.giver_dict.keys():
                        self.giver_dict[member] = recipient
                        self.family_members_flat.pop(self.family_members_flat.index(recipient))
                        # Randomize the all family list again (FIFO)
                        random.shuffle(self.family_members_flat)
        return self.giver_dict

    def print_result(self):
        for giver, recipient in self.giver_alg().items():
            print(f"{giver} gives to {recipient}")

        print("We all give to Nique.")

    def run(self):
        gifts.print_result()


if __name__ == '__main__':
    gifts = GiftGiver(FAMILY_MEMBERS)
    gifts.run()
