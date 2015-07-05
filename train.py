from captchacker import *
from break_captcha_utils import *

CRANGE = [1000]
KERNEL_TYPE = [RBF, POLY, LINEAR, SIGMOID]
TRAINING_FOLDER = 'DBTraining-Captcha_based'
TRAINING_FOLDER = 'DBTraining-Simulation_based'
TEST_FOLDER = 'DBTest-Captcha_based'
TEST_FOLDER = 'DBTest-Simulation_based'



app = captchacker()
app.generate_simulation_base(True,True,False,True,False)
model_file = app.generate_simulation_based_model()
app.test_based_model(model_file,'DBTest-Simulation_based')


