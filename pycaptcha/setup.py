#!/usr/bin/env python
from distutils.core import setup
from setup.my_install_data import *

setup (name = "PyCAPTCHA",
       version = "0.4",
       description = "A Python framework for CAPTCHA tests",
       maintainer = "Micah Dowty",
       maintainer_email = "micah@navi.cx",
       license = "MIT",
       packages = [
           'Captcha',
           'Captcha.Visual',
       ],
       cmdclass = {
           'install_data': my_install_data,
       },
       data_files = [Data_Files(
           preserve_path = 1,
           base_dir      = 'install_lib',
           copy_to       = 'Captcha/data',
           strip_dirs    = 2,
           template      = [
               'graft Captcha/data',
           ],
       )],
       )

