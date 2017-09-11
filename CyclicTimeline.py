#!/usr/bin/env python3

from datetime import datetime

from pysvgi import Svg


class CyclicTimeline(Svg):
    
    CYCLE_HOUR = 1
    CYCLE_DAY = 2
    CYCLE_WEEK = 3
    CYCLE_YEAR = 4
    
    def __init__(self, startDate, endDate, cycleLength=CYCLE_HOUR):

        self.startDate = startDate
        self.endDate = endDate
        self.cycleLength = cycleLength

        self.width = 100
        self.height = 100
        
        super().__init__(width=self.width, height=self.height)
        
        




if __name__ == '__main__':
    timeline = CyclicTimeline(
        datetime(2017, 9, 10, 9),
        datetime(2017, 9, 10, 17),
        CyclicTimeline.CYCLE_HOUR)
    with open('timeline.svg', 'w') as outFile:
        outFile.write(timeline.document())
