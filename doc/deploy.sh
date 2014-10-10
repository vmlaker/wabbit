# Sequence of commands used to deploy content to gh-pages branch.

git checkout gh-pages
rm -rf *
git checkout master doc
git reset HEAD
mv doc/* .
rm -rf doc
rm -rf deploy.sh forkme.xcf logo.xcf tile.xcf
git add .

# Sanity check before commit.
git status

git commit -m "Updated gh-pages for `git log master -1 | head -1`"
git push origin gh-pages
git checkout master
