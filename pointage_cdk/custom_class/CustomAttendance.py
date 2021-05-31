from erpnext.hr.doctype.attendance.attendance import Attendance

class CustomAttendance(Attendance):
    def on_submit(self):
        self.my_custom_code()
        super(Attendance, self).on_update()

    def my_custom_code(self):
        print("//////////////////////////////")

        print("//////////////////////////////")
        print("//////////////////////////////")

