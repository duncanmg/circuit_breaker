# duncan@Python18:~/circuit-breaker$ PYTHONPATH=`pwd` nosetests -v tests/circuit_breaker_test.py

from nose import with_setup
from circuit_breaker import CircuitBreaker
from time import sleep

cb = "";

def setup_cb():
   global cb
   cb = CircuitBreaker()
  
@with_setup(setup_cb)
def test_create():
   """ Test object creation. """
   global cb
   assert cb
   assert cb.__class__.__name__ == 'CircuitBreaker'

def test_is_closed():
  """ Test that is_closed returns False when the threshold is reached. """
  cb = CircuitBreaker()
  cb.threshold = 1
  assert cb.is_closed() == True
  cb.increment_num_failures()
  assert cb.is_closed() == False

def test_is_closed_two():
  """ Test is_closed with a different threshold. """
  cb = CircuitBreaker()
  cb.threshold = 3
  cb.increment_num_failures()
  cb.increment_num_failures()
  assert cb.is_closed() == True
  cb.increment_num_failures()
  assert cb.is_closed() == False

def test_is_closed_reset():
  """ Test that the reset works. """
  cb = CircuitBreaker()
  cb.threshold = 3
  cb.increment_num_failures()
  cb.increment_num_failures()
  assert cb.is_closed() == True
  cb.reset_num_failures()
  cb.increment_num_failures()
  assert cb.is_closed() == True

def test_is_closed_timeout():
  """ Test that the breaker closes again after "max_age" seconds. """
  cb = CircuitBreaker()
  cb.threshold = 1
  cb.increment_num_failures()
  cb.max_age = 5
  assert cb.is_closed() == False
  sleep(6) 
  assert cb.is_closed() == True

# **************************************************

def main_call_success():
  """ Mock function which simulates success. """
  print "main_call_success: Call succeeded"

def main_call_failure():
  """ Mock function which simulates failure by throwing an exception. """
  raise Exception("Exception in main_call_failure")

def test_protect_success():
  """ Test that a successful call executes without an exception. """

  cb = CircuitBreaker()

  cb.protect(main_call_success)
  assert True == True
  cb.protect(main_call_success)
  assert True == True
  cb.protect(main_call_success)
  assert True == True

def test_protect_failure():
  """ Test that the exception is re-thrown on failue and the 
      breaker opens after 3 failures. """
  cb = CircuitBreaker()

  for x in range(0,3):
    try:
      cb.protect(main_call_failure)
      assert True == False # Should not be reached
    except Exception as e:
      assert e.__class__.__name__ == 'Exception'
      assert  str(e) == "Exception in main_call_failure"

  try: 
    cb.protect(main_call_failure)
    assert True == False # Should not be reached
  except Exception as e:
    assert  str(e) == "Circuit Breaker open"

