frappe.listview_settings['Attendance'] = {
	add_fields: ["status", "attendance_date"],
	get_indicator: function (doc) {
		if (["Present", "Work From Home"].includes(doc.status)) {
			return [__(doc.status), "green", "status,=," + doc.status];
		} else if (["Absent", "On Leave"].includes(doc.status)) {
			return [__(doc.status), "red", "status,=," + doc.status];
		} else if (doc.status == "Half Day") {
			return [__(doc.status), "orange", "status,=," + doc.status];
		}
	},
	onload: function(list_view) {
		let me = this;
		const months = moment.months()
		const years = (back) => {
			const year = new Date().getFullYear();
			return Array.from({length: back}, (v, i) => year - back + i + 1);
		  }
		  
		
		list_view.page.add_inner_button( __("Mark Attendance"), function(){
			let dialog = new frappe.ui.Dialog({
				title: __("Mark Attendance"),
				fields: [
					{
						fieldname: 'employee',
						label: __('For Employee'),
						fieldtype: 'Link',
						options: 'Employee',
						reqd: 1,
						onchange: function(){
							dialog.set_df_property("unmarked_days", "hidden", 1);
							dialog.set_df_property("status", "hidden", 1);
							dialog.set_df_property("month", "value", '');
							dialog.set_df_property("year", "value", '');
							dialog.set_df_property("unmarked_days", "options", []);
						}
					},
					{
						label: __("For Year"),
						fieldtype: "Select",
						fieldname: "year",
						options: years(2),
						reqd: 1,
						onchange: function(){
						}
					},
					{
						label: __("For Month"),
						fieldtype: "Select",
						fieldname: "month",
						options: months,
						reqd: 1,
						onchange: function(){
							if(dialog.fields_dict.employee.value && dialog.fields_dict.month.value) {
								dialog.set_df_property("status", "hidden", 1);
								dialog.set_df_property("unmarked_days", "options", []);
								dialog.set_df_property("status", "value", "Present");
								me.get_multi_select_options(dialog.fields_dict.employee.value, dialog.fields_dict.month.value, dialog.fields_dict.year.value).then(options =>{
									dialog.set_df_property("unmarked_days", "hidden", 0);
									dialog.set_df_property("unmarked_days", "options", options);
									
								});
								
							}
						}
					},
					{
						label: __("Status"),
						fieldtype: "Select",
						fieldname: "status",
						options: ["Present", "Absent", "Half Day", "Work From Home"],
						hidden:1,
						reqd: 0,

					},
					{
						label: __("Unmarked Attendance for days"),
						fieldname: "unmarked_days",
						fieldtype: "MultiCheck",
						options: [],
						columns: 2,
						hidden: 1
					},

				],
				primary_action(data){
					data.status = "Present"
					frappe.confirm(__('Mark attendance as <b>' + data.status + '</b> for <b>' + data.month +'</b>' + ' on selected dates?'), () => {
						console.log(data)
						frappe.call({
							method: "erpnext.hr.doctype.attendance.attendance.mark_bulk_attendance",
							args: {
								data : data
							},
							callback: function(r) {
								if(r.message === 1) {
									frappe.show_alert({message:__("Attendance Marked"), indicator:'blue'});
									cur_dialog.hide();
								}
							}
						});
					});
					dialog.hide();
					list_view.refresh();
				},
				primary_action_label: __('Mark Attendance')

			});
			dialog.show();
		});
			list_view.page.add_inner_button( __("Mark Pointage du mois"), function(){
			let dialog = new frappe.ui.Dialog({
				title: __("Mark Pointage"),
				fields: [
					{
						fieldname: 'employee',
						label: __('For Employee'),
						fieldtype: 'Link',
						options: 'Employee',
						reqd: 1,
						onchange: function(){
							dialog.set_df_property("month", "value", '');

						}
					},
					{
						label: __("For year"),
						fieldtype: "Select",
						fieldname: "year",
						options: years(2),
						reqd: 1,
						onchange: function(){
							if(dialog.fields_dict.employee.value && dialog.fields_dict.month.value) {

								
							}
						}
					},
					
					{
						label: __("For Month"),
						fieldtype: "Select",
						fieldname: "month",
						options: months,
						reqd: 1,
						onchange: function(){
							if(dialog.fields_dict.employee.value && dialog.fields_dict.month.value) {

								
							}
						}
					},
					
				],
				primary_action(data){
					frappe.confirm(__('Mark attendance as <b>' + data.status + '</b> for <b>' + data.month +'</b>' + ' on selected dates?'), () => {
						console.log(data)
						frappe.call({
							method: "pointage_cdk.events.eventAttendance.mark_bulk_attendance_pointage",
							args: {
								data : data
							},
							callback: function(r) {
								if(r.message === 1) {
									frappe.show_alert({message:__("Attendance Marked"), indicator:'blue'});
									cur_dialog.hide();
									
								}
							}
							
						});
						
						frappe.set_route("Form", "pointage/view/report");
						list_view.refresh();
					});
					
					dialog.hide();
					list_view.refresh();
					
				},
				primary_action_label: __('Mark Attendance')

			});
			dialog.show();

		
		});
	},


	get_multi_select_options: function(employee, month, year){
		return new Promise(resolve => {
			frappe.call({
				method: 'erpnext.hr.doctype.attendance.attendance.get_unmarked_days',
				async: false,
				args:{
					employee: employee,
					month: month,
					year: year
				}
			}).then(r => {
				var options = [];
				for(var d in r.message){
					var momentObj = moment(r.message[d], 'YYYY-MM-DD');
					var date = momentObj.format('DD-MM-YYYY');
					options.push({ "label":date, "value": r.message[d] , "checked": 1});
				}
				resolve(options);
			});
		});
	}
};
