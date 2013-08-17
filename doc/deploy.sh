# Sequence of commands used to deploy content to gh-pages branch.

git checkout gh-pages
rm -rf *
git checkout master doc
git reset HEAD
mv doc/* .
rm -rf doc
rm -rf deploy.sh logo.xcf
git add .
git commit -m "Updated gh-pages for `git log master -1 | head -1`"
#git push
