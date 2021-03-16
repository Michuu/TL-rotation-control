#%%
from elliptec import Motor, find_ports

ports = find_ports()
#%%
motor=Motor(ports[0].device)
# %%
motor.move_absolute(360)
#%%
motor.get_position()
#%%
motor.home()
