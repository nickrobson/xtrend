import subprocess

def get_git_tags():
    tags = []
    with subprocess.Popen(['git', 'tag', '-l'], stdout=subprocess.PIPE) as proc:
        tags = proc.stdout.read().decode('utf-8').splitlines()
    # expect tags to be in [0-9]+_[0-9]+_[0-9]+ format
    tags = sorted(map(lambda tag: list(map(int, tag.split('_'))), tags))
    tags = list(map(lambda tag: '_'.join(map(str, tag)), tags))
    return tags