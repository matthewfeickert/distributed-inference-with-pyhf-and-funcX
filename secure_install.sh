#!/bin/bash

# Ensure there is a lockfile to install from
if [ ! -f requirements.lock ]; then
    if [ -f compile_dependencies.sh ]; then
        echo "# Generating requirements.lock from compile_dependencies.sh"
        bash compile_dependencies.sh
    else
        echo "Missing requirements.lock."
        echo "Please generate one with 'pip-tools compile'"
        return 1
    fi
fi

# Use Brett Cannon's recommendations for pip-secure-install to ensure environment
# is reproducible and installed as securely as possible.
# c.f. https://www.python.org/dev/peps/pep-0665/#secure-by-design
# c.f. https://github.com/brettcannon/pip-secure-install
# c.f. https://twitter.com/brettsky/status/1486137764315688961
python -m pip install \
    --no-deps \
    --require-hashes \
    --only-binary :all: \
    --no-binary jax \
    --requirement requirements.lock
