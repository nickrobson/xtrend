import subprocess
import re

def get_git_tags():
    tags = []
    with subprocess.Popen(['git', 'tag', '-l'], stdout=subprocess.PIPE) as proc:
        tags = proc.stdout.read().decode('utf-8').splitlines()
    return tags

# Get's the tag description using git show
def get_description(tag):
    with subprocess.Popen(["git", "show", tag], stdout=subprocess.PIPE) as proc:
        tagShow = proc.stdout.read().decode("utf-8")
    #some funky manipluation to get just commit msg:
    tagShow = re.sub("tag " + tag
        + "\s*Tagger:.*\s*Date:[^\n]*", "", tagShow)
    tagstring = tagShow.split('commit')
    tagShow = tagstring[0]
    return tagShow