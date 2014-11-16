# Sequence of commands used to deploy content to gh-pages branch.

# 1) Start from "clean all".
scons bites=../bites -j 9 -c . doc

# 2) Then, build all.
scons bites=../bites -j 9 . doc

# 3) Sanity check, may have to add any new files in doc/ directory.
git status

git checkout gh-pages
find . -maxdepth 1 ! -name '.git*' | xargs rm -rf
git checkout master doc
git reset HEAD
mv doc/* .
rm -rf doc
rm -rf deploy.sh forkme.xcf tile.xcf
git add .

# Sanity check before commit.
# May have to run "git add --all ." 
git status

git commit -m "Updated gh-pages for `git log master -1 | head -1`"
git push origin gh-pages
git checkout master
