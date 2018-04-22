import time

class CircuitBreaker:

  max_age = 60
  threshold = 3
  num_failures = 0

  last_failure_time = ""

  sink = ""
  source = ""

  def protect(self, external_call):
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

    if self.num_failures < self.threshold:
      return True

    if self.last_failure_time >= (int(time.time()) - self.max_age):
      return False;

    self.reset_num_failures()
 
    return True
      
  def process_error(self, e):
    self.increment_num_failures()
  
  def reset(self):
    self.reset_num_failures()

  def reset_num_failures(self):
    self.last_failure_time = ""
    self.num_failures = 0

  def increment_num_failures(self):
    self.num_failures = self.num_failures + 1
    self.last_failure_time = time.time()


# ****************************************************

  def set_storage_source(self,source):
    self.source = source

  def set_storage_sink(self,sink):
    self.sink = sink

  def get_state(self):
    failure_info = self.get_failure_info()
    self.num_failures = failure_info[0]
    self.last_failure_time = failure_info[1]

  def set_state(self):
    self.set_failure_info(self.num_failures, self.last_failure_time)

  def get_failure_info(self):
    if self.source:
      return self.source()
    else:
      return (self.num_failures, self.last_failure_time)

  def set_failure_info(self, num_failures, last_failure_time):
    if self.sink:
      self.sink(num_failures, last_failure_time)
    else:
      self.num_failures = num_failures
      self.last_failure_time = last_failure_time

