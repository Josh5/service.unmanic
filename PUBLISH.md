
# Update branch
git fetch unmanic
git checkout unmanic_release
git pull unmanic


git read-tree --prefix=service.unmanic/ -u unmanic_release
# OR
git pull --strategy subtree --squash unmanic release --allow-unrelated-histories



## Updating existing PR:

git pull --strategy subtree --squash unmanic release --allow-unrelated-histories
git commit --amend
git push origin matrix
