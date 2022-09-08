# Tim Barnes
# v0.0.1
# 2022-09-08
#
# A tool for network folks to quickly ping Google's public DNS server (8.8.8.8)
# to verify network functionality

from pythonping import ping

TARGET = '8.8.8.8'
VERBOSITY = True


def execute_ping():
    ping(TARGET, verbose=VERBOSITY)
    return


def main():
    execute_ping()
    return


main()