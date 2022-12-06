#%%

# Merges one repo into another.

#%%

import errno, os, stat, shutil

def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

#%%

repo_header = "https://github.com/zaireali649/"

source_repo = "zali-learning-python"
destination_repo = "deprecated_repos"

#%% 

out_folder = "out"

if not os.path.exists(out_folder):
    os.mkdir(out_folder)

os.chdir(out_folder)
#%%

os.system("git clone " + repo_header + source_repo)
os.system("git clone " + repo_header + destination_repo)

#%%

os.chdir(source_repo)
os.system("git checkout main")
os.system("git fetch")
os.system("git filter-repo --force --to-subdirectory-filter " + source_repo)
os.chdir("..")

#%%

os.chdir(destination_repo)
os.system("git checkout main")
os.system("git fetch")
os.system("git checkout -b " + source_repo)
os.system("git remote add " + source_repo + " " + "../" + source_repo)
os.system("git fetch "  + source_repo + " --tags")
os.system("git merge --allow-unrelated-histories " + source_repo + "/main")
os.system("git remote remove " + source_repo)
os.system("git push --set-upstream origin "  + source_repo)
os.chdir("../..")

