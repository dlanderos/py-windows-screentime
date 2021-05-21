"""
    py-windows-screentime: Python program that tracks window usage.
    Copyright (C) 2021 dxboats

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from asyncio import run, get_running_loop, create_task, wait, FIRST_COMPLETED
from asyncio.exceptions import CancelledError
from concurrent.futures.thread import ThreadPoolExecutor
from ctypes import pointer
from ctypes.wintypes import MSG

from helpers.printing import pretty_print_result
from helpers.rectangle import rectangle_area
from helpers.window import WindowResult, update_capture_state, finalize_capture_state
from windows.type import WINEVENTPROC
from windows.definition import EVENT_SYSTEM_FOREGROUND, EVENT_SYSTEM_MINIMIZESTART, EVENT_SYSTEM_MINIMIZEEND, \
    WINEVENT_OUTOFCONTEXT, WINEVENT_SKIPOWNPROCESS, WM_QUIT
from windows.function import get_message_w, post_thread_message_w, translate_message, dispatch_message_w, \
    set_win_event_hook, unhook_win_event, get_current_thread_id


def print_results(results: frozenset[WindowResult]):
    total_time_all = 0
    total_area_all = 0
    for result1 in results:
        for state in result1.states:
            total_time_all += state.duration
            total_area_all += rectangle_area(state.rectangle)

    for result in results:
        aggregate_time = 0
        aggregate_area = 0
        titles = set()
        for state in result.states:
            titles.add(state.title)
            aggregate_time += state.duration
            aggregate_area += rectangle_area(state.rectangle)
        share_time = aggregate_time / total_time_all
        share_area = aggregate_area / total_area_all
        average_area = int(aggregate_area / len(result.states))

        pretty_print_result(result.process, titles, aggregate_time, share_time, average_area, share_area)


async def routine_message_queue(event_loop, executor):
    captures = {}
    states = {}

    # Use an array so that a value can be appended to it from another thread.
    # Probably a more proper solution to this, but it works well enough.
    thread_ids = []

    # Isolate the message queue receiving to its own anonymous function.
    def blocking_receive_message() -> frozenset[WindowResult]:

        update_capture_state(captures, states)

        # Get this thread's ID
        current_thread_id = get_current_thread_id()
        thread_ids.append(current_thread_id)

        # Attempt to create the event hook.
        # It must be created within the same thread as the message queue receiver for the callback to be fired.
        event_hook_handle = set_win_event_hook(
            callback=win_event_hook_callback,
            event_filter_min=EVENT_SYSTEM_FOREGROUND,
            event_filter_max=EVENT_SYSTEM_MINIMIZEEND,
            flags=WINEVENT_OUTOFCONTEXT | WINEVENT_SKIPOWNPROCESS
        )

        # Determine if the hook was created successfully.
        if event_hook_handle == 0:
            print("Could not create the event hook.")
            return frozenset()

        # Read all readily available messages from the queue.
        # Loops forever until it receives a WM_QUIT message.
        message_pointer = pointer(MSG())
        while get_message_w(message_pointer):
            translate_message(message_pointer)
            dispatch_message_w(message_pointer)

        # Unhook the event handler.
        unhook_win_event(event_hook_handle)

        finalized_results = finalize_capture_state(captures, states)
        print_results(finalized_results)

        return finalized_results

    # Isolate the event hook callback to its own anonymous function.
    # It shouldn't be called anywhere except here.
    # The annotation is important so Python knows its a callback function using Windows calling procedures.
    @WINEVENTPROC
    def win_event_hook_callback(hook, event, hwnd, id_object, id_child, dw_event_thread, dw_event_time):
        if event == EVENT_SYSTEM_FOREGROUND or event == EVENT_SYSTEM_MINIMIZESTART or event == EVENT_SYSTEM_MINIMIZEEND:
            update_capture_state(captures, states)

    try:
        # Run the message queue receiver in a separate thread so it doesn't block the main one.
        await event_loop.run_in_executor(executor, blocking_receive_message)

    # Wait for a cancellation error so we can tell Windows we don't need to receive anymore messages
    # If we don't do this, the application will be locked... forever.
    except CancelledError:
        # Tell the message queue in the other thread that it can stop now (if the thread was even able to start).
        if len(thread_ids) == 1:
            post_thread_message_w(thread_ids[0], WM_QUIT)


async def routine_user_input(event_loop, executor):
    # Wait for the user to press (any key) to exit.
    await event_loop.run_in_executor(executor, input, "Press RETURN to exit and read results.\n")


async def routine_main():
    # Get the running loop.
    event_loop = get_running_loop()

    # Create a thread pool executor so tasks don't block the entire application.
    executor = ThreadPoolExecutor(max_workers=2)

    task_input = create_task(routine_user_input(event_loop, executor))
    task_message_queue = create_task(routine_message_queue(event_loop, executor))

    # Wait for one of the tasks to complete.
    _, pending_tasks = await wait(
        [
            task_input,
            task_message_queue
        ],
        return_when=FIRST_COMPLETED
    )

    # Cancel all pending (incomplete) tasks.
    for task in pending_tasks:
        task.cancel()


if __name__ == '__main__':
    run(routine_main())
