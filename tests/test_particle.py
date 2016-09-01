import itertools
import unittest
from sappho import particle
import pygame
from .common import compare_surfaces


class ArtistNull(object):
    def __init__(self):
        self.count = 0
        self.last_particle = None

    def __call__(self, surface, particle):
        self.count += 1
        self.last_particle = particle


class TestParticle(unittest.TestCase):
    def test_particle_construction(self):
        p = particle.Particle(-1, +1, +2, -2, +5, 'spark')
        self.assertEquals(p.x, -1)
        self.assertEquals(p.y, +1)
        self.assertEquals(p.dx, +2)
        self.assertEquals(p.dy, -2)
        self.assertEquals(p.life, +5)
        self.assertEquals(p.species, 'spark')

    def test_particle_repr(self):
        p = particle.Particle(-1, +1, +2, -2, +5, 'spark')
        r = repr(p)
        self.assertEquals(
            r, 'Particle(-1, 1, dx=2, dy=-2, life=5, species=\'spark\')'
        )


class TestParticleSystem(unittest.TestCase):
    def test_one_particle(self):
        # start it
        ps = particle.ParticleSystem(
            particle.Particle(0, -1, 1, 0, 3, 'giblet'),
            particle.EmitterBurst.single(1)
        )
        self.assertEquals(len(ps.particles), 0)
        self.assertTrue(ps.is_alive())

        # advance 1 second
        ps.update_state(1)
        self.assertEquals(len(ps.particles), 1, 'Particle not created')
        self.assertTrue(ps.is_alive())
        p = ps.particles[0]
        self.assertEquals(p.x, 1)     # Moved one unit in +x direction
        self.assertEquals(p.y, -1)    # unchanged
        self.assertEquals(p.dx, 1)
        self.assertEquals(p.dy, 0)
        self.assertEquals(p.life, 2)  # Lost one second of life
        self.assertEquals(p.species, 'giblet')

        # advance another second to t=2
        ps.update_state(1)
        self.assertEquals(len(ps.particles), 1, 'Particle killed too early')
        self.assertTrue(ps.is_alive())
        p = ps.particles[0]
        self.assertEquals(p.x, 2)     # Moved another unit in +x direction
        self.assertEquals(p.y, -1)    # unchanged
        self.assertEquals(p.dx, 1)
        self.assertEquals(p.dy, 0)
        self.assertEquals(p.life, 1)  # Lost another second of life
        self.assertEquals(p.species, 'giblet')

        # advance another second to t=3
        ps.update_state(1)
        self.assertEquals(len(ps.particles), 0,
                          'Particle not destroyed when life=0')
        self.assertFalse(ps.is_alive())
        # Keep `p` from previous call
        self.assertEquals(p.x, 3)     # Moved yet another unit in +x direction
        self.assertEquals(p.y, -1)    # still unchanged
        self.assertEquals(p.dx, 1)
        self.assertEquals(p.dy, 0)
        self.assertEquals(p.life, 0)  # Lost all life
        self.assertEquals(p.species, 'giblet')

    def test_particle_death(self):
        # start it
        # Particles alive for 3 seconds, one generated every two seconds
        ps = particle.ParticleSystem(
            particle.Particle(0, -1, 1, 0, 3, 'giblet'),
            particle.EmitterBurst.repeat(1, 2)
        )
        ps.update_state(1)
        self.assertEquals(len(ps.particles), 1)
        print(ps.particles)
        ps.update_state(1)
        self.assertEquals(len(ps.particles), 2)
        print(ps.particles)
        p1, p2 = ps.particles
        ps.update_state(1)
        self.assertEquals(len(ps.particles), 1)
        print(ps.particles)
        self.assertIs(p2, ps.particles[0])

    def test_draw_three_particles(self):
        # start it
        artist = ArtistNull()
        ps = particle.ParticleSystem(
            particle.Particle(0, -1, 1, 0, 3, 'giblet'),
            particle.EmitterBurst.single(3),
            artist=artist,
        )
        # advance 1 second
        ps.update_state(1)
        ps.draw_on(None)

        self.assertEquals(artist.count, 3)
        self.assertEquals(artist.last_particle, ps.particles[-1])


class TestEmitterConstantRate(unittest.TestCase):
    def test_emitter(self):
        emitter = particle.EmitterConstantRate(10)
        self.assertEquals(emitter(5.0), 50)
        self.assertEquals(emitter(1.0), 10)
        self.assertEquals(emitter(1.5), 15)
        self.assertEquals(emitter(9.0), 90)

    def test_emitter_with_limit(self):
        emitter = particle.EmitterConstantRate(10, limit=70)
        self.assertEquals(emitter(5.0), 50)
        self.assertEquals(emitter(1.0), 10)
        self.assertEquals(emitter(1.5), 10)
        self.assertLess(emitter(9.0), 0)


class TestEmitterComposite(unittest.TestCase):
    def test_two_bursts(self):
        emitter = particle.EmitterComposite(
            particle.EmitterBurst.single(100, 10),
            particle.EmitterBurst.single(200, 20),
        )
        self.assertEquals(emitter(5), 0)
        self.assertEquals(emitter(5), 100)
        self.assertEquals(emitter(15), 200)
        self.assertLess(emitter(1), 0)
        self.assertLess(emitter(1), 0)

    def test_two_bursts_alt_construction(self):
        emitter = particle.EmitterComposite().add(
            particle.EmitterBurst.single(100, 10),
            particle.EmitterBurst.single(200, 20),
        )
        self.assertEquals(emitter(5), 0)
        self.assertEquals(emitter(5), 100)
        self.assertEquals(emitter(15), 200)
        self.assertLess(emitter(1), 0)
        self.assertLess(emitter(1), 0)


class TestEmitterBurst(unittest.TestCase):
    def test_single_burst(self):
        # Emit 100 particles after ten seconds
        emitter = particle.EmitterBurst.single(100, 10)
        self.assertEquals(emitter(5.2), 0)
        self.assertEquals(emitter(4.9), 100)
        self.assertLess(emitter(0.1), 0)
        self.assertLess(emitter(0.1), 0)

    def test_repeated_bursts(self):
        # Emit 100 particles every ten seconds
        emitter = particle.EmitterBurst.repeat(100, 10)
        self.assertEquals(emitter(5.2), 100)
        self.assertEquals(emitter(4.9), 100)
        self.assertEquals(emitter(22.0), 200)
        self.assertEquals(emitter(1.0), 0)
        self.assertEquals(emitter(22.0), 200)

    def test_repeated_bursts_with_delay(self):
        # Emit 100 particles every ten seconds
        emitter = particle.EmitterBurst.repeat(100, 10, delay=6)
        self.assertEquals(emitter(5.2), 0)
        self.assertEquals(emitter(4.9), 100)
        self.assertEquals(emitter(22.0), 200)
        self.assertEquals(emitter(1.0), 0)
        self.assertEquals(emitter(22.0), 200)


class TestPhysicsComposite(unittest.TestCase):
    def test_composite_kicks(self):
        physics = particle.PhysicsComposite(
            particle.PhysicsKick(x=2),
            particle.PhysicsKick(y=5),
        )
        p = particle.Particle(x=100, y=100)
        self.assertEquals(p.x, 100)
        self.assertEquals(p.y, 100)
        physics(1, p)
        self.assertEquals(p.x, 102)
        self.assertEquals(p.y, 105)
        physics(3, p)
        self.assertEquals(p.x, 108)
        self.assertEquals(p.y, 120)

    def test_composite_alt_constructor(self):
        physics = particle.PhysicsComposite().add(
            particle.PhysicsKick(x=2),
            particle.PhysicsKick(y=5),
        )
        p = particle.Particle(x=100, y=100)
        self.assertEquals(p.x, 100)
        self.assertEquals(p.y, 100)
        physics(1, p)
        self.assertEquals(p.x, 102)
        self.assertEquals(p.y, 105)
        physics(3, p)
        self.assertEquals(p.x, 108)
        self.assertEquals(p.y, 120)


class TestPhysicsInertia(unittest.TestCase):
    def test_inertia(self):
        physics = particle.PhysicsInertia()

        p = particle.Particle(0, -1, 1, 0, 3, 'giblet')

        # advance 1 second
        physics(1, p)
        self.assertEquals(p.x, 1)  # Moved one unit in +x direction
        self.assertEquals(p.y, -1)  # unchanged
        self.assertEquals(p.dx, 1)
        self.assertEquals(p.dy, 0)
        self.assertEquals(p.life, 2)  # Lost one second of life
        self.assertEquals(p.species, 'giblet')

        # advance another two seconds to t=3
        physics(2, p)
        self.assertEquals(p.x, 3)  # Moved yet another unit in +x direction
        self.assertEquals(p.y, -1)  # still unchanged
        self.assertEquals(p.dx, 1)
        self.assertEquals(p.dy, 0)
        self.assertEquals(p.life, 0)  # Lost all life
        self.assertEquals(p.species, 'giblet')


class TestPhysicsJitter(unittest.TestCase):
    def test_jitter(self):
        # Jitter cycles between +1 & -1 times time delta
        jitter_iter = itertools.cycle((1, -1))

        def jitter(dt):
            return dt * next(jitter_iter)

        physics = particle.PhysicsJitter(y=2, jitter=jitter)
        p = particle.Particle(0, 0)
        self.assertEquals(p.y, 0)

        # Jitter one second; uses jitter value 1 * 1 second * scale 2, +2 to y
        physics(1, p)
        self.assertEquals(p.y, 2)

        # Jitter 2s; uses jitter value -1 * 2 second * scale 2, -4 to y
        physics(2, p)
        self.assertEquals(p.y, -2)

        # Jitter 5s; uses jitter value 1 * 5 second * scale 2, +10 to y
        physics(5, p)
        self.assertEquals(p.y, 8)

    def test_brownian(self):
        # Not much we can test here, just that it works
        physics = particle.PhysicsJitter(
            x=1,
            jitter=particle.PhysicsJitter.brownian
        )

        p = particle.Particle(0, 0)
        physics(1, p)
        self.assertEquals(p.y, 0)  # y unchanged :P


class TestPhysicsKick(unittest.TestCase):
    def test_kick(self):
        physics = particle.PhysicsKick(x=2, y=5)

        p = particle.Particle(x=100, y=100)
        self.assertEquals(p.x, 100)
        self.assertEquals(p.y, 100)
        physics(1, p)
        self.assertEquals(p.x, 102)
        self.assertEquals(p.y, 105)
        physics(3, p)
        self.assertEquals(p.x, 108)
        self.assertEquals(p.y, 120)


class TestPhysicsAcceleration(unittest.TestCase):
    def test_acceleration(self):
        # Accelerating +3 in dx direction
        physics = particle.PhysicsAcceleration(3, 0)

        p = particle.Particle(0, 0, dx=100, dy=100)
        self.assertEquals(p.dx, 100)
        self.assertEquals(p.dy, 100)
        physics(1, p)
        self.assertEquals(p.dx, 103)
        self.assertEquals(p.dy, 100)
        physics(3, p)
        self.assertEquals(p.dx, 112)
        self.assertEquals(p.dy, 100)

    def test_acceleration_radial(self):
        # Radial indicating +2 in dy direction
        physics = particle.PhysicsAcceleration.radial(2, 90)

        p = particle.Particle(0, 0, dx=100, dy=100)
        self.assertEquals(p.dx, 100)
        self.assertEquals(p.dy, 100)
        physics(1, p)
        self.assertEquals(p.dx, 100)
        self.assertEquals(p.dy, 102)
        physics(3, p)
        self.assertEquals(p.dx, 100)
        self.assertEquals(p.dy, 108)


class TestArtistSimple(unittest.TestCase):
    def test_artist_draw_origin(self):
        block = pygame.surface.Surface((2, 2))
        block.fill((255, 0, 0), pygame.Rect(0, 0, 2, 2))

        ps = particle.ParticleSystem(
            particle.Particle(0, 1, 1, 0, 3, 'pixel'),
            particle.EmitterBurst.single(1),
            artist=particle.ArtistSimple(block, (0, 0)),
        )
        world = pygame.surface.Surface((4, 4))
        world.fill((0, 255, 0), pygame.Rect(0, 0, 4, 4))

        desired_world = pygame.surface.Surface((4, 4))
        desired_world.fill((0, 255, 0), pygame.Rect(0, 0, 4, 4))
        for x in (1, 2):
            for y in (1, 2):
                desired_world.set_at((x, y), (255, 0, 0))

        ps.update_state(1)
        ps.draw_on(world)
        assert(compare_surfaces(desired_world, world))

    def test_artist_draw_center(self):
        block = pygame.surface.Surface((2, 2))
        block.fill((255, 0, 0), pygame.Rect(0, 0, 2, 2))

        ps = particle.ParticleSystem(
            particle.Particle(0, 1, 1, 0, 3, 'pixel'),
            particle.EmitterBurst.single(1),
            artist=particle.ArtistSimple(
                block, particle.CENTER
            ),
        )
        world = pygame.surface.Surface((4, 4))
        world.fill((0, 255, 0), pygame.Rect(0, 0, 4, 4))

        desired_world = pygame.surface.Surface((4, 4))
        desired_world.fill((0, 255, 0), pygame.Rect(0, 0, 4, 4))
        for x in (0, 1):
            for y in (0, 1):
                desired_world.set_at((x, y), (255, 0, 0))

        ps.update_state(1)
        ps.draw_on(world)
        assert(compare_surfaces(desired_world, world))


class TestArtistFadeOverlay(unittest.TestCase):
    def test_artist_draw_origin(self):
        block = pygame.surface.Surface((2, 2))
        block.fill((255, 0, 0), pygame.Rect(0, 0, 2, 2))

        ps = particle.ParticleSystem(
            particle.Particle(0, 1, 1, 0, 3, 'pixel'),
            particle.EmitterBurst.single(1),
            artist=particle.ArtistFadeOverlay(
                block, (0, 0),
                [(255, 255, 255, 255), (255, 255, 255, 255)]
            ),
        )
        world = pygame.surface.Surface((4, 4))
        world.fill((0, 255, 0), pygame.Rect(0, 0, 4, 4))

        desired_world = pygame.surface.Surface((4, 4))
        desired_world.fill((0, 255, 0), pygame.Rect(0, 0, 4, 4))
        for x in (1, 2):
            for y in (1, 2):
                # Ugh this is only 254 for some reason
                # get it together pygame
                desired_world.set_at((x, y), (254, 0, 0))

        ps.update_state(1)
        ps.draw_on(world)
        assert(compare_surfaces(desired_world, world))

    def test_artist_draw_center(self):
        block = pygame.surface.Surface((2, 2))
        block.fill((255, 0, 0), pygame.Rect(0, 0, 2, 2))

        ps = particle.ParticleSystem(
            particle.Particle(0, 1, 1, 0, 3, 'pixel'),
            particle.EmitterBurst.single(1),
            artist=particle.ArtistFadeOverlay(
                block, particle.CENTER,
                [(255, 255, 255, 255), (255, 255, 255, 255)]
            ),
        )
        world = pygame.surface.Surface((4, 4))
        world.fill((0, 255, 0), pygame.Rect(0, 0, 4, 4))

        desired_world = pygame.surface.Surface((4, 4))
        desired_world.fill((0, 255, 0), pygame.Rect(0, 0, 4, 4))
        for x in (0, 1):
            for y in (0, 1):
                # Ugh this is only 254 for some reason
                # get it together pygame
                desired_world.set_at((x, y), (254, 0, 0))

        ps.update_state(1)
        ps.draw_on(world)

        print(world.get_at((1, 1)))
        assert(compare_surfaces(desired_world, world))

    def test_calculate_tint(self):
        block = pygame.surface.Surface((2, 2))
        block.fill((255, 0, 0), pygame.Rect(0, 0, 2, 2))

        artist = particle.ArtistFadeOverlay(
            block, particle.CENTER,
            [(10, 10, 10, 255), (20, 20, 20, 255), (40, 40, 40, 255)]
        )
        low_life_tint = artist.calculate_tint(-0.5, 10)
        self.assertEquals(low_life_tint, (40, 40, 40, 255))
        high_life_tint = artist.calculate_tint(10.5, 10)
        self.assertEquals(high_life_tint, (10, 10, 10, 255))


if __name__ == '__main__':
    unittest.main()
