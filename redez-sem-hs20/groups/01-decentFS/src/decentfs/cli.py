import argparse
import api
import sys
import pathlib
import logging

def _main(argv):
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)
    parser = argparse.ArgumentParser(description='BACnet DecentFS cli', epilog='Version: ' + api.DecentFs.VERSION)
    parser.add_argument('--keyfile', help='A key generated by crypto.py', type=pathlib.Path)
    parser.add_argument('--storage', help='Use an existing DecentFS path', type=pathlib.Path)
    parser.add_argument('--opt', help='Pass custom options', type=ascii)
    parser.add_argument('--verbose', help='Verbose logging', action='store_true')
    parser.add_argument('--debug', help='Debug logging (overwrites verbose)', action='store_true')

    xorarg = parser.add_mutually_exclusive_group()
    xorarg.add_argument('--dump', help='Dump FS', action='store_true')
    xorarg.add_argument('--read', help='File to read from DecentFS', type=pathlib.Path)
    xorarg.add_argument('--stat', help='Get stat of file', type=pathlib.Path)
    xorarg.add_argument('--write', help='File to write to DecentFS', type=pathlib.Path)

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    myDecentFs = None

    if args.keyfile is None:
        logging.error('No keyfile specified')
        parser.print_help()
        sys.exit(1)

    if args.opt is None:
        opt = ''
    else:
        opt = args.opt

    if args.storage is None:
        try:
            myDecentFs = api.DecentFs(args.keyfile, opt=opt)
        except FileExistsError:
            logging.error('File or Directory already exists')
            sys.exit(1)
    else:
        myDecentFs = api.DecentFs(args.keyfile, args.storage, opt=opt)

    if args.write is not None:
        myDecentFs.writeFile(args.write)

    if args.stat is not None:
        stat = myDecentFs.stat(args.stat)
        if stat is None:
            logging.error('File not found.')
            sys.exit(1)
        print('Path: {}\nFlags: {}\nTimestamp: {}\nBytes: {}'.format(stat['path'], stat['flags'], stat['timestamp'], stat['bytes']))
        if args.verbose or args.debug:
            print('Blocks: {}'.format(stat['blocks']))

    if args.dump:
        myDecentFs.dump()

    if args.read is not None:
        try:
            output = open("/dev/stdout", 'wb')
            myDecentFs.readFile(args.read, buf=output)
        except FileExistsError:
            logging.error('File not found.')
            sys.exit(1)

if __name__ == '__main__':
    _main(sys.argv[1:])
