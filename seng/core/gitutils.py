import subprocess

def _tag_to_key(tag):
    return list(map(int, tag.split('_')))

def _key_to_tag(key):
    return '_'.join(map(str, tag))

def get_git_tags():
    tags = []
    with subprocess.Popen(['git', 'tag', '-l'], stdout=subprocess.PIPE) as proc:
        tags = proc.stdout.read().decode('utf-8').splitlines()
    # expect tags to be in [0-9]+_[0-9]+_[0-9]+ format
    tags = sorted(map(_tag_to_key, tags))
    tags = list(map(_key_to_tag, tags))
    return tags