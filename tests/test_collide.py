import os

import pygame

from sappho import animate
from sappho import collide


# this sprite is 10x10
testpath = os.path.realpath(__file__)
path = os.path.abspath(os.path.join(testpath,
                                    "..",
                                    "resources",
                                    "animatedsprite.gif"))

animsprite_mask_20_20 = animate.AnimatedSprite.from_gif(
    path,
    mask_threshold=254
)

animsprite_mask_20_20.rect.topleft = (20, 20)

animsprite_mask_40_40 = animate.AnimatedSprite.from_gif(
    path,
    mask_threshold=254
)

animsprite_mask_40_40.rect.topleft = (40, 40)

animsprite_group_sans_one = pygame.sprite.Group(animsprite_mask_40_40)


def test_move_close_as_possible():
    """

    Move `animsprite_mask_20_20` to (60, 60), which should collide
    with both `animsprite_mask_40_40` and `animsprite_35_40`.

    """

    closest_to_goal, collided_with = collide.move_as_close_as_possible(
        animsprite_mask_20_20,
        (60, 60),
        animsprite_group_sans_one
    )
    assert closest_to_goal == (30, 30)
    assert collided_with is animsprite_mask_40_40

    closest_to_goal, collided_with = collide.move_as_close_as_possible(
        animsprite_mask_20_20,
        (10, 10),
        animsprite_group_sans_one
    )
    assert closest_to_goal == (10, 10)
    assert collided_with is None
