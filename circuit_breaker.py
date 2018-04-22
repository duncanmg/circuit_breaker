import time

class CircuitBreaker:

  max_age = 60
  threshold = 3
  num_failures = 0

  last_failure_time = ""

  sink = ""
  source = ""

  def protect(self, external_call):
    if self.is_closed():
      try:
        external_call()
        self.reset_num_failures()
      except Exception as e:
        self.process_error(e)
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
  
  def get_failures(self):
    if self.source:
      return self.source()
    else:
      return self.failures

  def set_failures(self, failures):
    if self.sink:
      self.sink(failures)
    else:
      self.failures = failures

  def reset(self):
    self.failures = list()

  def set_storage_source(self,source):
    self.source = source

  def set_storage_sink(self,sink):
    self.sink = sink

  def reset_num_failures(self):
    self.last_failure_time = ""
    self.num_failures = 0

  def increment_num_failures(self):
    self.num_failures = self.num_failures + 1
    self.last_failure_time = time.time()


