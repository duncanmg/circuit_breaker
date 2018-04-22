import time

class CircuitBreaker:

  max_age = 60
  threshold = 3

  failures = list()

  sink = ""
  source = ""

  def protect(self, external_call):
    if self.is_closed():
      try:
        external_call()
      except Exception as e:
        self.process_error(e)
        raise
    else:
      raise Exception('Circuit Breaker open')
    
  def is_closed(self):
    failures = self.get_failures()
    count = 0

    while len(failures) and failures[0][0] < int(time.time()) - self.max_age:
      failures.pop(0)
      count = count + 1

    if count > 0:
      self.set_failures(failures)

    if len(failures) < self.threshold:
      return True
    else:
      return False
      
  def process_error(self, e):
    failures = self.get_failures()
    failures.append((time.time(), e))
    self.set_failures(failures)
  
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

