# duncan@Python18:~/circuit-breaker$ PYTHONPATH=`pwd` nosetests -v tests/circuit_breaker_test.py
# PYTHONPATH=`pwd` nosetests -v --no-byte-compile tests/*

from nose import with_setup
from circuit_breaker import CircuitBreaker


num_failures = 0
last_failure_time = ""

def source():
  global num_failures, last_failure_time
  return (num_failures, last_failure_time)


def sink(nf, lft):
  global num_failures, last_failure_time
  num_failures = nf
  last_failure_time = lft

def main_call_success():
  print "main_call_success: Call succeeded"

def main_call_failure():
  raise Exception("Exception in main_call_failure")

def test():
  cb = CircuitBreaker()
  cb.set_storage_source(source)
  cb.set_storage_sink(sink)
  assert True == True
  try:
    cb.protect(main_call_failure)
  except Exception as e:
    pass

def test_globals():
  global num_failures, last_failure_time
  assert num_failures == 1
  assert last_failure_time > 0

def test_different_object():
  cb2 = CircuitBreaker()
  cb2.set_storage_source(source)
  cb2.set_storage_sink(sink)
  assert True == True
  try:
    cb2.protect(main_call_failure)
  except Exception as e:
    pass

def test_globals_persist():
  global num_failures, last_failure_time
  print num_failures
  assert num_failures == 2
  assert last_failure_time > 0

