#!/bin/bash
# Clone the Sappho repository's gh-pages branch, remove everything in it,
# regenerate the documentation, commit, and push.
#
# Commit messages are of the format: [docpush] Generated at YYYY-mm-dd HH:MM
#
# Use --dry-run to commit but not push, this will print the temporary
# directory and not delete it when the script exits

shopt -s extglob

REPOSITORY="git@github.com:hypatia-software-org/sappho.git"
BRANCH="gh-pages"

function die() {
    echo "!! An error occurred:"
    echo "!! $@"
    if [[ "x$TMPDIR" != "x" ]]; then
        echo "!! The cloned repository will not be deleted and will remain"
        echo "!! at $TMPDIR"
    fi
    exit 1
}

# Runtime options
DRY_RUN=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            echo "Usage: $0 [--help] [--dry-run]"
            exit
            ;;
        -d|--dry-run)
            DRY_RUN=1
            ;;
        *)
            echo "Unknown argument \"$1\""
            exit 1
            ;;
    esac
    shift
done

if [[ $DRY_RUN -eq 1 ]]; then
    echo "!! Dry run, will not push changes"
fi

DOCSDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMPDIR=$(mktemp -d)

echo ">> Cloning repository..."
git clone "$REPOSITORY" "$TMPDIR/sappho" -b "$BRANCH" >/dev/null || die "Git clone failed"

pushd "$TMPDIR/sappho" >/dev/null 2>/dev/null

echo ">> Building documentation..."
rm -r !(.|..|.git|CNAME|.nojekyll)
sphinx-build -b html "$DOCSDIR" . >/dev/null || die "Sphinx build failed"

echo ">> Committing..."
git add -A
git commit -m "[docpush] Generated at $(date +'%F %H:%M')" || die "Git commit failed"

if [[ $DRY_RUN -eq 0 ]]; then
    echo ">> Pushing..."
    git push origin gh-pages || die "Git push failed" 
    rm -rf "$TMPDIR"
else
    echo "!! Completed dry run."
    echo "!! Repository is at $TMPDIR/sappho"
fi

popd >/dev/null 2>/dev/null