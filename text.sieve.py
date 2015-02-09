#!/usr/bin/python
# -*- coding: utf-8 -*-
# """
# Filtering text file viewer
# """
import sys
import os
import logging
import curses
import curses.wrapper

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='{0}.log'.format(__name__),
                    level=logging.INFO)

doc_name = 'test.txt'
doc = []

def PrintDocument(stdscr, start = 0):
    try:
        max_x, max_y = stdscr.getmaxyx()
        #max_x = max_x - 1
        #max_y = max_y - 10
        logging.info("PrintDocument: max_x: {0} max_y: {1}".format(str(max_x), str(max_y)))
        pad = curses.newpad(max_x, max_y)
        #  These loops fill the pad with letters; this is
        # explained in the next section
        row = 0
        x = start
        y = 11
        while row < max_x:
            try:
                if len(doc) < x:
                   break
                line = doc[x]
                pad.addnstr(row, 0, "{0:0{1}d}".format(x + 1, 10), 10, curses.A_REVERSE)
                pad.addnstr(row, y, line, max_y - 12)
            except curses.error:
                logging.exception('addch error@ x={0} y={1} row={2} start={3}:'.format(str(x), str(y), str(row), str(start)))
            finally:
                row = row + 1
                x = x + 1
        #  Displays a section of the pad in the middle of the screen
        pad.refresh(0,0, 1,1, max_x-2,max_y-2)
        stdscr.addstr(0, 0, "file: {0} {1:1{2}d}".format(doc_name, start, 10), curses.A_REVERSE)
        stdscr.refresh()
    except:
        logging.exception("saw:")


def sieve(stdscr):
    logging.info("sieve start")
    max_x, max_y = stdscr.getmaxyx()
    logging.info("max_x: {0} max_y: {1}".format(str(max_x), str(max_y)))
    begin_x = 1; begin_y = 1
    height = max_x - 2; width = max_y - 2
    win = curses.newwin(height, width, begin_y, begin_x)

    f = open(doc_name, 'r')
    for line in f:
        doc.append(line)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    win.addstr(5,5, "RED ALERT!", curses.color_pair(1))
#    stdscr.refresh()
#    curses.echo()            # Enable echoing of characters

    # Get a 15-character string, with the cursor on the top line
#    s = stdscr.getstr(0,0, 15)

    PrintDocument(stdscr)
    x = 0
    while True:
        c = stdscr.getch()
        if c == ord('p'):
            PrintDocument(stdscr)
        elif c == ord('q'):
            break  # Exit the while()
        elif c == curses.KEY_HOME:
            x = y = 0
        elif c == curses.KEY_DOWN:
            x = x + 1
            PrintDocument(stdscr, x)
        elif c == curses.KEY_UP:
            x = x - 1
            if x < 0:
                x = 0
            PrintDocument(stdscr, x)
def main():
    logging.info("main start")
    curses.wrapper(sieve)

# main
if __name__ == "__main__":
    main()
