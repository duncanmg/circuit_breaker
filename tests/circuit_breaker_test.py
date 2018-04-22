from nose import with_setup
from circuit_breaker import CircuitBreaker
from time import sleep

cb = "";

def setup_cb():
   global cb
   cb = CircuitBreaker()
  
@with_setup(setup_cb)
def test_create():
   global cb
   assert cb
   assert cb.__class__.__name__ == 'CircuitBreaker'

def test_is_closed():
  cb = CircuitBreaker()
  cb.threshold = 1
  assert cb.is_closed() == True
  cb.increment_num_failures()
  assert cb.is_closed() == False

def test_is_closed_two():
  cb = CircuitBreaker()
  cb.threshold = 3
  cb.increment_num_failures()
  cb.increment_num_failures()
  assert cb.is_closed() == True
  cb.increment_num_failures()
  assert cb.is_closed() == False

def test_is_closed_reset():
  cb = CircuitBreaker()
  cb.threshold = 3
  cb.increment_num_failures()
  cb.increment_num_failures()
  assert cb.is_closed() == True
  cb.reset_num_failures()
  cb.increment_num_failures()
  assert cb.is_closed() == True

def test_is_closed_timeout():
  cb = CircuitBreaker()
  cb.threshold = 1
  cb.increment_num_failures()
  cb.max_age = 5
  assert cb.is_closed() == False
  sleep(6) 
  assert cb.is_closed() == True

# **************************************************

def main_call_success():
  print "main_call_success: Call succeeded"

def main_call_failure():
  raise Exception("Exception in main_call_failure")

def test_protect_success():
  cb = CircuitBreaker()

  cb.protect(main_call_success)
  assert True == True
  cb.protect(main_call_success)
  assert True == True
  cb.protect(main_call_success)
  assert True == True

def test_protect_failure():
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

