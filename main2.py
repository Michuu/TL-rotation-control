#%%
from elliptec import Motor, find_ports

ports = find_ports()
#%%
motor=Motor(ports[0].device)
# %%
pos=motor.get_('position')
pos[1]/(motor.counts_per_rev//motor.range)
# %%
motor.do_('absolute',motor.deg_to_hex(5))
# %%
motor.do_('home')
# %%
motor.deg_to_hex(5)
# %%
