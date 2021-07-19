from opentrons import protocol_api
from opentrons.types import Location, Point

metadata = {
    'protocolName': 'Reformatting_15mL NEST_96 samples',
    'author': 'Chris Yarka',
    'apiLevel': '2.2'
}

def run(protocol: protocol_api.ProtocolContext):
    #Lights prep
    gpio = protocol._hw_manager.hardware._backend._gpio_chardev

    #labware
    rack1 = protocol.load_labware('nest_32_tuberack_8x15ml_8x15ml_8x15ml_8x15ml','1')
    rack2 = protocol.load_labware('nest_32_tuberack_8x15ml_8x15ml_8x15ml_8x15ml','4')
    rack3 = protocol.load_labware('nest_32_tuberack_8x15ml_8x15ml_8x15ml_8x15ml','7')
    tuberacks = [rack1,rack2,rack3]
    tiprack_1000_1 = protocol.load_labware('opentrons_96_tiprack_1000ul','10')
    empty_tiprack_1000 = protocol.load_labware('opentrons_96_filtertiprack_1000ul','11')
    deepwell_96 = protocol.load_labware('nest_96_wellplate_2ml_deep','3')

    #Pipettes
    r_p = protocol.load_instrument('p1000_single_gen2','right',tip_racks=[tiprack_1000_1])


    # Mapping of Wells
    lookup_table = [
        [#beginning of tube rack 1
        #         tuberack,deepwell    tuberack,deepwell

            {'left': ('D7','A1'),'right': ('A1','A1')},    #empty control sample goes here
            {'left': ('C7','A1'),'right': ('A2','B1')},
            {'left': ('B7','A1'),'right': ('A3','C1')},
            {'left': ('A7','A1'),'right': ('A4','D1')},

            {'left': ('D5','A1'),'right': ('A5','E1')},
            {'left': ('C5','A1'),'right': ('A6','F1')},
            {'left': ('B5','A1'),'right': ('A7','G1')},
            {'left': ('A5','A1'),'right': ('A8','H1')},

            {'left': ('D3','A1'),'right': ('B1','A2')},
            {'left': ('C3','A1'),'right': ('B2','A3')},
            {'left': ('B3','A1'),'right': ('B3','A4')},
            {'left': ('A3','A1'),'right': ('B4','A5')},

            {'left': ('D1','A1'),'right': ('B5','A6')},
            {'left': ('C1','A1'),'right': ('B6','A7')},
            {'left': ('B1','A1'),'right': ('B7','A8')},
            {'left': ('A1','A1'),'right': ('B8','A9')},

            {'left': ('D7','A1'),'right': ('C1','A10')},
            {'left': ('C7','A1'),'right': ('C2','A11')},
            {'left': ('B7','A1'),'right': ('C3','A12')},
            #{'left': ('A7','A1'),'right': ('A4','D4')},

            #{'left': ('D5','A1'),'right': ('D3','C1')},
            #{'left': ('C5','A1'),'right': ('C3','C2')},
            #{'left': ('B5','A1'),'right': ('B3','C3')},
            #{'left': ('A5','A1'),'right': ('A3','C4')},

            #{'left': ('D3','A1'),'right': ('D2','B1')},
            #{'left': ('C3','A1'),'right': ('C2','B2')},
            #{'left': ('B3','A1'),'right': ('B2','B3')},
            #{'left': ('A3','A1'),'right': ('A2','B4')},

            #{'left': ('D1','A1'),'right': ('D1','A1')},
            #{'left': ('C1','A1'),'right': ('C1','A2')},
            #{'left': ('B1','A1'),'right': ('B1','A3')},
            #{'left': ('A1','A1'),'right': ('A1','A4')},

        ], #end of rack1
    ]



    #Pipette max_speeds
    r_p.flow_rate.aspirate = 400
    r_p.flow_rate.dispense = 400
    r_p.flow_rate.blow_out = 400


    tip_droptip_count = 0
    tip_pickup_count = 0

    #Light turns to yellow to indicate protocol is running
    gpio.set_button_light(red=True, green=True, blue=False)

    #Pipetting Actions
    for tuberack_index, tuberack_commands in enumerate(lookup_table):  # go through the three entries CH modified to be just 1 tube rack

        tuberack_lw = tuberacks[tuberack_index]

        for reformatting in tuberack_commands:  # go through the entries for each tube
            r_p.pick_up_tip(tiprack_1000_1.wells()[tip_pickup_count])
            tip_pickup_count += 1

            r_p.aspirate(400, tuberack_lw[reformatting['right'][0]].top(-92))
            r_p.air_gap(150)

            r_p.dispense(1000, deepwell_96[reformatting['right'][1]].bottom(5))
            r_p.blow_out(deepwell_96[reformatting['right'][1]].bottom(5))
            r_p.touch_tip(v_offset=-6,speed=40)
            r_p.air_gap(100) #aspirate any liquid that may be leftover inside the tip



            #Home the Z/A mount. Not the pipette
            protocol._implementation.get_hardware().hardware.home_z(r_p._implementation.get_mount())
            current_location = protocol._implementation.get_hardware().hardware.gantry_position(r_p._implementation.get_mount())
            final_location_xy = current_location._replace(y=300,x=300)
            r_p.move_to(Location(labware=None, point=final_location_xy),force_direct=True)


            r_p.drop_tip(empty_tiprack_1000.wells()[tip_droptip_count])
            tip_droptip_count += 1

    gpio.set_button_light(red=False, green=True, blue=False)
    protocol.pause()
    protocol.home()
    gpio.set_button_light(red=False, green=False, blue=True)
