from circuit_breaker import *

def main_call_success():
  print "main_call_success: Call succeeded"

def main_call_failure():
  print "main_call_failure: Call failure"
  raise Exception("Exception in main_call_failure")

cb = CircuitBreaker()

cb.protect(main_call_success)

try:
  cb.protect(main_call_failure)
except Exception as e:
  print e


print cb.num_failures
