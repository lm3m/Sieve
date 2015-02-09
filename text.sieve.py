#!/usr/bin/env python2.7
"""Text Sieve

Usage: text.sieve.py <filename>

Options:
    -h --help -?    Show this message and exit.
    --version       Show version and exit.
"""
from docopt import docopt
import sys
import os
import logging
import curses
import curses.wrapper
from doc_wrapper import DocWrapper

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='{0}.log'.format(__name__),
                    level=logging.INFO)

doc_name = None

def PrintDocument(doc, stdscr, start = 0):
    try:
        max_x, max_y = stdscr.getmaxyx()
        logging.info("PrintDocument: max_x: {0} max_y: {1}".format(str(max_x), str(max_y)))
        pad = curses.newpad(max_x, max_y)
        row = 0
        x = start
        disp_digits = doc.digits_needed_for_display()
        y = disp_digits + 1
        while row < max_x:
            try:
                if doc.len() < x:
                   break
                line = doc.element(x)
                pad.addnstr(row, 0, "{0:0{1}d}".format(x + 1, disp_digits), disp_digits, curses.A_REVERSE)
                pad.addnstr(row, y, line, max_y - 12)
            except curses.error:
                logging.exception('addch error@ x={0} y={1} row={2} start={3}:'.format(str(x), str(y), str(row), str(start)))
            finally:
                row = row + 1
                x = x + 1

        pad.refresh(0,0, 1,1, max_x-2,max_y-2)
        stdscr.addstr(0, 0, "file: {0} {1:1{2}d}".format(doc.name(), start, disp_digits), curses.A_REVERSE)
        stdscr.refresh()
    except:
        logging.exception("saw:")


def sieve(stdscr):
    logging.info("sieve start")
    max_x, max_y = stdscr.getmaxyx()
    logging.info("max_x: {0} max_y: {1}".format(str(max_x), str(max_y)))
    begin_x = 0; begin_y = 0
    height = max_x - 2; width = max_y
    win = curses.newwin(height, width, begin_x, begin_y)

    doc = DocWrapper(doc_name)
   
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    win.addstr(5,5, "RED ALERT!", curses.color_pair(1))

    PrintDocument(doc, stdscr)
    x = 0
    while True:
        c = stdscr.getch()
        if c == ord('p'):
            PrintDocument(doc, stdscr)
        elif c == ord('q'):
            break  # Exit the while()
        elif c == curses.KEY_HOME:
            x = y = 0
        elif c == curses.KEY_DOWN:
            x = x + 1
            if x > doc.len():
                x = doc.len()
                
            PrintDocument(doc, stdscr, x)
        elif c == curses.KEY_UP:
            x = x - 1
            if x < 0:
                x = 0
            PrintDocument(doc, stdscr, x)
def main():
    logging.info("main start")
    curses.wrapper(sieve)

# main
if __name__ == "__main__":
    arguments = docopt(__doc__, version='text.sieve.py 0.1')
    doc_name = arguments['<filename>']
    main()
