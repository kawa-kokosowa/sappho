# ![Sappho Logo (A Lyre)](sappho-logo.png)

The purpose of this repo is to rewrite Hypatia Engine
and eventually replace Hypatia Engine as "Sappho."

Sorry I haven't had time to clean anything yet.

## Design Philosophy

  1. Don't interfere with the way people build their pygame games
  2. We are not automating game logic
  3. Sappho modules _may not_ import other Sappho modules
  4. Inherit from pygame objects when possible; use conventional
     pygame models/architecture.
  5. Consistency.
  6. Simplicity trumps all else.
  7. Well documented.

For more details see `CONTRIBUTING.md`.
