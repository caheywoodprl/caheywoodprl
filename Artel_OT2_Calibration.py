
from opentrons import protocol_api
from opentrons.types import Location, Point

metadata = {
    'protocolName': 'OT-2 Artel Verification',
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
    
    #Running Baseline only = 1
    #Running Large Volumes only = 2
    #Running both basline & large volumes = 3
    
    type = input('enter in 1 for baseline only, 2 for large volumes only, 3 for both baseline and large volumes')
    
    protocol.pause(type)

#Baseline Addition ONLY
    if type == '1':
        r_p.pick_up_tip(tiprack.wells()[tip_pickup_count])
        for j in range(0,11,4):
            for i in range(8):
                w = j + 1
                x = j + 2
                z = j + 3
                r_p.aspirate(1000,reservoir['A1'].bottom(10))
                r_p.dispense(100, reservoir['A1'].bottom(10))
                r_p.dispense(200, baseline.rows()[i][j].bottom(5))
                r_p.dispense(200, baseline.rows()[i][w].bottom(5))
                r_p.dispense(200, baseline.rows()[i][x].bottom(5))
                r_p.dispense(200, baseline.rows()[i][z].bottom(5))
                r_p.dispense(100, reservoir['A1'].bottom(10))
                r_p.blow_out()
        r_p.drop_tip(empty_tiprack.wells()[tip_droptip_count])        
        tip_droptip_count += 1
        tip_pickup_count += 1
        protocol.pause('Please remove baseline plate from the deck')

#Large Volume Dispense ONLY
    if type=='2':
        for j in range(0,11,2):
            for i in range(8):
                w = j + 1 
                r_p.pick_up_tip(tiprack.wells()[tip_pickup_count])
                tip_pickup_count += 1
                r_p.air_gap(2)
                r_p.aspirate(400, reservoir['A2'].bottom(10))
                r_p.dispense(200, plate.rows()[i][j].bottom(5))
                r_p.dispense(200, plate.rows()[i][w].bottom(5))
                r_p.blow_out()
                r_p.drop_tip(empty_tiprack.wells()[tip_droptip_count])
                tip_droptip_count += 1
                
 
#Baseline & Large Volume Dispense ONLY 
    if type=='3':
        r_p.pick_up_tip(tiprack.wells()[tip_pickup_count])
        for j in range(0,11,4):
            for i in range(8):
                w = j + 1
                x = j + 2
                z = j + 3
                r_p.aspirate(1000,reservoir['A1'].bottom(10))
                r_p.dispense(100, reservoir['A1'].bottom(10))
                r_p.dispense(200, baseline.rows()[i][j].bottom(5))
                r_p.dispense(200, baseline.rows()[i][w].bottom(5))
                r_p.dispense(200, baseline.rows()[i][x].bottom(5))
                r_p.dispense(200, baseline.rows()[i][z].bottom(5))
                r_p.dispense(100, reservoir['A1'].bottom(10))
                r_p.blow_out()
        r_p.drop_tip(empty_tiprack.wells()[tip_droptip_count])        
        tip_droptip_count += 1
        tip_pickup_count += 1
    
        protocol.pause('Please remove baseline plate from the deck')
        
        for j in range(0,11,2):
            for i in range(8):
                w = j + 1 
                r_p.pick_up_tip(tiprack.wells()[tip_pickup_count])
                tip_pickup_count += 1
                r_p.air_gap(2)
                r_p.aspirate(400, reservoir['A2'].bottom(10))
                r_p.dispense(200, plate.rows()[i][j].bottom(5))
                r_p.dispense(200, plate.rows()[i][w].bottom(5))
                r_p.blow_out()
                r_p.drop_tip(empty_tiprack.wells()[tip_droptip_count])
                tip_droptip_count += 1