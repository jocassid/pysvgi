#!/usr/bin/env python3

from datetime import datetime
from unittest import TestCase

from CyclicTimeline import DatetimeUtil


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
