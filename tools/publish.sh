#!/bin/bash
#!/usr/bin/python

####################
# Variables
####################
# PATHS
HERE="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BUILD="$HERE"/build
SRC="$(dirname "$HERE")"
DEST="$SRC"/_site
TEMP="$SRC"/.temp

SOURCE_DIR="${1:-"$SRC"}"
PUBLISH_DIR="${2:-"$DEST"}"

# Git Branches
SOURCE_BRANCH="main"
PUBLISH_BRANCH="published"

####################
# Initialize
####################
printf "\n\033[0;32mInitializing...\033[0m\n"
# Anything needed here?

####################
# Commit Source
####################
# Commit to remote branch
printf "\n\033[0;32mEnter source commit description:\033[0m\n"
read DESC
cd "$SOURCE_DIR" &&
  git add --all . &&
  git commit -am "$DESC" &&
  git push -u origin "$SOURCE_BRANCH"

####################
# Publish Build
####################
# Check out tree branch
printf "\n\033[0;32mCreating tree branch for $PUBLISH_BRANCH...\033[0m\n"
git worktree add "$DEST" "$PUBLISH_BRANCH" # Create dir if needed
rm -rf -- "$DEST"/* # Remove all files from previous branch commit, except for .*

# Build website
printf "\n\033[0;32mGenerating site...\033[0m\n"
python "$BUILD"/build-site.py # TO-DO: Have src and dir parameters configured by this script

# Copy build contents to temporary directory
#cp -r "$PUBLISH_DIR"/. "$DEST"/

# Commit to remote branch
printf "\n\033[0;32mDeploying site to $PUBLISH_BRANCH branch...\033[0m\n"
cd "$DEST" &&
  git add --all . &&
  git commit -a --amend --no-edit && # Replace HEAD
  git push -fu origin "$PUBLISH_BRANCH" # Force push

####################
# Cleanup
####################
printf "\n\033[0;32mCleaning up...\033[0m\n"
cd "$SOURCE_DIR"
git worktree remove -f "$DEST" # Remove Git worktree and dir
cd "$HERE" # Return to original directory

# Final Status
printf "\n\033[0;32mFinished!\033[0m\n"
cmd /k # ~optional~