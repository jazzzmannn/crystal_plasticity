import packages.pairer as pairer
import packages.orientation as orientation
import packages.angle as angle

# euler_1 = [0.3404, 1.3610, 3.8399]
# euler_2 = [1.2423, 2.9281, 3.4985]
euler_1 = [1.2423, 2.9281, 3.4985]

pr = pairer.Pairer(euler_1, angle.deg_to_rad(60), "cubic")
euler_2 = pr.get_pairing_euler()

print(orientation.get_csl(euler_1, euler_2))
