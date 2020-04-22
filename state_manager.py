import pickle as pk

class StateManager():
    def __init__(self, last_exit_file, state_file ):
        self.last_exit_file = last_exit_file
        self.state_file = state_file


    def is_last_exit_from_reload(self):
        try:
            with open(self.last_exit_file,'rb') as exit_file:
                last_exit = pk.load(exit_file)
                # print(last_exit)
        except FileNotFoundError or FileExistsError as e:
            print(e)
            self.save_last_exit(last_exit_state='Exit')
            last_exit = 'Exit'
            pass

        if last_exit == 'Reload':
            return True

        elif last_exit == 'Exit':
            return False


    def save_gpi_state(self, gpi_stream_dict):
        state_dict = {}
        for gpi, obj in gpi_stream_dict.items():
            state_dict[gpi] = obj.in_cue

        with open(self.state_file, 'wb') as self.state_file:
                pk.dump(state_dict, self.state_file, protocol=pk.\
                    HIGHEST_PROTOCOL)
        self.save_last_exit()


    def load_gpi_state(self):
        with open(self.state_file,'rb') as state_file:
            loaded_dict = pk.load(state_file)
            return loaded_dict


    def save_last_exit(self, last_exit_state = 'Reload'):
        with open(self.last_exit_file, 'wb') as self.state_file:
            pk.dump(last_exit_state, self.state_file, protocol=pk.\
                HIGHEST_PROTOCOL)