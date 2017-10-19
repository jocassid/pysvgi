#!/usr/bin/env python3

from datetime import datetime, timedelta
from unittest import TestCase

from CyclicTimeline import CyclicTimeline, DatetimeUtil, Event, \
    EventSeries, EventSpan, Row


class DatetimeUtilTest(TestCase):

    def test_round_down(self):
        d1 = datetime(2017, 9, 17, 2, 13, 9, 31434)
        self.assertEqual(
            datetime(2017, 9, 17, 2),
            DatetimeUtil.round_down(d1, 'hour'))

    def test_round_up(self):
        d1 = datetime(2017, 9, 17, 2, 13, 9, 31434)
        self.assertEqual(
            datetime(2017, 9, 17, 3),
            DatetimeUtil.round_up(d1, 'hour'))


class EventTest(TestCase):
    def test_onRow(self):
        event = Event(datetime(2017, 10, 2, 23, 59, 59))
        
        row = Row(
            datetime(2017, 10, 2, 22),
            datetime(2017, 10, 2, 23),
            0, 100, 50)
        self.assertFalse(event.onRow(row))
        
        row = Row(
            datetime(2017, 10, 2, 23),
            datetime(2017, 10, 3),
            0, 100, 50)
        self.assertTrue(event.onRow(row))
        
        row = Row(
            datetime(2017, 10, 3),
            datetime(2017, 10, 3, 1),
            0, 100, 50)
        self.assertFalse(event.onRow(row))


class RowTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.startTime = datetime(2017, 10, 17, 23, 0)
        cls.row1 = Row(
            cls.startTime,
            datetime(2017, 10, 17, 23, 5),
            0,      # minX
            100,    # maxX,
            25)

    def test_recalculate(self):
        # recalculate is called as part of the __init__ method
        self.assertEqual(100, self.row1.width)
        self.assertEqual(
            self.startTime.timestamp(), 
            self.row1.startTimestamp)
        self.assertEqual(300, self.row1.timeSpan)
    
    def test_datetimeToX(self):
        
        row = Row(
            datetime(2017, 10, 17, 23, 0),
            datetime(2017, 10, 17, 23, 5),
            0,      # minX
            100,    # maxX,
            25)
        
        self.assertEqual
            
        
        
class EventSpanTest(TestCase):
    def test_inRange(self):
        event = EventSpan(
            datetime(2017, 10, 3, 19, 40),
            datetime(2017, 10, 3, 19, 45))

        row = Row(
            datetime(2017, 10, 3, 19, 10),
            datetime(2017, 10, 3, 19, 30),
            0, 100, 50)
        self.assertFalse(event.onRow(row))
        
        row = Row(
            datetime(2017, 10, 3, 19, 30),
            datetime(2017, 10, 3, 19, 40),
            0, 100, 50)
        self.assertFalse(event.onRow(row))
        
        row = Row(
            datetime(2017, 10, 3, 19, 30),
            datetime(2017, 10, 3, 19, 42),
            0, 100, 50)
        self.assertTrue(event.onRow(row))
        
    def test_split(self):
        startTime = datetime(2017, 10, 7, 17, 50)
        endTime = datetime(2017, 10, 7, 18, 10)
        event = EventSpan(startTime, endTime)
        
        splitTime = datetime(2017, 10, 7, 18, 0)
        resolutionTimedelta = timedelta(minutes=1)
        event, remainder = event.split(splitTime, resolutionTimedelta)
        
        self.assertEqual(
            EventSpan(startTime, splitTime - resolutionTimedelta),
            event)
        
        self.assertEqual(
            EventSpan(splitTime, endTime),
            remainder)
                
        
class EventSeriesTest(TestCase):
    def test_getEventsOnRow(self):
        
        startTime = datetime(2017, 10, 7, 17, 0)
        endTime = datetime(2017, 10, 7, 18, 0)
        
        event1 = Event(datetime(2017, 10, 7, 16, 45))
        event2 = Event(startTime)
        event3 = Event(datetime(2017, 10, 7, 17, 30))
        event4 = Event(endTime)
        
        spanStart = datetime(2017, 10, 7, 17, 50)
        spanEnd = datetime(2017, 10, 7, 18, 10)
        event5 = EventSpan(spanStart, spanEnd)
        
        series = EventSeries(
            'test2', 
            'red',
            [event1, event2, event3, event4, event5])
        
        row = Row(
            startTime,
            endTime,
            0,
            100,
            50)
        
        resolutionTimedelta = timedelta(minutes=1)
        
        events = series.getEventsOnRow(
            row, 
            resolutionTimedelta)
        
        self.assertFalse(event1 in events)
        self.assertTrue(event2 in events)
        self.assertTrue(event3 in events)
        self.assertFalse(event4 in events)
        
        event5a = EventSpan(spanStart, endTime - resolutionTimedelta)
        event5b = EventSpan(endTime, spanEnd)
        
        self.assertTrue(event5a in events)
        self.assertTrue(event5b in series)
            
        

class CyclicTimelineTest(TestCase):
   
    def test_getRowStartTime(self):
        timelineStart = datetime(2017, 10, 2, 22, 0)
        cyclicTimeline = CyclicTimeline(
            timelineStart,
            datetime(2017, 10, 3, 10, 0),
            'hour')
        
        self.assertEqual(timelineStart, cyclicTimeline.getRowStartTime(0))
        self.assertTrue(0 in cyclicTimeline.rowStartTimes)
        self.assertEqual(timelineStart, cyclicTimeline.rowStartTimes[0])
        
        oneHourLater = datetime(2017, 10, 2, 23, 0)
        self.assertEqual(
            oneHourLater,
            cyclicTimeline.getRowStartTime(1))
        self.assertTrue(1 in cyclicTimeline.rowStartTimes)
        self.assertEqual(oneHourLater, cyclicTimeline.rowStartTimes[1])
        
        twoHoursLater = datetime(2017, 10, 3, 0, 0)
        self.assertEqual(
            twoHoursLater,
            cyclicTimeline.getRowStartTime(2))
        self.assertTrue(2 in cyclicTimeline.rowStartTimes)
        self.assertEqual(twoHoursLater, cyclicTimeline.rowStartTimes[2])
        self.assertFalse(0 in cyclicTimeline.rowStartTimes)
            
            
            
