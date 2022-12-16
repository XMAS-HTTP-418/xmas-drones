from drone import Drone
class DroneController(Drone):
    def socket_get_incomming_mission(self):
        pass

    def socket_check_for_incomming_mission(self):
        pass

    def socket_check_for_incomming_task(self):
        pass

    def socket_get_task_assignment(self):
        pass

    def socket_receive_status_from_slave(self):
        pass

    def socket_send_status_to_master(self):
        pass

    def vote_for_master(self):
        pass

    def fly_towards(self):
        pass

    def activate_load(self):
        pass

    def assign_task(self):
        pass

    def run(self):
        if self.is_master:
            if self.check_for_incomming_mission():
                self.get_incomming_mission()
                pass # recalculate mission
            if self.socket_receive_status_from_slave():
                pass
        else:
            if self.check_for_incomming_task():
                self.get_task_assignment()
                self.assign_task()
                self.send_status_to_master()

        # proceed with assignment