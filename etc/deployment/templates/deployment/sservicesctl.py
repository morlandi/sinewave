#!/usr/bin/env python
import argparse
import os

services = {{project.supervised_services}}


def main():

    parser = argparse.ArgumentParser("Supervised services helper script")
    parser.add_argument('action', choices=('start', 'stop', 'restart', 'tail', 'status'))
    parser.add_argument('--verbosity', '-v', type=int, default=1)
    args = parser.parse_args()

    for service in services:
        command = 'sudo supervisorctl %s %s' % (
            args.action,
            service
        )
        if args.verbosity:
            print("\x1b[1;37;40m" + command + "\x1b[0m")
        os.system(command)

if __name__ == "__main__":
    main()
