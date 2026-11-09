"""A stand-in for the slow part of a real pipeline.

The unit tests of this repository finish in under a second, which leaves a /loop
nothing to wait for. Real pipelines spend minutes on integration suites, image
builds and smoke deploys; this step simulates that wait, and says so in the log.
It checks nothing.
"""

import sys
import time

SECONDS = int(sys.argv[1]) if len(sys.argv) > 1 else 75

for elapsed in range(0, SECONDS, 15):
    print(f"simulated integration stage: {elapsed}s of {SECONDS}s", flush=True)
    time.sleep(min(15, SECONDS - elapsed))
print("simulated integration stage: done (this step checks nothing)")
