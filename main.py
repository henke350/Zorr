import random

# --- Data for all of Zorr's Tables (No changes needed here) ---
TABLES = {
    1: {"name": "Table I", "rolls": {range(1, 8): "Do nothing.", range(8, 9): "Sacrifice your best Creature.", range(9, 11): "Zorr puts a RED 1/1 Token Creature on the battlefield."}, "advancement": range(1, 9)},
    2: {"name": "Table II", "rolls": {range(1, 5): "Do nothing.", range(5, 8): "Zorr puts a GREEN 2/2 Token Creature on the battlefield.", range(8, 9): "Zorr gets a bonus roll using Bonus Table A.", range(9, 11): "Exile your best Creature."}, "advancement": range(1, 8)},
    3: {"name": "Table III", "rolls": {range(1, 4): "Do nothing.", range(4, 5): "Zorr puts 2 BLUE 1/1 Token Creatures [Flying] on the battlefield.", range(5, 6): "Zorr puts a GREEN 3/3 Token Creature on the battlefield.", range(6, 7): "Destroy your best Land.", range(7, 8): "Zorr puts a BLACK 1/1 Token Creature [Lifelink] on the battlefield.", range(8, 9): "Zorr puts a WHITE 1/1 Token Creature on the battlefield and Zorr gets a bonus roll using Bonus Table B.", range(9, 10): "Destroy your best Creature.", range(10, 11): "Sacrifice your best Artifact or roll on the Zorr's Wrath chart (-2)."}, "advancement": range(1, 7)},
    4: {"name": "Table IV", "rolls": {range(1, 4): "Do nothing.", range(4, 5): "Zorr puts a BLACK 4/4 Token Creature [Menace] on the battlefield.", range(5, 6): "Sacrifice your best Creature.", range(6, 7): "Destroy your best Artifact or Enchantment.", range(7, 8): "Exile your best Creature.", range(8, 9): "Sacrifice your two best Creatures or take 4 damage.", range(9, 10): "Zorr puts 2 RED 3/1 Token Creatures on the battlefield or roll on Zorr's Wrath chart (-1).", range(10, 11): "Roll on the Zorr's Wrath chart (+0)."}, "advancement": range(1, 7), "advancement_after": range(1, 6)},
    5: {"name": "Table V", "rolls": {range(1, 4): "Do nothing.", range(4, 5): "Zorr puts a BLACK 3/3 Token Creature [Deathtouch] on the battlefield.", range(5, 6): "Zorr puts a WHITE 2/2 Token Creature [Flying] on the battlefield and Zorr gets a bonus roll using Table C.", range(6, 7): "Destroy your best Artifact, Creature, or Enchantment (whichever you hold dearest).", range(7, 8): "Zorr puts a GREEN 4/4 Token Creature on the battlefield.", range(8, 9): "Zorr puts a BLACK 4/4 Token Creature on the battlefield or destroy all your Lands.", range(9, 10): "Sacrifice your best Creature or roll on the Zorr's Wrath chart (+1).", range(10, 11): "Roll on the Zorr's Wrath chart (+2)."}, "advancement": range(1, 6)},
    6: {"name": "Table VI", "rolls": {range(1, 4): "Do nothing.", range(4, 5): "Zorr puts a BLACK 2/4 Token Creature [Reach] on the battlefield or you may sacrifice all your Artifacts, Creatures, and Lands.", range(5, 6): "Zorr puts a RED 5/1 Token Creature [Trample] [Haste] on the battlefield.", range(6, 8): "Sacrifice your best Creature or take 6 damage.", range(8, 9): "Destroy your best Artifact, Enchantment, or Land (whichever you hold dearest).", range(9, 10): "Sacrifice your best creature or roll on the Zorr's Wrath chart (+3).", range(10, 11): "Roll on the Zorr's Wrath chart (+4)."}, "advancement": "None"}
}
BONUS_TABLES = {
    "A": {"name": "Bonus Table A", "rolls": {range(1, 8): "Do nothing.", range(8, 9): "Sacrifice your best Creature.", range(9, 11): "Zorr puts a RED 1/1 Token Creature on the battlefield."}},
    "B": {"name": "Bonus Table B", "rolls": {range(1, 5): "Do nothing.", range(5, 8): "Zorr puts a GREEN 2/2 Token Creature on the battlefield.", range(8, 9): "Tap all of your Creatures.", range(9, 11): "Exile your best Creature."}},
    "C": {"name": "Bonus Table C", "rolls": {range(1, 4): "Do nothing.", range(4, 5): "Zorr puts a WHITE 1/1 Token Creature on the battlefield.", range(5, 6): "Zorr puts a BLUE 1/1 Token Creature [Flying] on the battlefield.", range(6, 7): "Destroy your best Land.", range(7, 8): "Zorr puts a BLACK 1/1 Token Creature [Lifelink] on the battlefield.", range(8, 9): "Zorr puts a GREEN 3/3 Token Creature on the battlefield.", range(9, 10): "Exile your best Creature.", range(10, 11): "Sacrifice your best Artifact or roll on the Zorr's Wrath chart (-2)."}}
}
ZORRS_WRATH = {"name": "Zorr's Wrath", "rolls": {range(0, 2): "Zorr puts 2 BLUE 1/1 Token Creatures [Flying] on the battlefield; plus he gains 2 life.", range(2, 3): "Zorr plays an Artifact card (randomly decide which one).", range(3, 4): "Zorr puts a WHITE 4/4 Token Creature [Flying] on the battlefield; plus he gains 3 life.", range(4, 5): "Sacrifice all of your Artifacts, or all of your Creatures, or all of your Enchantments. Treat Zorr's next roll as \"Do nothing.\"", range(5, 6): "Zorr plays an Emblem card (randomly decide which one).", range(6, 7): "Zorr puts a RED 5/5 Token Creature [Flying] on the battlefield; plus he gains 4 life.", range(7, 8): "Zorr puts a BLACK 5/5 Token Creature [Trample] on the battlefield; plus you lose 4 life.", range(8, 9): "Sacrifice all of your Lands of one basic type (whichever type is most prevalent on battlefield; otherwise, your choice). Treat Zorr's next roll as \"Do nothing.\"", range(9, 10): "Exile the top five cards in your library.", range(10, 100): "Zorr gains 6 life."}}


class ZorrAI:
    """Handles the game logic for the Zorr AI."""
    def __init__(self):
        self.current_table_num = 1
        self.table_iv_first_use = True

    def _get_result_from_table(self, roll, table_data):
        """Finds the result for a given roll in a table's data."""
        for roll_range, result_text in table_data["rolls"].items():
            if roll in roll_range:
                return result_text
        return "Error: Roll out of range"

    def play_zorr_turn(self):
        """
        Simulates one turn for Zorr, returning all displayable information.
        """
        table_data = TABLES[self.current_table_num]
        main_roll = random.randint(1, 10)
        main_result = self._get_result_from_table(main_roll, table_data)

        bonus_info = None
        wrath_info = None
        advancement_info = None
        
        # --- Handle special results ---
        result_to_check = main_result
        
        if "Bonus Table" in result_to_check:
            bonus_table_key = result_to_check.split("Bonus Table ")[1][0]
            bonus_table = BONUS_TABLES[bonus_table_key]
            bonus_roll = random.randint(1, 10)
            bonus_result = self._get_result_from_table(bonus_roll, bonus_table)
            bonus_info = f"Bonus Roll ({bonus_table['name']}): {bonus_roll} -> {bonus_result}"
            result_to_check = bonus_result # Check the bonus result for a potential wrath roll

        if "Zorr's Wrath" in result_to_check:
            modifier_start = result_to_check.find('(')
            modifier_end = result_to_check.find(')')
            modifier = int(result_to_check[modifier_start + 1:modifier_end])
            
            wrath_roll = random.randint(1, 10)
            modified_roll = wrath_roll + modifier
            wrath_result = self._get_result_from_table(modified_roll, ZORRS_WRATH)
            wrath_info = f"Zorr's Wrath! ({wrath_roll} {modifier:+}) -> {wrath_result}"

        # --- Handle Table Advancement ---
        advancement_range = table_data.get("advancement")
        if self.current_table_num == 4 and not self.table_iv_first_use:
            advancement_range = table_data.get("advancement_after")

        if advancement_range != "None" and main_roll in advancement_range:
            if self.current_table_num < 6:
                self.current_table_num += 1
                advancement_info = f"*** Zorr advances to Table {self.current_table_num}! ***"
            if self.current_table_num == 4 and self.table_iv_first_use:
                self.table_iv_first_use = False
        
        return {
            "table_name": table_data["name"],
            "roll": main_roll,
            "result": main_result,
            "bonus_info": bonus_info,
            "wrath_info": wrath_info,
            "advancement_info": advancement_info
        }