from core import Mrak
import systray

m = Mrak("../test/testconfig.yaml")
systray.run(m)