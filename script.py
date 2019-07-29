# !/usr/bin/python

import random

def homer_read(hwaddr):
    print ("homer_read")
    switch = {
        "e2006": 0,  # max pstate ultra turbo
        "e2018": 0,  # pstate id for 0
        "1f8001": 0, # P8 occ pstate version
        "1f8003": 0, # P8 pstate min
        "1f8010": 0, # P8 pstate id for 0
        "e2000": 1,  # occ data area
        "e2002": 1,  # occ_role master/slave*/
        "e2004": 1,  # pstate nom
        "e2005": 1,  # pstate turbo
        "e2020": 1,  # pstate id for 1
        "e2818": 1,  # pstate ultra turbo
        "e2b85": 1,  # opal dynamic data (runtime)
        "1f8000": 1, # P8 occ pstate valid
        "1f8002": 1, # P8 throttle
        "1f8004": 1, # P8 pstate nom
        "1f8005": 1, # P8 pstate turbo
        "1f8012": 1, # vdd voltage identifier
        "1f8013": 1, # vcs voltage identifier
        "1f8018": 1, # P8 pstate id for 1
        "e2003": 2,  # pstate min (2 as pstate min)
        "e2028": 2,  # pstate id for 2
        "1f8006": 2, # P8 pstate ultra turbo
        "1f8020": 2, # P8 pstate id for 2
        "e2001": 0x90,  # major version
        # 3000 khz frequency for 0": 0, 1, and 2 pstates
        "e201c": 3000,
        "e2024": 3000,
        "e202c": 3000,
        # P8 frequency for 0": 0, 1, and 2 pstates
        "1f8014": 3000,
        "1f801c": 3000,
        "1f8024": 3000,
        "0": 0x1000000000000000,      # homer base
        "e2008": 0x1000000000000000,  # occ data area + 8
        "1f8008": 0x1000000000000000, # P8 occ data area + 8
        # homer base access to get homer image pointer
        "200008": 0x1000000000000000
    }
    return switch.get(hwaddr, 0)

def occ_read(hwaddr):
    print ("occ_read")
    switch = {
        "580000": 1, # occ sensor data block
        "580001": 1, # valid
        "580002": 1, # version
        "580004": 1, # reading_version
        "580008": 1, # nr_sensors
        "580010": 1, # names_offset
        "580014": 1, # reading_ping_offset
        "58000c": 1, # reading_pong_offset
        "580023": 1, # structure_type
        "58000d": 0x30,   # name length
        "580022": 0x0040, # occ sensor loc core
        "580003": 0x0080, # occ sensor type power
        "580005": 0x1000, # sensor name
        "58001e": 0x8e00, # HWMON_SENSORS_MASK
        "580020": 0x8e00,
        # P8 slw base access for slw image size
        "0": 0x1000000000000000
    }
    return switch.get(hwaddr, 0)

def randomint(hwaddr):
    switch = {
        "580001": 1, # valid
        "580002": 1, # version
        "580004": 1, # reading_version
        "580008": 1, # nr_sensors
        "580010": 1, # names_offset
        "580014": 1, # reading_ping_offset
        "58000c": 1, # reading_pong_offset
        "580023": 1, # structure_type
        "58000d": 0x30,   # name length
        "580022": 0x0040, # occ sensor loc core
        "580003": 0x0080, # occ sensor type power
        "580005": 0x1000, # sensor name
        "58001e": 0x8e00, # HWMON_SENSORS_MASK
        "580020": 0x8e00,
        "e2006": 0,  # max pstate ultra turbo
        "1f8001": 0, # P8 occ pstate version
        "1f8003": 0, # P8 pstate min
        "1f8010": 0, # P8 pstate id for 0
        "e2000": 1,  # occ data area
        "e2004": 1,  # pstate nom
        "e2005": 1,  # pstate turbo
        "e2818": 1,  # pstate ultra turbo
        "1f8000": 1, # P8 occ pstate valid
        "1f8004": 1, # P8 pstate nom
        "1f8005": 1, # P8 pstate turbo
        "e2003": 2,  # pstate min (2 as pstate min)
        "e2028": 2,  # pstate id for 2
        "1f8006": 2, # P8 pstate ultra turbo
        "e2001": 0x90,  # major version
    }
    return switch.get(hwaddr,random.randint(1, 100))

def hw_size(hw):
    sizes = {
        "occ": 0x700000,
        "homer": 0x300000
    }
    return sizes[hw]

def hw_address(hw, chip_num, cpu_model):
    base = get_base_address(hw, cpu_model)
    val = int(base, 16) + (int(chip_num) * hw_size(hw))
    return val

def xscom_read(hwaddr, chip_num, cpu_model):
    print ("xscom_read")
    switch = {
        "f000f": int(get_base_address('cfam_id', cpu_model), 16),
        "18002": 0,       # ECID2
        # PRD ipoll mask register
        "f0033": 0,
        "1020013": 0,
        # PBA BAR0
        "5012b00": hw_address("homer", chip_num, cpu_model), # P9 homer base address
        "2013f00": hw_address("homer", chip_num, cpu_model), # P8 homer base address
        # PBA BARMASK0
        "5012b04": 0x300000, # P9 homer region size
        "2013f04": 0x300000, # P8 homer region size
        # PBA BAR2
        "5012b02": hw_address("occ", chip_num, cpu_model), # P9 occ common area
        "2013f02": hw_address("occ", chip_num, cpu_model), # P8 occ common area
        # PBA BARMASK2
        "5012b06": 0x700000, # P9 occ common area size
        "2013f06": 0x700000, # P8 occ common area size
        "1010c00": 0,     # PIBAM FIR
        "1010c03": 0,     # PIBAM FIR MASK
        # P9 xscom reset
        "0090018": 0,     # Receive status reg
        "0090012": 0,     # log register
        "0090013": 0,     # error register
        # P8 xscom reset
        "2020007": 0,     # ADU stuff, log register
        "2020009": 0,     # ADU stuff, error register
        "202000f": 0,     # ADU stuff, receive status register*/
        "2013f01": 0,     # PBA stuff
        "2013f03": 0,     # PBA stuff
        "2013f05": 0,     # PBA stuff
        "2013f07": 0,     # PBA stuff
        "2013028": 0,     # CAPP stuff
        "201302a": 0,     # CAPP stuff
        "2013801": 0,     # CAPP stuff
        "2013802": 0,     # CAPP stuff
    }
    return switch.get(hwaddr, -1)


def xscom_write(hwaddr):
    print ("xscom_write")
    switch = {
        # We ignore writes to these
        "f000f": True,       # chip id is RO
        "1010c00": True,     # PIBAM FIR
        "1010c01": True,     # PIBAM FIR
        "1010c02": True,     # PIBAM FIR
        "1010c03": True,     # PIBAM FIR MASK
        "1010c04": True,     # PIBAM FIR MASK
        "1010c05": True,     # PIBAM FIR MASK
        # P9 xscom reset
        "0090018": True,     # Receive status reg
        "0090012": True,     # log register
        "0090013": True,     # error register

        # P8 xscom reset
        "2020007": True,     # ADU stuff, log register
        "2020009": True,     # ADU stuff, error register
        "202000f": True,     # ADU stuff, receive status register

        "2013028": True,     # CAPP stuff
        "201302a": True,     # CAPP stuff
        "2013801": True,     # CAPP stuff
        "2013802": True,     # CAPP stuff
        # PRD ipoll mask register
        "1020013": True,
        "f0033": True,
    }
    return switch.get(hwaddr, False)


def get_base_address(hardware, processor):
    switch = {
        "0": {"xscom": "003fc0000000000",
              "homer": "7ffd800000",
              "occ": "7fff800000",
              "cfam_id": "221ef04980000000"},
        "1": {"xscom": "003fc0000000000",
              "homer": "7ffd800000",
              "occ": "7fff800000",
              "cfam_id": "220ea04980000000"},
        "2": {"xscom": "003fc0000000000",
              "homer": "7ffd800000",
              "occ": "7fff800000",
              "cfam_id": "120d304980000000"},
        "3": {"xscom": "00603fc00000000",
              "homer": "203ffd800000",
              "occ": "203fff800000",
              "cfam_id": "220d104900008000"}
    }
    return switch.get(processor, "").get(hardware, "")
