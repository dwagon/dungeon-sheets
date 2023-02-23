from typing import Any, Generator, Iterator, Optional, TYPE_CHECKING
from dungeonsheets import weapons, features

if TYPE_CHECKING:
    from character import Character
    from spells import Spell


def create_feature(**params):
    """Create a new subclass of ``Feature`` with given default parameters.

    Useful for features that haven't been entered into the ``features.py``
    file yet.

    Parameters
    ----------
    params : optional
     Saved as attributes of the new class.

    Returns
    -------
    NewFeature
     New feature class, subclass of ``Feature``, with given params.
    """
    NewFeature = type("UnknownFeature", (Feature,), params)
    return NewFeature


class Feature:
    """
    Provide full text of rules in documentation
    """

    name: str = "Generic Feature"
    owner: Optional[Character] = None
    source: str = "Unknown"  # race, class, background, etc.
    spells_known: list[Spell] = []
    spells_prepared: list[Spell] = []
    needs_implementation = False  # Set to True if need to find way to compute stats

    def __init__(self, owner: Optional[Character]=None):
        self.owner: Optional[Character] = owner
        self.spells_known = [S() for S in self.spells_known]
        self.spells_prepared = [S() for S in self.spells_prepared]

    def __eq__(self, other: Any) -> bool:
        return (self.name == other.name) and (self.source == other.source)

    def __hash__(self) -> int:
        return 0

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '"{:s}"'.format(self.name)

    def weapon_func(self, weapon: weapons.Weapon, **kwargs):
        """
        Updates weapon based on the Feature property

        Parameters
        ----------
        weapon
          The weapon to be tested for special bonuses
        kwargs
          Any other key-word arguments the function may require
        """
        pass


class FeatureSelector(Feature):
    """
    A feature with multiple possible choices.
    """

    options = dict()
    name = ""
    source = ""

    def __new__(t, owner: Character, feature_choices=[]):
        # Look for matching feature_choices
        new_feat = Feature.__new__(Feature, owner=owner)
        new_feat.__doc__ = t.__doc__
        new_feat.name = t.name
        new_feat.source = t.source
        new_feat.needs_implementation = True
        for selection in feature_choices:
            if selection.lower() in t.options:
                feat_class = t.options[selection.lower()]
                if owner.has_feature(feat_class):
                    continue
                new_feat = feat_class(owner=owner)
                new_feat.source = t.source
        return new_feat


def all_features() -> Iterator[Feature]:
    """Generate all the valid features classes so far defined."""
    for feature_name, feature in features.__dict__.items():
        # Check if it's (a) a class and (b) a subclass of ``Features``
        if isinstance(feature, type) and issubclass(feature, Feature):
            yield feature
