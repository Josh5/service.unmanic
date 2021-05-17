# Just some docs for me to refer to when publishing to teh official repo


## Initial setup Update branch
```
# Fetch fork of main repo
git clone git@github.com:Josh5/repo-scripts.git
cd repo-scripts

# Add my add-on as a remote
git remote add unmanic git@github.com:Josh5/service.unmanic.git

# Fetch changes on my add-on repo
git fetch unmanic

# Checkout my add-on repo as a new branch
git checkout -b unmanic_release unmanic/release

# Update this new branch
git pull unmanic
```


## Adding addon for first time
Only do this if the directory does not already exist in the main repo
```
# Checkout the official branch
git checkout matrix

# Create branch of offical branch
git checkout -b matrix-service.unmanic

# Use subtree to place addon into main repo tree
git read-tree --prefix=service.unmanic/ -u unmanic_release



## Updating existing PR:
```
# Checkout the official branch
git checkout matrix

# Create branch of offical branch
git checkout matrix-service.unmanic

# Fetch the latest changes
git pull --strategy subtree --squash unmanic release --allow-unrelated-histories

# Amend the previous commit
git commit --amend

# Force push (only one commit per PR)
git push -f origin matrix-service.unmanic
```
