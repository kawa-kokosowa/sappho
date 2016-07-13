import pygame


class PhysicalSprite(pygame.sprite.Sprite):
    """A sprite with a position and collision data.

    Attributes:
        sprite (pygame.Sprite): The sprite which represents
            this actor, and from which the actor's mask and
            rect are derived every call to update_state().
        rect (pygame.Rect): Rectangle whose dimensions
            are updated (update_state) to reflect that
            of the sprite's rect dimensions. Absolute position
            of the Actor is set by setting this rect's:
            topleft, center, etc.
        mask (pygame.Mask): Reference to sprite's mask,
            which is updated every update_state().

    """

    def __init__(self, sprite):
        """Create a PhysicalSprite, using data from the
        supplied sprite.

        Arguments:
            sprite (pygame.Sprite): A Pygame sprite with the
                special attributes of mask and update_state().
                QUACK!

        """

        super(AnimatedSprite, self).__init__()

        self.sprite = sprite
        self.rect = self.sprite.rect
        self.mask = self.sprite.mask

    def update_state(self, timedelta):
        self.sprite.update_state(timedelta)
        self.rect.size = self.sprite.size
        self.mask = self.sprite.mask
