class A:
  def f1(self, x):
    print(x)
    i = int(x)
    self.f2(x)
  def f2(self, x):
    print(x)
