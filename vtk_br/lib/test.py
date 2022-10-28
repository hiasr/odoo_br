#!/usr/bin/env python3
import litus

assert litus.get_company_id("VTK Bedrijvenrelaties") == "10"

assert litus.send_activation("17452") == True

# print(litus.create_company("Test1"))
