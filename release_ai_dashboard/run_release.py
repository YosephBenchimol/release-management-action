# run_release.py

import sys
from auto_generate import main

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_release.py <version_tag>")
        sys.exit(1)

    version_tag = sys.argv[1]
    main(version_tag)
