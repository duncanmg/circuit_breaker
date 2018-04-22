from circuit_breaker import *
from random import randrange
from time import sleep

def main_call_success():
  print "main_call_success: Call succeeded"

def main_call_failure():
  sleep(5)
  raise Exception("Exception in main_call_failure")

def random_call():
  if randrange(0,10) < 3: 
    return main_call_success()
  else: 
    return main_call_failure()

cb = CircuitBreaker()
cb.max_age = 30

for x in range(0,1000):
  sleep(1)
  try:
    cb.protect(random_call)
  except Exception as e:
    print e
