from captchacker import *
from break_captcha_utils import *

app = captchacker()
app.set_svm_model("models/simulation_based_NEW_C=1000_KERNEL=3.svm	57.1047008547%")
for i in range (10):
    image_url = "https://jaccount.sjtu.edu.cn/jaccount/captcha"
    file = save_image(i,image_url)
    app.set_image(file)
    values,prob,predictions_detail = app.get_result()
    print values, prob,predictions_detail


