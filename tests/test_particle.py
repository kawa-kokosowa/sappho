import unittest
from sappho import particle


class TestParticle(unittest.TestCase):
    def test_particle_construction(self):
        p = particle.Particle(-1, +1, +2, -2, +5, 'spark')
        self.assertEquals(p.x, -1)
        self.assertEquals(p.y, +1)
        self.assertEquals(p.dx, +2)
        self.assertEquals(p.dy, -2)
        self.assertEquals(p.life, +5)
        self.assertEquals(p.species, 'spark')


class TestParticleSystem(unittest.TestCase):
    def test_one_particle(self):
        # start it
        ps = particle.ParticleSystem(
            particle.Particle(0, -1, 1, 0, 3, 'giblet'),
            particle.EmitterBurst.single(1)
        )
        self.assertEquals(len(ps.particles), 0)

        # advance 1 second
        ps.update_state(1)
        self.assertEquals(len(ps.particles), 1, 'Particle not created')
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
        # Keep `p` from previous call
        self.assertEquals(p.x, 3)     # Moved yet another unit in +x direction
        self.assertEquals(p.y, -1)    # still unchanged
        self.assertEquals(p.dx, 1)
        self.assertEquals(p.dy, 0)
        self.assertEquals(p.life, 0)  # Lost all life
        self.assertEquals(p.species, 'giblet')


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


class TestEmitterBurst(unittest.TestCase):
    def test_single_burst(self):
        # Emit 100 particles after ten seconds
        emitter = particle.EmitterBurst.single(100, 10)
        self.assertEquals(emitter(5.2), 0)
        self.assertEquals(emitter(4.9), 100)
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

if __name__ == '__main__':
    unittest.main()
