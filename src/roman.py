#!/bin/env python

# A class for outputting the time as roman numerals.

from datetime import datetime

class RomanNumber(object):
    """A small class for writing Roman Numerals"""

    nums = {1: { 1: "I",
                 5: "V"},
            2: { 1: "X",
                 5: "L"},
            3: { 1: "C",
                 5: "D"},
            4: { 1: "M"}}

    def __init__(self, num=0):
        """Initialize Roman Number
        
        @int num: Integer number to convert.
        """
        self.num = int(num)

    def to_string(self):
        if self.num >= 10000:
            raise ValueError("Number is too large. Mind is blown.")

        if self.num == 0:
            return "0"

        s = str(self.num)
        final = ""
        while (s):
            l = s[0]
            i = int(l)
            chrs = self.nums[len(s)]
            out = ""

            if i == 4:
                out = chrs[1] + chrs[5]
                i = 0
            elif i == 9:
                out = chrs[1] + self.nums[len(s) + 1][1]
                i = 0
            elif i >= 5:
                out = chrs[5]
                i -= 5

            while(i):
                out += chrs[1]
                i -= 1

            s = s[1:]

            # Append to final string.
            final += out

        return final

    def __str__(self):
        return self.to_string()

class RomanTime(object):
    """A small class for printing the current hour and minute as roman numerals."""

    def __init__(self, dt=None):
        """Initialize Roman Time.
        
        @datetime dt: Datetime wanted.  If not supplied, datetime.now() is used.
        """

        if not dt:
            dt = datetime.now()
        self.dt = dt

    def to_string(self):
        """Present Roman Time as string."""
        # We don't have a 0-hour. Only a 24.
        hour = self.dt.hour
        if hour == 0:
            hour = 24
        return "%s:%s" % (RomanNumber(hour), RomanNumber(self.dt.minute))

    def __str__(self):
        return self.to_string()

if __name__ == "__main__":
    import sys
    print "Time is now:", RomanTime()

    if len(sys.argv) > 1:
        print "Supplied numbers are:"
        for i in sys.argv[1:]:
            print "    %s => %s" % (i, RomanNumber(int(i)))
