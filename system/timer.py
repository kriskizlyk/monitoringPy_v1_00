from threading import Timer, Thread, Event

class TimerEvent():

    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.timed_out = False
        self.__error_flag = False
        self.retry = 1
        self.status = True

    def handle_function(self):
        # Run the function once the timer thread is done.

        # Timer did not catch an error, reset timeout count.
        if (self.__error_flag == False):
            self.retry = 1
        else:
            self.__error_flag = False

        # Timer cycle was complete, restart timer.
        if (self.timed_out == False):
            self.hFunction()
            self.start()
        else:
            self.cancel()

    def start(self):
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def error(self):
        self.retry = self.retry - 1
        self.__error_flag = True
        if (self.retry < 1):
            self.timed_out = True
            self.status = False

    def cancel(self):
        # Destroys the entire timer thread.
        self.status = False
        self.thread.cancel()

    def get_status(self):
        return self.status
