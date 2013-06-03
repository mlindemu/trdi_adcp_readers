#!/usr/bin/python


# Taken from http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def PD15_file_to_PD0(path, header_lines=0):
    """
    Parses a PD15 formatted file and returns a list of PD0 Strings
    """
    retVal = []
    with open(path, 'rb') as f:
        if (header_lines > 0):
            for i in xrange(0, header_lines):
                f.readline()

        for line in f:
            retVal.append(PD15_string_to_PD0(line))

    return retVal


def PD15_string_to_PD0(line):
    """
    Parses a single PD15 line and returns a PD0 byte array
    """
    line_bytes = bytearray(line)
    line_chunks = chunks(line_bytes, 4)

    pd0_out = bytearray(len(line_bytes))
    pd0_index = 0
    for c in line_chunks:
        if (len(c) >= 2):
            temp_int = (c[0] & 0x3f) << 2
            temp_int |= (c[1] & 0x30) >> 4
            pd0_out[pd0_index] = temp_int
            pd0_index += 1

            if (len(c) >= 3):
                temp_int = (c[1] & 0x0f) << 4
                temp_int |= (c[2] & 0x3c) >> 2
                pd0_out[pd0_index] = temp_int
                pd0_index += 1

                if (len(c) == 4):
                    temp_int = (c[2] & 0x03) << 6
                    temp_int |= (c[3] & 0x3f)
                    pd0_out[pd0_index] = temp_int
                    pd0_index += 1

    return pd0_out[:pd0_index+1]

import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--header_lines", type=int,
                        help="Number of header lines to skip in PD15 file")
    parser.add_argument("input_path",
                        help="PD15 file path to be converted to PD0")
    parser.add_argument("output_path", help="PD0 output file")
    args = parser.parse_args()

    if args.header_lines is None:
        args.header_lines = 0

    PD0Bytes = PD15_file_to_PD0(args.input_path,
                                header_lines=args.header_lines)
    with open(args.output_path, 'wb') as f:
        for b in PD0Bytes:
            f.write(b)

if __name__ == '__main__':
    sys.exit(main())
