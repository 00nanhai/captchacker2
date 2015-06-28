#!/usr/bin/env python
#
# A very simple example that creates a random image from the
# PseudoGimpy CAPTCHA, saves and shows it, and prints the list
# of solutions. Normally you would call testSolutions rather
# than reading this list yourself.
#
from Captcha.Visual.Tests import PseudoGimpy

g = PseudoGimpy()
i = g.render()
i.save("output.png")
i.show()
print g.solutions
