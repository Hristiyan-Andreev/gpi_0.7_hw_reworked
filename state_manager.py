import pickle as pk

class StateManager():
    def __init__(self, last_exit_file, state_file ):
        self.last_exit_file = self.last_exit_file
        self.state_file = self.state_file


    def is_last_exit_from_reload(self):
        try:
            with open(self.last_exit_file,'rb') as exit_file:
                last_exit = pk.load(exit_file)
                print(last_exit)
        except Exception as e:
            print(e)
            pass

        if last_exit == 'Reload':
            return True

        elif last_exit == 'Exit':
            return False


    def save_gpi_state(self, gpi_cue_state_dict):
        with open(self.state_file, 'wb') as self.state_file:
                pk.dump(gpi_cue_state_dict, self.state_file, protocol=pk.\
                    HIGHEST_PROTOCOL)
        save_last_exit()


    def load_gpi_state(self):
        with open(self.state_file,'rb') as state_file:
            loaded_dict = pk.load(state_file)
            return loaded_dict


    def save_last_exit(self, last_exit_state = 'Reload'):
        with open(self.last_exit_file, 'wb') as self.state_file:
            pk.dump(last_exit_state, self.state_file, protocol=pk.\
                HIGHEST_PROTOCOL)