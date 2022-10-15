#!/bin/bash

source_dir = ../
publish_dir = ../_site
source_branch = main
publish_branch = published

build_command() {
  build/build-site.py
}

#echo -e "\033[0;32mDeleting old content...\033[0m"
#rm -rf $publish_dir

echo -e "\033[0;32mChecking out $publish_branch....\033[0m"
git worktree add $publish_dir $publish_branch

echo -e "\033[0;32mGenerating site...\033[0m"
build_command

echo -e "\033[0;32mDeploying site to $publish_branch branch...\033[0m"
cd $publish_dir &&
  git add --all &&
  git commit -m "Deploy updates" &&
  git push origin $publish_branch

#echo -e "\033[0;32mCleaning up...\033[0m"
#git worktree remove $publish_dir