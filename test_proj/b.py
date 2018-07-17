from test_proj.a import A

class B:
  def f1(self, x):
    print(x)
    self.f2(x)
  def f2(self, l):
    if (l < 15):
      a = A()
      a.f2(l)
    else:
      a = l / 0
