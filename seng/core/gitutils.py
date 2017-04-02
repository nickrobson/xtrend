import subprocess

from datetime import datetime

def _tag_to_key(tag):
    return list(map(int, tag.split('_')))

def _key_to_tag(key):
    return '_'.join(map(str, key))

def get_tags():
    tags = []
    with subprocess.Popen(['git', 'tag', '-l'], stdout=subprocess.PIPE) as proc:
        tags = proc.stdout.read().decode('utf-8').splitlines()
    # expect tags to be in [0-9]+_[0-9]+_[0-9]+ format
    tags = sorted(map(_tag_to_key, tags))
    tags = list(map(_key_to_tag, tags))
    return tags

# Get's the tag description using git show
def get_tag_meta(tag):
    with subprocess.Popen(["git", "show", tag], stdout=subprocess.PIPE) as proc:
        lines = proc.stdout.read().decode("utf-8").splitlines()
    #some funky manipluation to get just commit msg:
    commit, date = None, None
    start, end = None, None
    for i, line in enumerate(lines):
        # get tag message start line
        if line == '' and start is None:
            start = i + 1 # ignore next line (blank)
        # get commit id and tag message end line
        if line.startswith('commit '):
            end = i - 1 # ignore previous line (blank)
            commit = line[len('commit '):]
        # get commit date
        if commit is not None and line.startswith('Date:   '):
            date = datetime.strptime(line[len('Date:   '):], '%a %b %d %H:%M:%S %Y %z')
            break
    meta = {
        'tag': tag,
        'commit': commit,
        'date': date,
        'description': '\n'.join(lines[start : end])
    }
    return meta
