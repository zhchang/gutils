# Make sure you replace the API and/or APP key below
# with the ones for your account

from cliapp import CliApp
import sys
import json
from os.path import expanduser


class GUtils(CliApp):

    def get_stats_by_author(self, author, since):
        cmd = "git log --graph --decorate --pretty=oneline --abbrev-commit  --numstat --author='{}' --since='{}'".format(
            author, since)
        o, r = self.shell_run(cmd, silent=True)
        if r != 0:
            return 'something wrong with the git command execution: {}'.format(o)
        additions = 0
        deletions = 0
        commits = 0
        if len(o) > 0:
            for line in o:
                line = line.decode()
                if line.startswith('*'):
                    commits += 1
                    continue
                if line.find('/vendor') > 0:
                    continue
                items = line.split('\t')
                if len(items) > 2:
                    try:
                        additions += int(items[0])
                        deletions += int(items[1])
                    except:
                        continue
        print ("{}\t{}\t{}\t{}".format(author, commits, additions, deletions))

    def get_authors_from_config(self):
        with open('{}/.gs'.format(expanduser('~')), 'r') as f:
            cfg = json.load(f)
            return cfg['authors']

    def do_stats(self, **kwargs):
        """gus stats author=<author> since=<since>
        since is default to '3 month ago'
        When author is not specified, gus will try to read from ~/.gs (sample content: {"author":["author1","author2"]}
        """
        author = kwargs.get('author', None)
        since = kwargs.get('since', '3 month ago')
        print ("{}\t{}\t{}\t{}".format('author', 'commits', 'additions', 'deletions'))
        try:
            if author != None:
                self.get_stats_by_author(author, since)
            else:
                authors = self.get_authors_from_config()
                if authors != None:
                    for author in authors:
                        self.get_stats_by_author(author, since)
        except Exception as e:
            print ('something is wrong: {}'.format(e))

    def do_who(self, **kwargs):
        """gus who path=<path> max=<max>
        max is default to 5
        path is default to . (current working directory)
        """
        path = kwargs.get('path', '.')
        max_str = kwargs.get('max', '5')
        try:
            max = int(max_str)
        except:
            print ('invalid input for max, default to 5 now.')
            max = 5
        cmd = 'git shortlog -nse -- {}'.format(path)
        o, r = self.shell_run(cmd, silent=True)
        if r != 0:
            print ('something went wrong with the git shortlog command execution: {}'.format(o))
            return
        if len(o) > 0:
            print ('commits\tauthor')
            for line in o[:max]:
                print (line.decode())


if __name__ == '__main__':
    gus = GUtils()
    gus.run(sys.argv[1:])
