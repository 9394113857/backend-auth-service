# =========================================
# GENERAL: Rename any branch (local + remote)
# =========================================

# Step 1: Switch to the branch you want to rename
git checkout <old-branch-name>

# Step 2: Rename locally
git branch -m <new-branch-name>

# Step 3: Push new branch + set upstream (combined step)
git push -u origin <new-branch-name>

# Step 4: Delete old branch from remote
git push origin --delete <old-branch-name>

# Step 5: Verify
git branch      # local branches
git branch -r   # remote branches

# =========================================
# DONE ✅ Branch renamed successfully
# =========================================
