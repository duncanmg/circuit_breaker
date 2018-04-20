import time

class CircuitBreaker:

  max_age = 60
  threshold = 3

  failures = list()

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
    while len(self.failures) and self.failures[0][0] < int(time.time()) - self.max_age:
      self.failures.pop(0)
    if len(self.failures) < self.threshold:
      return True
    else:
      return False
      
  def process_error(self, e):
    self.failures.append((time.time(), e))
    pass
  
  def reset(self):
    self.failures = list()

  def set_storage_source(self,source):
    self.source = source

  def set_storage_sink(self,sink):
    self.sink = sink

