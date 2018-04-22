from circuit_breaker import *
from random import randrange
from time import sleep

def main_call_success():
  print "main_call_success: Call succeeded"

def main_call_failure():
  sleep(3)
  raise Exception("Exception in main_call_failure")

def random_call():
  if randrange(0,10) < 2: 
    print "Success"
    return main_call_success()
  else: 
    print "Failure"
    return main_call_failure()

cb = CircuitBreaker()

for x in range(0,1000):
  sleep(1)
  try:
    cb.protect(random_call)
  except Exception as e:
    print e
