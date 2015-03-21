#!/usr/bin/env python3

# For more information on the uniprot REST interface go here
# http://www.uniprot.org/help/programmatic_access

import argparse
import httplib2
import sys

__version__ = '1.0'
__prog__ = 'dolup'

def positive_int(i):
    i = int(i)
    if i < 0:
         raise argparse.ArgumentTypeError("%s is an invalid positive number" % i)
    return i

def parser(argv=None):
    parser = argparse.ArgumentParser(
        prog=__prog__,
        usage="%s [options] <clade taxon id>" % __prog__,
        description="List or download UniProt proteomes within a taxonomic group"
    )
    parser.add_argument(
        '--version',
        help='Display version',
        action='version',
        version='%(prog)s {}'.format(__version__)
    )
    parser.add_argument(
        'top_taxid',
        type=positive_int,
        help='The taxon id of the ancestral node'
    )
    parser.add_argument(
        '-q', '--retrieve-sequence',
        help="download all proteome fasta files",
        action="store_true",
        default=False
    )
    parser.add_argument(
        '-r', "--reference",
        help="retrieve only reference proteomes",
        action="store_true",
        default=False
    )
    parser.add_argument(
        '-a', '--retrieve-annotations',
        help='download columns of data (write "--" after last column name)',
        nargs='+'
    )
    parser.add_argument(
        '-i', '--include-isoforms',
        help='include protein isoforms',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--cache',
        help="Cache directory name",
    )
    parser.add_argument(
        '--print_http',
        help="Print all HTTP request",
        action="store_true",
        default=False
    )
    args = parser.parse_args(argv)
    return(args)

def prettyprint_http(response):
    d = dict(response.items())
    for k,v in d.items():
        print("\t%s: %s" % (k,v), file=sys.stderr)

def makeurl(db, arg):
    argstr = '&'.join('%s=%s' % (k,v) for k,v in arg.items())
    url = "http://www.uniprot.org/%s/?%s" % (db, argstr)
    return(url)


if __name__ == '__main__':

    args = parser()

    if args.print_http:
        httplib2.debuglevel = 1

    proteome = 'reference:yes' if args.reference else 'complete:yes'
    include = 'yes' if args.include_isoforms else 'no'

    h = httplib2.Http(args.cache)

    par = {'query': 'ancestor:%s+%s' % (args.top_taxid, proteome),
           'format': 'list'}
    response, content = h.request(makeurl('taxonomy', par))

    if args.print_http:
        prettyprint_http(response)

    taxids = content.decode().strip().split("\n")

    for taxid in taxids:
        if args.retrieve_sequence or args.retrieve_annotations:
            if args.retrieve_annotations:
                filename = '%s.tab' % taxid
                par = {'query':'organism:%s' % taxid,
                       'format':'tab',
                       'include':include,
                       'columns':','.join(args.retrieve_annotations)}
            elif args.retrieve_sequence:
                filename = '%s.faa' % taxid
                par = {'query':'organism:%s' % taxid,
                       'format':'fasta',
                       'include':include}
            print("Retrieving %s" % filename, file=sys.stderr)
            url = makeurl('uniprot', par)
            response, content = h.request(url)
            if args.print_http:
                print("URL:%s" % url)
                prettyprint_http(response)
            with open(filename, 'w') as f:
                print(content.decode(), file=f)
        else:
            print(taxid)
