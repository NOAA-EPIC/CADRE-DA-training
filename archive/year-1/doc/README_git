#################################################################################

* Submitting pull requests to offline_land_workflow

1) Each pull request should have an associated issue. Create a draft pull request as soon as you start working on a new issue, and select the "DRAFT: do not merge" option from the labels. You should then regularly push commits to your branch, making sure to provide a useful description of the commit in the comments. 

2) Before converting your PR from draft mode: 
- make sure that the DA_IMS_test passes, or that different output is expected. See README.md for instructions on runnung the test. 
- either on command line, or through the web browser double check all differences between your PR and the current develop. Make sure that your PR does not include any unnecessary changes / change to default behaviour. 
- edit your .gitmodules to point at the original repos, and not to your version.

3) Give your PR a name that clearly identifies it. Likewise, give your branches identifying names.

4) Add comments to the PR briefly listing all the changes that have been made (i.e. "fixed bug in WHATEVER_VARIABLE, added SMAP observation assimilation, ..."), and link every PR to an issue.

5) If you need to submit PRs to multiple repos, give them the same name and note in the comments that they're linked.

ADDITIONAL INFO ON GIT: 

* To clone and commit code with submodules

1) using the web interface, fork any modules that you will be editing.

2) create a branch within your fork, with an informative name ( use this format: feauture/BRANCH_NAME, or bugfix/BRANCH_NAME)

3) clone the parent repo and update the .gitmodules to point to your code

>git clone YOUR_REPO
>cd YOUR_REPO
>update .gitmodules to point to your forks/branches
>git submodule update --init --recursive

(note: DA_update also has submodules. same process for .gitmodules in that repo if you need to change these).

4) Make your code changes.

5) commit changes to each submodule, starting at the lowest level and working your way up (to the parent repo).

If you have committed changes to a submodule, you will need to commit the updated submodule in the parent module.

>cd SUBMODULE
>git add FILES
>git commit
>cd ..
>git add SUBMODULE   <-- here.
>git commit

6) when pushing your updates, this option is useful to check that the necesary submodules have been pushed:
> git push --recurse-submodules=check

* To merge the latest remote changes into your local clone:

Note that the submodules are cloned as a specific hash of their branch. This has is not necessarily the head of the branch.
When merging the latest remote upcates you need to merge to the submodules hash used by the parent repo, not to the head of the submodule branch (see below).
Also, if you want to edit the submodules, switch to a branch immediately (otherwise, it's a nuisance to do this later).

This is clunky, but the best way I've found to do it is to clone the module that you wish to update to, then go to each submodule and check the hash. "git log" will show you the commit history, including the hash (the long string of letters and numbers) of the latest commit.  For each submodule that you've edited, manually merge the latest hash into your local version:

check have remote set, and if not add
>git remote -v
>git remote add upstream MAIN_REPO
>git fetch upstream
>git checkout YOUR_LOCAL_BRANCH
>git merge REMOTE_REPO_HASH

For submodules that you haven't edited, you can just checkout the HASH ("git fetch" first to download it).
