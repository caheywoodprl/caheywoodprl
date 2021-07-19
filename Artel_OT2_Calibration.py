
from opentrons import protocol_api
from opentrons.types import Location, Point

metadata = {
    'protocolName': 'OT-2 Reformatting Artel Verification',
    'author': 'Catherine Heywood',
    'apiLevel': '2.2'
    }

def run(protocol: protocol_api.ProtocolContext):
    #labware
    reservoir = protocol.load_labware('thomassciporvair_6_reservoir_47000ul', '2')
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '3')
    baseline = protocol.load_labware('corning_96_wellplate_360ul_flat', '6')
    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', '10')
    empty_tiprack = protocol.load_labware('opentrons_96_filtertiprack_1000ul','11')

    #Pipettes
    r_p = protocol.load_instrument('p1000_single_gen2','right',tip_racks=[tiprack])

    #Pipetting Actions
    
    tip_droptip_count = 0
    tip_pickup_count = 0

#Baseline Addition (can comment out if not needed and baseline has been performed)
    r_p.pick_up_tip(tiprack.wells()[tip_pickup_count])
    for j in range(0,11,4):
        for i in range(8):
            w = j + 1
            x = j + 2
            z = j + 3
            r_p.aspirate(1000,reservoir['A1'])
            r_p.dispense(100, reservoir['A1'])
            r_p.dispense(200, baseline.rows()[i][j])
            r_p.dispense(200, baseline.rows()[i][w])
            r_p.dispense(200, baseline.rows()[i][x])
            r_p.dispense(200, baseline.rows()[i][z])
            r_p.dispense(100, reservoir['A1'])
            r_p.blow_out()
    r_p.drop_tip(empty_tiprack.wells()[tip_droptip_count])        
    tip_droptip_count += 1
    #r_p.pause()

#Large Volume Dispense
    for j in range(0,11,2):
        for i in range(8):
            w = j + 1 
            r_p.pick_up_tip(tiprack.wells()[tip_pickup_count])
            tip_pickup_count += 1
            r_p.air_gap(2)
            r_p.aspirate(400, reservoir['A2'])
            r_p.dispense(200, plate.rows()[i][j])
            r_p.dispense(200, plate.rows()[i][w])
            r_p.blow_out()
            r_p.drop_tip(empty_tiprack.wells()[tip_droptip_count])
            tip_droptip_count += 1
