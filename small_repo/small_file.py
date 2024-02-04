from large_file import LargeClass

class SmallClass:
  
	def __init__(self):
		self.large = LargeClass()

	def smallFunction(self):
		pass

	def helpingHand(self):
		self.large.functionNumber1()
		self.large.functionNumber2()