#!/usr/bin/python3


from saturn.data_view import EventView

__all__ = ['event_plot', ]


def event_plot():
    from dev_global.env import VIEWER_HEADER
    event = EventView(VIEWER_HEADER)
    event.get_basic_index('SH000300')
