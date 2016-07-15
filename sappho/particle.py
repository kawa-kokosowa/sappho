from __future__ import division
import copy
import math
import random

import pygame


class Particle(object):
    __slots__ = ['x', 'y', 'dx', 'dy', 'life', 'species', 'initial_life']

    def __init__(self, x, y, dx=0, dy=0, life=0, species=None):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.life = life
        self.species = species
        self.initial_life = life


class EmitterConstantRate(object):
    def __init__(self, rate, limit=None):
        self.rate = rate
        self.particles_left = limit
        self.remainder = 0

    @property
    def has_limit(self):
        return self.particles_left is not None

    def __call__(self, dt):
        if self.has_limit and not self.particles_left:
            return None

        exact = self.remainder + dt * self.rate
        count = int(exact)
        self.remainder = exact - count
        if self.has_limit:
            count = max((count, self.particles_left))
            self.particles_left -= count

        return count


class PhysicsComposite(object):
    def __init__(self, *physics):
        self.physics = list(physics)

    def add(self, physics):
        self.physics.append(physics)

    def __call__(self, dt, particle):
        for physics in self.physics:
            physics(dt, particle)


class PhysicsInertia(object):
    def __init__(self, scale=1):
        self.scale = scale

    def __call__(self, dt, particle):
        particle.x += self.scale * dt * particle.dx
        particle.y += self.scale * dt * particle.dy
        particle.life -= self.scale * dt


class PhysicsBounce(object):
    def __init__(self, x=0, y=0, value=0, bounce=1):
        norm = math.sqrt(x ** 2 + y ** 2)
        self.x = x / norm
        self.y = y / norm
        self.value = value / norm
        self.bounce = bounce

    def __call__(self, dt, particle):
        value = particle.x * self.x + particle.y * self.y - self.value
        if value < 0:
            particle.x += 2 * self.x * -value
            particle.y += 2 * self.y * -value
            dvalue = particle.dx * self.x + particle.dy * self.y
            if dvalue < 0:
                particle.dx = (particle.dx -2 * dvalue * self.x) * self.bounce
                particle.dy = (particle.dy -2 * dvalue * self.y) * self.bounce


class PhysicsJitter(object):
    def __init__(self, x=0, y=0, dx=0, dy=0, life=0, jitter=None):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.life = life
        if jitter:
            self.jitter = jitter

    def jitter(self, dt):
        return random.random() - 0.5

    def __call__(self, dt, particle):
        particle.x += dt * self.x * self.jitter(dt)
        particle.y += dt * self.y * self.jitter(dt)
        particle.dx += dt * self.dx * self.jitter(dt)
        particle.dy += dt * self.dy * self.jitter(dt)
        particle.life += dt * self.life * self.jitter(dt)


class PhysicsKick(object):
    def __init__(self, x=0, y=0, dx=0, dy=0, life=0):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.life = life

    @classmethod
    def radial(cls, r, theta, circle=360.0):
        radians = 2.0 * math.pi * theta / circle
        dx = r * math.cos(radians)
        dy = r * math.sin(radians)
        return cls(dx=dx, dy=dy)

    def __call__(self, dt, particle):
        particle.x += dt * self.x
        particle.y += dt * self.y
        particle.dx += dt * self.dx
        particle.dy += dt * self.dy
        particle.life += dt * self.life


class PhysicsAcceleration(object):
    def __init__(self, ax, ay):
        self.ax = ax
        self.ay = ay

    @classmethod
    def radial(cls, r, theta, circle=360.0):
        radians = 2 * math.pi * theta / circle
        ax = r * math.cos(radians)
        ay = r * math.sin(radians)
        return cls(ax=ax, ay=ay)

    def __call__(self, dt, particle):
        particle.dx += dt * self.ax
        particle.dy += dt * self.ay


class ParticleSystem(object):
    def __init__(
            self, origin_particle, emitter, launcher,
            physics=None,
            drawer=None,
            launcher_dt=1.0,
            particle_limit=512,
    ):
        self.origin = origin_particle
        self.emitter = emitter
        self.launcher = launcher
        self.launcher_dt = launcher_dt
        self.physics = physics or PhysicsInertia()
        self.is_emitting = True
        self.drawer = drawer
        self.particle_limit = particle_limit
        self.particles = list()

    def is_alive(self):
        return self.particles or self.is_emitting

    def update_state(self, dt):
        for particle in self.particles:
            self.physics(dt, particle)
        self.discard_dead_particles()
        new_particle_count = self.get_new_particle_count(dt)
        for _ in range(new_particle_count):
            self.emit()

    def get_new_particle_count(self, dt):
        desired_particle_count = self.emitter(dt)
        self.is_emitting = desired_particle_count is not None
        particle_slots_available = self.particle_limit - len(self.particles)
        return min(desired_particle_count or 0, particle_slots_available)

    def emit(self):
        new_particle = copy.copy(self.origin)
        self.launcher(self.launcher_dt, new_particle)
        new_particle.initial_life = new_particle.life
        self.particles.append(new_particle)

    def discard_dead_particles(self):
        write_index = 0
        for read_index, particle in enumerate(self.particles):
            if particle.life > 0:
                write_index += 1
                if read_index > write_index:
                    self.particles[write_index] = particle
        del self.particles[write_index:]

    def draw_on(self, surface):
        for particle in self.particles:
            self.drawer.draw(surface, particle)


class DrawerSimple(object):
    def __init__(self, image, special_flags=0):
        self.image = image
        self.special_flags = special_flags

    def draw(self, surface, particle):
        x = int(particle.x - 0.5 * self.image.get_size()[0])
        y = int(particle.y - 0.5 * self.image.get_size()[1])
        surface.blit(self.image, (x, y), special_flags=self.special_flags)


class DrawerFadeOverlay(object):
    def __init__(self, image, tints, special_flags=0):
        self.image = image.convert_alpha()
        self.tints = tints
        self.special_flags = special_flags

    def draw(self, surface, particle):
        overlay = self.image.copy()
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

        overlay.fill(tint, special_flags=pygame.BLEND_RGBA_MULT)
        x = int(particle.x - 0.5 * self.image.get_size()[0])
        y = int(particle.y - 0.5 * self.image.get_size()[1])
        surface.blit(overlay, (x, y), special_flags=self.special_flags)
