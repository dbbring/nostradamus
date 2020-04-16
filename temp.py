#! /usr/bin/env python
# ======================= Gen Imports ========================

# ====================== Custom Imports ======================
from data_operations.utils.scrapers import SEC_Edgar
# Run a historical search to find other companies listed with the same address??
temp = []
sec = SEC_Edgar('mcf')
if sec.is_valid:
  _sec = sec.make_sec_model()

  comps = sec.get_related_companies()
  for ticker in comps:
    p_p = sec.make_arr_peer_performance_model(ticker)
    temp = temp + p_p

print('Done')
print(_sec)
print(temp)


