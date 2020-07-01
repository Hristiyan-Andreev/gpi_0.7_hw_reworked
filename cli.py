import PyInquirer as pyq
import sys
import json

import validators as val
from config_manager import ConfigManager


# Used to manage configuration files - read, write and changes
cfg = ConfigManager('config.json', 'default_config.json')

# Dicts of menu options - to avoid using strings in the whole program
mm_choices = {
    'current_sett': 'Show current settings from file',
    'edit_sett':'Edit settings',
    'preview_ch': 'Preview changes',
    'save_ch': 'Save changes to file',
    'back': 'Exit the program'
}

main_cfg_choices = {
    'elemental':'Elemental server - IP and credentials',
    'stream': 'Stream-GPI pairs - number of streams and GPI mapping',
    'avail': 'Minimum avail duration - Enable/Disable, Duration',
    'back': 'Back to main menu'
}

av_choices = {
    'enable': 'Enable minimum avail duration',
    'duration': 'Set duration',
    'back': 'Go back'
}

el_choices = {
    'ip': 'Enter Elemental Live server IP address',
    'credentials': 'Enter the username and password for access',
    'back': 'Go back'
}


def config_menu():
    config_menu_promt = {
        'type': 'list',
        'name': 'main_choice',
        'message': 'Choose an option\n',
        'choices': [mm_choices['current_sett'], mm_choices['edit_sett'],\
                     mm_choices['preview_ch'], mm_choices['save_ch'],\
                     mm_choices['back']]
    }

    save_promt = {
        'type': 'confirm',
        'name': 'save?',
        'message': 'Are you sure you want to save these changes to the config file?',
        'default': True
    }

    while(True):
        mm_answers = pyq.prompt(config_menu_promt)

        if mm_answers['main_choice'] is mm_choices['back']:
            break

        elif mm_answers['main_choice'] is mm_choices['current_sett']:
            cfg.show_current_cfg()

        elif mm_answers['main_choice'] is mm_choices['edit_sett']:
            main_config_menu()

        elif mm_answers['main_choice'] is mm_choices['preview_ch']:
            cfg.preview_changes()

        elif mm_answers['main_choice'] is mm_choices['save_ch']:
            cfg.preview_changes()
            save_answer = pyq.prompt(save_promt)
            if save_answer['save?'] is True:
                cfg.save_config()


def main_config_menu():
    
    main_options_promt = {
        'type': 'list',
        'name': 'main_option',
        'message': 'What you want to configure?\n',
        'choices': [main_cfg_choices['elemental'], main_cfg_choices['stream'], \
                    main_cfg_choices['avail'], main_cfg_choices['back']]
    }
    while(True):
        answers = pyq.prompt(main_options_promt)

        if answers['main_option'] is main_cfg_choices['back']:
            break

        elif answers['main_option'] is main_cfg_choices['elemental']:
            elemental_menu()

        elif answers['main_option'] is main_cfg_choices['stream']:
            stream_menu()

        elif answers['main_option'] is main_cfg_choices['avail']:
            avail_menu()


def elemental_menu():
    
    elemental_promt = [
        {
            'type': 'list',
            'name': 'elemental',
            'message': 'Elemenal Live server options\n',
            'choices': [el_choices['ip'], el_choices['credentials'], \
                        el_choices['back']]
        },
        {
            'type': 'input',
            'name': 'elemental_ip',
            'message': 'Enter the Elemenal Live server IP address - without port',
            'validate': val.IpValidator,
            'when': lambda elemental_answers: elemental_answers['elemental'] \
                is el_choices['ip'],
            # 'filter': lambda val: float(val)
        },
        {
            'type': 'input',
            'name': 'elemental_user',
            'message': 'Enter Elemental Live username',
            'when': lambda elemental_answers: elemental_answers['elemental'] \
                is el_choices['credentials']
        },
        {
            'type': 'password',
            'name': 'elemental_pass',
            'message': 'Enter Elemental Live password',
            'when': lambda elemental_answers: elemental_answers['elemental'] \
                is el_choices['credentials']
        }
    ]
    while(True):

        elemental_answers = pyq.prompt(elemental_promt)

        if elemental_answers['elemental'] is el_choices['ip']:
            cfg.NEW_CONFIG['elemental_ip'] = elemental_answers['elemental_ip']

        elif elemental_answers['elemental'] is el_choices['credentials']:
            cfg.NEW_CONFIG['elemental_user'] = elemental_answers['elemental_user']
            cfg.NEW_CONFIG['elemental_pass'] = elemental_answers['elemental_pass']

        elif elemental_answers['elemental'] is el_choices['back']:
            print(cfg.NEW_CONFIG)
            break


def stream_menu():

    stream_num_promt = [
        {
            'type': 'input',
            'name': 'gpi_num',
            'message': 'Enter the number of GPI-Stream pairs',
            # 'validate':
            # 'filter': lambda input: int(input)
        }
    ]

    while(True):

        stream_answers = pyq.prompt(stream_num_promt)
        num_of_streams = int(stream_answers['gpi_num'])

        gpi_to_event = {}
        for stream in range(1, num_of_streams+1):
            gpi_promt = [
                {
                    'type': 'input',
                    'name': 'gpi_{}'.format(stream),
                    'message': 'Enter the GPI pin for GPI-Stream pair number ({}):'.format(stream),
                    # 'validate': lambda input: not isinstance(input, int) or 'Enter an int value',
                    # 'filter': lambda input: int(input)
                }
            ]
            gpi_answer = pyq.prompt(gpi_promt)
            gpi_pin = gpi_answer['gpi_{}'.format(stream)]

            stream_promt = [
                {
                    'type': 'input',
                    'name': 'stream_{}'.format(stream),
                    'message': 'Enter the Elemental event number for GPI ({}):'.format(gpi_pin),
                }
            ]
            stream_answer = pyq.prompt(stream_promt)
            event_number = stream_answer['stream_{}'.format(stream)]

            gpi_to_event[gpi_pin] = event_number
        
        print(gpi_to_event)
        done_with_streams_promt = [
            {
                'type': 'list',
                'name': 'done?',
                'message': 'Is the mapping correct?\n',
                'choices': ['Yes, Save & Exit', 'No, edit the GPI-Stream pairs again']
            }
        ]
        done_answer = pyq.prompt(done_with_streams_promt)
        
        if done_answer['done?'] is 'Yes, Save & Exit':
            cfg.NEW_CONFIG['gpi_to_event'] = gpi_to_event
            break
        

def avail_menu():
    avails_promt = [
        {
            'type': 'list',
            'name': 'avail',
            'message': 'Avail duration options',
            'choices': [av_choices['enable'], av_choices['duration'], \
                        av_choices['back']]
        },
        {
            'type': 'list',
            'name': 'enable',
            'message': 'Do you want to enable minimum avail duration',
            'choices': ['Yes', 'No'],
            'when': lambda avails: avails['avail'] is av_choices['enable']
        },
        {
            'type': 'input',
            'name': 'avail_duration',
            'message': 'Enter the minimum avail duration in seconds',
            'validate': val.AvDurValidator,
            'when': lambda avails: avails['avail'] is av_choices['duration'],
            'filter': lambda val: float(val)
        }
    ]
    while(True):

        avails = pyq.prompt(avails_promt)

        if avails['avail'] is av_choices['enable']:
            cfg.NEW_CONFIG['min_avail_enabled'] = True if avails['enable'] == 'Yes' else False
            print(cfg.NEW_CONFIG)

        elif avails['avail'] is av_choices['duration']:
            cfg.NEW_CONFIG['min_avail_duration'] = avails['avail_duration']
            print(cfg.NEW_CONFIG)

        if avails['avail'] is av_choices['back']:
            break
        
  
def whole_menu():

    config_menu()           
    return 0


if __name__ == '__main__':
    try:
        whole_menu()
    except KeyboardInterrupt:
        print('Will miss you')
    finally:
        print('We are done!')