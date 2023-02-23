from typing import Any, Tuple
from dungeonsheets import spells


def all_spells():
    """Generate all the valid spell classes so far defined."""
    for spell_name, spell in spells.__dict__.items():
        # Check if it's (a) a class and (b) a subclass of ``Spell``
        if isinstance(spell, type) and issubclass(spell, Spell):
            yield spell


class Spell:
    """A magical spell castable by a player character."""

    level:int = 0
    name: str = "Unknown spell"
    casting_time: str = "1 action"
    casting_range:str = "60 ft"
    components: Tuple[str,...] = ()
    materials: str = ""
    duration: str = "instantaneous"
    ritual: bool = False
    _concentration: bool = False
    magic_school: str = ""
    classes = ()

    def __str__(self):
        s = self.name
        requirements = list(self.components)
        # Indicate if this is a ritual or a concentration
        indicators = [
            ("R", self.ritual),
            ("C", self.concentration),
            ("$", self.special_material),
        ]
        requirements.extend([letter for letter, is_active in indicators if is_active])
        if len(requirements):
            s += f' ({"/".join(requirements)})'
        return s

    def __repr__(self):
        return f"{self.level} {self.name}"

    def __eq__(self, other):
        return (self.name == other.name) and (self.level == other.level)

    def __hash__(self):
        return 0

    @property
    def component_string(self):
        s = f'{", ".join(self.components)}'
        if "M" in self.components:
            s += f" ({self.materials})"
        return s

    @property
    def concentration(self):
        return ("concentration" in self.duration.lower()) or self._concentration

    @concentration.setter
    def concentration(self, val: bool):
        self._concentration = val

    @property
    def special_material(self):
        return "worth" in self.materials.lower()


def create_spell(**params: Any) -> Spell:
    """Create a new subclass of ``Spell`` with given default parameters.

    Useful for spells that haven't been entered into the ``spells.py``
    file yet.

    Parameters
    ----------
    params : optional
      Saved as attributes of the new class.

    Returns
    -------
    NewSpell
      New spell class, subclass of ``Spell``, with given params.
    """
    NewSpell = Spell
    NewSpell.name = params.get("name", "Unknown Spell")
    NewSpell.level = params.get("level", 9)
    return NewSpell