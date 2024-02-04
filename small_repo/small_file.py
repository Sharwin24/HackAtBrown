from large_file import Larger

class SmallClass:
  
	def __init__(self):
		self.large = Larger()

	def smallFunction(self):
		pass

	def helpingHand(self):
		self.large.functionNumber1()
		self.large.functionNumber2()