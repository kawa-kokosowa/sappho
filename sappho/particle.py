"""Particle system definitions.

There's a few basic concepts here.  Note that all functions affecting physics,
emission, launch, and display are implemented as classes with a `__call__`
magic method, but could just as easily be pure functions since no extra info
is used on these.

    Particle: this represents each basic particle in the system, in particular
        its physical position, velocity, and lifetime.

    Emitter: this determines the number of particles emitted and time between
        particle emission.  It doesn't determine anything about particle
        location speed, etc., as an emitter simply takes a time delta (in
        seconds) and returns the number of particles to emit.

    Launcher: this is the same as a physics function.  Launchers are allowed
        to operate on a new particle (copy of a particle system's example
        particle) for 1 second effective time, instantaneously in real time.
        So an acceleration of 20 pixels / sec / sec, when put in a launcher,
        will give the particle a starting velocity of 20 pixels / sec.

    Physics: each physics function take a time delta and a particle and
        modifies the particle in some way.  It could move or accelerate the
        particle, change the particle's species, etc.

    Artist: this receives a surface to draw on, and a particle, and is
        responsible for drawing the particle on the surface as specified.
        Typically a drawer decides what the particle looks like, if it's
        stretched by velocity, etc.

    ParticleSystem: the current state of a system of particles, including
        all current particles, the physics that affects them, and the artists
        that illustrate them.
"""
from __future__ import division
import copy
import math
import random

import pygame


# The biggest number less than infinity-plus-one
INFINITY = float('inf')


class Particle(object):
    """This represents the state of a particle in the system.

    Contains all attributes expected by methods in this module, but
    you're always free to duck-type a particle class with more or fewer
    attributes as you need.  However, note that whatever particle class
    you make should be shallow-copiable by `copy.copy`.

    Attributes:
        x (float): X position of the particle's center, in pixels.
        y (float): Y position of the particle's center,.
        dx (float): X velocity of the particle, in pixels / second.
        dy (float): Y valocity of the particle, in pixels / second.
        life (float): Expected remaining lifetime of the particle, in seconds.
        species (str): Arbitrary name that can affect which physics or
            display to use for the particle.  (This attribute is currently
            unused, and may be used as desired by custom methods.)
        initial_life (float): Life that was initially granted to the particle
            after launch.  This allows one to calculate the remaining
            life fraction of the particle.
    """
    __slots__ = ['x', 'y', 'dx', 'dy', 'life', 'species', 'initial_life']

    def __init__(self, x, y, dx=0, dy=0, life=0, species=None):
        """Just initialize with attributes default values.
        """
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.life = life
        self.species = species
        self.initial_life = life


class ParticleSystem(object):
    """A particle system contains current state of particles, evolution
    functions, and illustration functions.

    After configuring a particle system with `__init__`, users are expected
    to regularly call `update_state(dt)` with time deltas to update physical
    state of the system, & `draw_on(surface)` to draw the particles on a
    pygame surface.  You may also periodically check `is_alive` to determine
    if the particle system has run out of particles and can safely be deleted.
    """
    def __init__(
            self, origin_particle, emitter, launcher,
            physics=None,
            artist=None,
            particle_limit=512,
            launcher_dt=1.0,
    ):
        """Create a new particle system.

        Arguments:
            origin_particle (Particle): A particle that defines the origin
                of the system, including its current location & velocity, and
                the initial lifetime remaining of a particle.
            emitter (callable): A function that takes a time delta (in seconds)
                and returns the number of new particles to emit.
            launcher (callable): A physics function that is called on a new
                particle just after being created with an effective time
                delta of one second.  This can apply initial velocity,
                lifetime, etc of the particle.
            physics (callable): A physics function that take a time delta (
                in seconds) and a particle, and applies an update to the
                particle physics that would occur in that period of time.
                Examples include gravitational acceleration, inertia, etc.
            artist (callable): A function taking a surface & a particle,
                that draws the particle however it likes on the given
                surface.
            particle_limit (int): The maximum ever allowed number of particles.
            launcher_dt (float): Effective number of seconds the launcher
                physics is applied to a new particle.

        """
        self.origin = origin_particle
        self.emitter = emitter
        self.launcher = launcher
        self.launcher_dt = launcher_dt
        self.physics = physics or PhysicsInertia()
        self.is_emitting = True
        self.artist = artist
        self.particle_limit = particle_limit
        self.particles = list()

    def is_alive(self):
        """Is this particle system still running? Either emitting new
        particles, or still illustrating old ones?

        returns (bool): Whether the system is still running.
        """
        return self.particles or self.is_emitting

    def update_state(self, dt):
        """Simulate physics for `dt` seconds.

        Arguments:
            dt (float): Number of elapsed seconds since last update.
        """
        for particle in self.particles:
            self.physics(dt, particle)
        self._discard_dead_particles()
        new_particle_count = self._get_new_particle_count(dt)
        for _ in range(new_particle_count):
            self._launch()

    def draw_on(self, surface):
        """Draw all particles on the given surface."""
        for particle in self.particles:
            self.artist(surface, particle)

    # Internal methods
    def _get_new_particle_count(self, dt):
        """Get count of new particles to create in next `dt` seconds.

        This isn't necessarily the same as the result of just running the
        emitter, because it also applies any particle limit that's in
        effect.
        """
        desired_particle_count = self.emitter(dt)
        self.is_emitting = desired_particle_count is not None
        particle_slots_available = self.particle_limit - len(self.particles)
        return min(desired_particle_count or 0, particle_slots_available)

    def _launch(self):
        """Build and launch a particle."""
        new_particle = copy.copy(self.origin)
        self.launcher(self.launcher_dt, new_particle)
        new_particle.initial_life = new_particle.life
        self.particles.append(new_particle)

    def _discard_dead_particles(self):
        """Get rid of all no longer active particles (life <= 0)."""
        write_index = 0
        for read_index, particle in enumerate(self.particles):
            if particle.life > 0:
                write_index += 1
                if read_index > write_index:
                    self.particles[write_index] = particle
        del self.particles[write_index:]


class EmitterConstantRate(object):
    """Emit new particles at a constant rate."""
    def __init__(self, rate, limit=None):
        """Emit `rate` particles / second, up to a total `limit` lifetime.

        Arguments:
            rate: Number of particles to emit per second.
            limit: Maximum number of particles to ever emit.
        """
        self.rate = rate
        self.particles_left = limit
        self.remainder = 0

    def __call__(self, dt):
        """How many particles to emit in `dt` seconds.

        Arguments:
            dt: Elapsed time in seconds.
        """
        if self._has_limit and not self.particles_left:
            return None

        exact = self.remainder + dt * self.rate
        count = int(exact)
        self.remainder = exact - count
        if self._has_limit:
            count = max((count, self.particles_left))
            self.particles_left -= count

        return count

    @property
    def _has_limit(self):
        return self.particles_left is not None


class EmitterBurst(object):
    """Emit bursts of particles."""
    def __init__(self, counts_and_delays):
        """Set up the burst.

        Arguments:
            counts_and_delays (iterable): this is an iterable that
                yields pairs of (particle count, delay in seconds) allowing
                you to define multiple bursts, bursts after delays, etc.
        """
        self.iter_counts_and_delays = iter(counts_and_delays)
        self.delay = 0
        self.count = 0

    @classmethod
    def single(cls, count, delay=0):
        """Perform one single burst on particle system creation, launching
        count particles.

        Arguments:
            count: Number of particles to emit.
            delay: Time to wait before burst.
        """
        return cls([(count, delay)])

    @property
    def is_alive(self):
        """Whether it's still creating bursts in the future."""
        return self.delay < INFINITY

    def __call__(self, dt):
        """How many particles to emit in `dt` seconds.

        Arguments:
            dt: Elapsed time in seconds.
        """
        count = 0
        while dt >= self.delay:
            count += self.count
            dt -= self.delay
            self.count, self.delay = next(
                self.iter_counts_and_delays, (INFINITY, 0))
        self.delay -= dt
        if count or self.is_alive:
            return count
        else:
            return None


class PhysicsComposite(object):
    """Perform multiple physics operations in one call."""
    def __init__(self, *physics):
        """Create composite of multiple physics rules.

        Arguments:
            physics (list of physics callables): Physics callables, all of
                which will be applied to particles each frame.
        """
        self.physics = list(physics)

    def add(self, *physics):
        """Add a new physics function.

        Arguments:
            physics (list of physics callables): Physics callables, all of
                which will be applied to particles each frame.
        """
        self.physics.extend(physics)

    def __call__(self, dt, particle):
        """Do all physics updates for `dt` seconds on given particle.

        Arguments:
            dt (float): Elapsed seconds
            particle (Particle): Particle to update.
        """
        for physics in self.physics:
            physics(dt, particle)


class PhysicsInertia(object):
    """Perform inertia on a particle.

    Basically this will add the particle's velocity to position & expend
    the particle's life.
    """
    def __call__(self, dt, particle):
        """Perform inertia updates for `dt` seconds on given particle.

        Arguments:
            dt (float): Elapsed seconds
            particle (Particle): Particle to update.
        """
        particle.x += dt * particle.dx
        particle.y += dt * particle.dy
        particle.life -= dt


class PhysicsJitter(object):
    """Add randomness to particle motion.

    Randomness can be applied to particle coordinates, velocity, or life,
    which is cool.
    """
    def __init__(self, x=0, y=0, dx=0, dy=0, life=0, jitter=None):
        """Define randomness to add.

        Arguments:
            x (float): scale to add x-jitter
            y (float): scale to add y-jitter
            dx (float): scale to add dx-jitter
            dy (float): scale to add dy-jitter
            life (float): scale to add life-jitter
            jitter (callable): random function, taking time delta, returning
                a random float multiplied by each attribute.
        """
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.life = life
        if jitter:
            self.jitter = jitter

    def jitter(self, dt):
        """Default jitter function: just randomness centered at 0"""
        return dt * (random.random() - 0.5)

    def __call__(self, dt, particle):
        """Perform jitter for `dt` seconds on given particle.

        Arguments:
            dt (float): Elapsed seconds
            particle (Particle): Particle to update.
        """
        particle.x += dt * self.x * self.jitter(dt)
        particle.y += dt * self.y * self.jitter(dt)
        particle.dx += dt * self.dx * self.jitter(dt)
        particle.dy += dt * self.dy * self.jitter(dt)
        particle.life += dt * self.life * self.jitter(dt)


class PhysicsKick(object):
    """Kick a particle by adding whatever values to its attributes.

    This is intended for use in launchers, you can define an initial
    velocity for new particles, etc.
    """
    def __init__(self, x=0, y=0, dx=0, dy=0, life=0):
        """Set up values to add to kick particle.

        Arguments:
            x (float): value to add to x per second
            y (float): value to add to y per second
            dx (float): value to add to dx per second
            dy (float): value to add to dy per second
            life (float): value to add to life per second
        """
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.life = life

    @classmethod
    def radial(cls, r, theta):
        """Provide a radial velocity kick.

        Arguments:
            r (float): speed in pixels per second (per second)
            theta (float): angle in degrees (0 = +X axis, 90 = +Y axis)
        """
        radians = math.radians(theta)
        dx = r * math.cos(radians)
        dy = r * math.sin(radians)
        return cls(dx=dx, dy=dy)

    def __call__(self, dt, particle):
        """Perform kick for `dt` seconds on given particle.

        Arguments:
            dt (float): Elapsed seconds
            particle (Particle): Particle to update.
        """
        particle.x += dt * self.x
        particle.y += dt * self.y
        particle.dx += dt * self.dx
        particle.dy += dt * self.dy
        particle.life += dt * self.life


class PhysicsAcceleration(object):
    """Constant acceleration field."""
    def __init__(self, ax, ay):
        """Set up acceleration field.

        Arguments:
            ax (float): Acceleration in positive X direction,
                in pixels / sec / sec.
            ay (float): Acceleration in positive Y direction,
                in pixels / sec / sec.
        """
        self.ax = ax
        self.ay = ay

    @classmethod
    def radial(cls, r, theta):
        """Provide a radial acceleration.

         Arguments:
             r (float): speed in pixels per second (per second)
             theta (float): angle in degrees (0 = +X axis, 90 = +Y axis)
         """
        radians = math.radians(theta)
        ax = r * math.cos(radians)
        ay = r * math.sin(radians)
        return cls(ax=ax, ay=ay)

    def __call__(self, dt, particle):
        """Perform acceleration for `dt` seconds on given particle.

        Arguments:
            dt (float): Elapsed seconds
            particle (Particle): Particle to update.
        """
        particle.dx += dt * self.ax
        particle.dy += dt * self.ay


class ArtistSimple(object):
    """Artist that simply draws an image at each particle position."""
    def __init__(self, image, special_flags=0):
        """Initialize the artist.

        Arguments:
            image (pygame.Surface): Image to draw for each particle.
            special_flags (int): blit flags determining blit mode (normal,
                additive, subtractive, etc)
        """
        self.image = image
        self.special_flags = special_flags

    def __call__(self, surface, particle):
        """Draw given particle on given surface.

        Arguments:
            surface (pygame.Surface): Surface to draw on
            particle (Particle): Particle to draw
        """
        x = int(particle.x - 0.5 * self.image.get_size()[0])
        y = int(particle.y - 0.5 * self.image.get_size()[1])
        surface.blit(self.image, (x, y), special_flags=self.special_flags)


class ArtistFadeOverlay(object):
    """Arist that draws an image, fading between different tints based on
    the particle's lifetime."""
    def __init__(self, image, tints,
                 blit_flags=0, tint_flags=pygame.BLEND_RGBA_MULT):
        """Initialize the artist.

        Arguments:
            image (pygame.Surface): Image to draw for each particle.
            tints (list of 4-tuple colors): Contains multiple 4-tuples,
                each of which indicates an RGBA tint to apply to the image.
                There should be at least two tints: if two are provided,
                the image will fade from the first tint to the second
                over its lifetime (determined by
                `particle.life / particle.initial_life`).  If more than two
                are given, particle will fade between different tints by
                dividing lifetime equally; so for 4 tints, particle will spend
                1/3 its lifetime between the first two, 1/3 between
                the middle two, and 1/3 between the last two.
            blit_flags (int): special flags determining blit mode (normal,
                additive, subtractive, etc) the tinted image will be applied
                to the surface. By default this is normal -- apply the
                image while respecting alpha, etc.)
            tint_flags (int): special flags determining blit mode (normal,
                additive, subtractive, etc) the tint will be applied to
                the image. By default this is multiplicative.
        """
        self.image = image.convert_alpha()
        self.tints = tints
        self.blit_flags = blit_flags
        self.tint_flags = tint_flags

    def __call__(self, surface, particle):
        """Draw given particle on given surface.

        Arguments:
            surface (pygame.Surface): Surface to draw on
            particle (Particle): Particle to draw
        """
        overlay = self.image.copy()
        tint = self._calculate_tint(particle)

        overlay.fill(tint, special_flags=self.tint_flags)
        x = int(particle.x - 0.5 * self.image.get_size()[0])
        y = int(particle.y - 0.5 * self.image.get_size()[1])
        surface.blit(overlay, (x, y), special_flags=self.blit_flags)

    def _calculate_tint(self, particle):
        """Calculate tint to apply to particle."""
        life_fraction = 1 - particle.life * 1.0 / particle.initial_life
        if life_fraction > 1:
            life_fraction = 1
        elif life_fraction < 0:
            life_fraction = 0
        index = life_fraction * (len(self.tints) - 1)
        floor = int(index)
        remainder = index - floor
        if remainder > 0:
            tint = tuple([
                int(a * (1 - remainder) + b * remainder)
                for a, b in zip(self.tints[floor], self.tints[floor+1])
            ])
        else:
            tint = self.tints[floor]
        return tint
