# gutils
contains utils for git
requires: cliapp

pip install cliapp gus

## usage:
gus stats --author=<author> --since=<since>
where author can be git name or email, since defaults to '3 month ago'

you can also choose edit ~/.gs as config file:
{
"author" : ["author1","author2"]
}

