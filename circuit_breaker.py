import time

""" circuit_breaker """

class CircuitBreaker:

  max_age = 60

  threshold = 3
  num_failures = 0

  last_failure_time = ""

  sink = ""
  source = ""

  def protect(self, external_call):
    """ Executes "external_call" if the circuit breaker is closed.
        Otherwise throws an exception.
        "external_call" must be a function which throws an
        exception on error. """

    self.get_state()
    if self.is_closed():
      try:
        external_call()
        self.reset_num_failures()
        self.set_state()
      except Exception as e:
        self.process_error(e)
        self.set_state()
        raise
    else:
      raise Exception('Circuit Breaker open')
    
  def is_closed(self):
    """ Returns True if the circuit breaker is closed. """

    if self.num_failures < self.threshold:
      return True

    if self.last_failure_time >= (int(time.time()) - self.max_age):
      return False;

    self.reset_num_failures()
 
    return True
      
  def process_error(self, e):
    """ Call when "external_call" throws an exception. """

    self.increment_num_failures()
  
  def reset(self):
    """ Resets the circuit breaker to closed. """

    self.reset_num_failures()

  def reset_num_failures(self):
    """ Sets num_failures to 0 and last_failure_time to "". """
    self.last_failure_time = ""
    self.num_failures = 0

  def increment_num_failures(self):
    """ Increments num_failures and sets last_failure_time. """
    self.num_failures = self.num_failures + 1
    self.last_failure_time = time.time()


# ****************************************************

  def set_storage_source(self,source):
    """ Accepts a function which returns a tuple of
        the number of failures and the time of the
        last failure. """
    self.source = source

  def set_storage_sink(self,sink):
    """ Accepts a function which takes two arguments,
        the number of failures and the time of the
        last failure. """

    self.sink = sink

  def get_state(self):
    """ Gets the current number of failures and
        the time of the last failure. """
    failure_info = self.get_failure_info()
    self.num_failures = failure_info[0]
    self.last_failure_time = failure_info[1]

  def set_state(self):
    """ Sets the current number of failures and
        the time of the last failure. """
    self.set_failure_info(self.num_failures, self.last_failure_time)

  def get_failure_info(self):
    """ Get the failure information by executing "source" if it is
        set or by returning the internal values. """
    if self.source:
      return self.source()
    else:
      return (self.num_failures, self.last_failure_time)

  def set_failure_info(self, num_failures, last_failure_time):
    """ Stores the failure information by executing "sink" it is
        set or by setting the internal values. """

    if self.sink:
      self.sink(num_failures, last_failure_time)
    else:
      self.num_failures = num_failures
      self.last_failure_time = last_failure_time

