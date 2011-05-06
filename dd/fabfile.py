# http://lethain.com/entry/2008/nov/04/deploying-django-with-fabric/
# Fabric ---
#	run 		runs command on another machine
#	sudo		runs command on another machine as root
#	put			sends a file to another machine
# 	invoke		runs another function with the current function's config context
#	require		creates dependencies between various functions,
#				prevents function from being run without its prerequisites

# Runs with commands like 
#	fab production reboot
#	fab staging reboot
#	fab production pull reboot
# 	fab production reset:repo=my_app_repo,hash=13klafeomaeio23 reboot

# Branches: 
#	master		current working copy
#	release		
# 	proto		

def production():
	config.fab_hosts = ['doloresdeals.org']
	config.repos = (('dolores-deals','origin','release'),)
	# Repo:		repo, parent, branch

def staging():
	config.fab_hosts = ['staging.doloresdeals.org']
	config.repos = (('dolores-deals','origin','release'),)
	
def proto():
	config.fab_hosts = ['proto.doloresdeals.org']
	config.repos = (('dolores-deals','origin','proto'),)

def git_pull():
	"Updates the repository."
	run("cd ~/git/$(repo)/; git pull $(parent) $(branch)")

def git_reset():
	"Resets the repository to specified version."
	run("cd ~/git/$(repo)/; git reset --hard $(hash)")

def reboot():
    "Reboot Apache2 server."
	run('../apache2/bin/restart')		# Rel to this file (fabfile.py)
	
# Pulls the repo from the remote store
def pull():
    require('fab_hosts', provided_by=[production])		# Other configs as well?
    for repo, parent, branch in config.repos:
        config.repo = repo
        config.parent = parent
        config.branch = branch
        invoke(git_pull)

def reset(repo, hash):
    """
    Reset all git repositories to specified hash.
    Usage:
        fab reset:repo=my_repo,hash=etcetc123
    """
    require("fab_hosts", provided_by=[staging, production])
    config.hash = hash
    config.repo = repo
    invoke(git_reset)
