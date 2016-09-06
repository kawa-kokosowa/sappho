"""Painless animated sprites which are pygame.sprite.Sprite objects.

Animated sprites from GIF, and all YOU have to know is to `update_state`!
You just have to call `update_state` once per loop with the timedelta:

  >>> AnimatedSprite.from_gif('example.gif')  # doctest: +SKIP
  >>> timedelta = clock.get_time()  # doctest: +SKIP
  >>> animated_sprite.update_state(timedelta)  # doctest: +SKIP

Treat it like a normal pygame sprite, because it is! It's that easy!

A word on `rect` and `mask`:
    In pygame, `Sprite` has the `rect` attribute and optionally the
    `mask` attribute. Both `rect` and `mask` sprite attributes are the
    primary data used in collision detection.

    In this implementation, `Frame` and `AnimatedSprite` both have the
    `mask` and `rect` attributes. Don't use `rect for positional stuff,
    e.g., don't do something like `animatedsprite.rect.topleft = (11, 22)`.
    The `mask` and `rect` of an `AnimatedSprite` are merely a reference to
    the current `Frame`'s `rect` and `mask`! When you load an animated
    sprite, you can specify a threshold:

      >>> AnimatedSprite.from_gif('example.gif',
      ...                         mask_threshold=254)  # doctest: +SKIP

    Whereas, the threshold denotes the alpha transparency value for a
    pixel, which is opaque enough to be "set".

What's supported:
    Right now there's only support for GIFs, but I'd like to expand that
    (especially since GIFs can't really take advantage of alpha
    transparency).

"""

import pygame
from PIL import Image


# NOTE: could be a sprite...
class Frame(object):
    """A frame of an AnimatedSprite animation.

    Attributes:
        surface (pygame.Surface): The pygame image which is used
            for a frame of an animation.
        mask (pygame.Mask): Mask automatically generated from the
            supplied surface (see above). Only exists if mask_threshold
            was >0 on init.
        duration (integer): Milliseconds this frame lasts. How
            long this frame is displayed in corresponding animation.
        start_time (integer): The animation position in milleseconds,
            when this frame will start being displayed.

    See Also:
        * AnimatedSprite.frames_from_gif()
        * AnimatedSprite.animation_position

    """

    def __init__(self, surface, start_time, duration, mask_threshold=0):
        """Create a frame using a pygame surface, the start time,
        and the duration time.

        Args:
            surface (pygame.Surface): The surface/image for this
                frame.
            start_time (int): Millisecond this frame starts. This
                frame is a part of a larger series of frames and
                in order to render the animation properly we
                need to know when each frame begins to be drawn,
                while duration signifies when it ends.
            duration (integer): Milleseconds this frame lasts. See:
                start_time argument description.
            mask_threshold (int): Valid values 0-254. Alpha values
                ABOVE this provided number are marked as "solid"/
                collidable/set. If this is not greater than zero,
                the mask is not generated.

        """

        self.surface = surface
        self.duration = duration
        self.start_time = start_time
        self.end_time = start_time + duration

        if mask_threshold > 0:
            self.mask = pygame.mask.from_surface(surface, mask_threshold)

    def __repr__(self):
        s = "<Frame duration(%s) start_time(%s) end_time(%s)>"

        return s % (self.duration, self.start_time, self.end_time)


class AnimatedSprite(pygame.sprite.Sprite):
    """Animated sprite with mask, loaded from GIF.

    Supposed to be mostly uniform with the Sprite API.

    Attributes:
        total_duration (int): The total duration of of this
            animation in milliseconds.
        image (pygame.Surface): Current surface belonging to
            the active frame. Set once per tick through
            the AnimatedSprite.update_state() method.
        rect (pygame.Rect): Does not reflect position, only
            area. Updated once per tick, to reflect current
            frame's rect, in AnimatedSprite.update_state().
        mask (pygame.Mask): If the first frame had a mask
            attribute, then we assume all do, and this
            (optional) attribute points to the active
            frame's mask attribute.
        active_frame_index (int): Frame # which is being
            rendered/to be rendered. Also updated once per
            tick, see the AnimatedSprite.update_state() method.
        active_frame: The current surface representing this
            animation at its current animation position. Set
            once per tick through the update_state() method.
        animation_position (int): Animation position in
            milliseconds; milleseconds elapsed in this
            animation. This is used for determining
            which frame to select. Set once per tick through
            the AnimatedSprite.update_state() method.

    See Also:
        * :class:`pygame.sprite.Sprite`
        * :class:`Frame`

    """

    def __init__(self, frames):
        """Create this AnimatedSprite using
        a list of Frame instances.

        Args:
            frames (list[Frame]): A properly assembled list of frames,
                which assumes that each Frame's start_time is greater
                than the previous element and is the previous element's
                start time + previous element/Frame's duration. Here
                is an example of aformentioned:

                >>> frame_one_surface = pygame.Surface((16, 16))
                >>> frame_one = Frame(frame_one_surface, 0, 100)
                >>> frame_two_surface = pygame.Surface((16, 16))
                >>> frame_two = Frame(frame_two_surface, 100, 50)

        Note:
            In the future I may add a method for verifying the
            validity of Frame start_times and durations.

        """

        super(AnimatedSprite, self).__init__()
        self.frames = frames
        self.total_duration = self.get_total_duration(self.frames)
        self.active_frame_index = 0
        self.active_frame = self.frames[self.active_frame_index]

        # animation position in milliseconds
        self.animation_position = 0

        # this gets updated depending on the frame/time
        # needs to be a surface.
        self.image = self.frames[0].surface

        # represents the animated sprite's position
        # on screen.
        self.rect = self.image.get_rect()

        # making the bold assumption that if the
        # first frame has a mask, as do the rest.
        if hasattr(self.frames[0], 'mask'):
            self.mask = self.frames[0].mask

    def __getitem__(self, frame_index):
        """Return the frame corresponding to
        the supplied frame_index.

        Args:
            frame_index (int): Index number to lookup
                a frame by element number in the
                self.frames list.

        Returns:
            Frame: The frame of this animation at the
                specified index of frame_index.

        """

        return self.frames[frame_index]

    def largest_frame_size(self):
        """Return the largest frame's (by area)
        dimensions as tuple(int x, int y).

        Returns:
            tuple (x, y): pixel dimensions of the largest
                frame surface in this AnimatedSprite.

        """

        largest_frame_size = (0, 0)

        for frame in self.frames:
            largest_x, largest_y = largest_frame_size
            largest_area = largest_x * largest_y

            frame_size = frame.surface.get_size()
            frame_x, frame_y = frame_size
            frame_area = frame_x * frame_y

            if frame_area > largest_area:
                largest_frame_size = (frame_size)

        return largest_frame_size

    @classmethod
    def from_gif(cls, path_or_readable, mask_threshold=0):
        """The default is to create from gif bytes, but this can
        also be done from other methods...

        Create a list of surfaces (frames) and a list of their
        respective frame durations from an animated GIF.

        Args:
            path_or_readable (str|file-like-object): Either a string
                or an object with a read() method. So, either a path
                to an animated GIF, or a file-like-object/buffer of
                an animated GIF.
            mask_threshold (int): An optional keyword argument which
                must be >0 to generate masks automatically per frame.
                This value is used to note which parts are opaque and
                thus collidable, and which values are not. Think of
                RGBA, valid values are 0-254. See also: Frame().

        Returns:
            AnimatedSprite: --

        """

        pil_gif = Image.open(path_or_readable)

        frame_index = 0
        frames = []
        time_position = 0

        try:

            while True:
                duration = pil_gif.info['duration']
                frame_sprite = cls.pil_image_to_pygame_surface(pil_gif)
                frame = Frame(surface=frame_sprite,
                              start_time=time_position,
                              duration=duration,
                              mask_threshold=mask_threshold)
                frames.append(frame)
                frame_index += 1
                time_position += duration
                pil_gif.seek(pil_gif.tell() + 1)

        except EOFError:

            pass  # end of sequence

        return AnimatedSprite(frames)

    def update(self, timedelta):
        """Manipulate the state of this AnimatedSprite, namely
        the on-screen/viewport position (not absolute) and
        using the timedelta to do animation manipulations.

        Using the game's timedelta we decipher the animation position,
        which in turn allows us to locate the correct frame.

        Sets the image attribute to the current frame's image. Updates
        the rect attribute to the new relative position and frame size.

        Warning:
            Since we're changing the rect size on-the-fly, this can
            get the player stuck in certain boundaries. I will be
            remedying this in the future.

        Args:
            timedelta (int|float): Typically from the game
                clock (pygame.time.Clock) via clock.get_time().
                Used to update the animation position.

        """

        self.animation_position += timedelta

        if self.animation_position >= self.total_duration:
            self.animation_position = (self.animation_position %
                                       self.total_duration)
            self.active_frame_index = 0

        while (self.animation_position >
               self.frames[self.active_frame_index].end_time):

            self.active_frame_index += 1

        # NOTE: the fact that I'm using -1 here seems sloppy/hacky
        self.image = self.frames[self.active_frame_index - 1].surface

        self.rect.size = self.image.get_size()
        self.active_frame = self.frames[self.active_frame_index]

        # if we have a mask, let's update our pointer!
        # again, we make the bold assumption that if
        # our first frame had a mask, then the rest do.
        if hasattr(self, 'mask'):
            self.mask = self.active_frame.mask

    @staticmethod
    def get_total_duration(frames):
        """Return the total duration of the animation in milliseconds,
        milliseconds, from animation frame durations.

        Args:
            frames (List[AnimatedSpriteFrame]): --

        Returns:
            int: The sum of all the frame's "duration" attribute.

        """

        return sum([frame.duration for frame in frames])

    @staticmethod
    def pil_image_to_pygame_surface(pil_image):
        """Convert PIL Image() to RGBA pygame Surface.

        Args:
            pil_image (Image): image to convert to pygame.Surface().

        Returns:
            pygame.Surface: the converted image

        Example:
            >>> from PIL import Image
            >>> gif = Image.open('demo/test_scene/test.gif')
            >>> AnimatedSprite.pil_image_to_pygame_surface(gif)
            <Surface(10x10x32 SW)>

        """

        image_as_string = pil_image.convert('RGBA').tobytes()

        return pygame.image.fromstring(image_as_string,
                                       pil_image.size,
                                       'RGBA')
