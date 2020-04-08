#! /usr/bin/env python
# ======================= Gen Imports ========================

# ====================== Custom Imports ======================
from data_operations.utils.scrapers import SEC_Edgar

sec = SEC_Edgar('CHU')
if sec.is_valid_cik:
  sec.make_peer_performance_model()
