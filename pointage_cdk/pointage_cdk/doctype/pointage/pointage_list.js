// Copyright (c) 2021, dHaj and contributors
// For license information, please see license.txt

// frappe.ui.form.on('pointage', {
// 	refresh: function(frm) {

// 	}
// });
frappe.listview_settings['pointage'] = {
	
	onload: function(list_view) {
		const months = moment.months();
		
		const years = (back) => {
			const year = new Date().getFullYear();
			return Array.from({length: back}, (v, i) => year - back + i + 1);
		  }
		list_view.page.add_inner_button( __("Exporter EXCEL"), function(){
			let d = new frappe.ui.Dialog({
				title: __("Export le relevé des heures:"),
				fields:  [
					{
						fieldtype: 'Select',
						label: __('Type de fichier'),
						fieldname:'file_format_type',
						options: ['Excel'],
						default: 'Excel'
					},
					{
						label: __("Pour le mois"),
						fieldtype: "Select",
						fieldname: "month",
						options: months,
						reqd: 1,},
						{
							label: __("For Year"),
							fieldtype: "Select",
							fieldname: "year",
							options: years(2),
							reqd: 1,
							onchange: function(){
							}
						},
				],
				primary_action_label: __('Download'),
				primary_action: (data) => {
					// return new Promise(resolve => {
					// 	frappe.call({
					// 		method: 'pointage_cdk.pointage_cdk.doctype.pointage.pointage.get_data_export',
					// 		async: false,
					// 		args:{
					// 			data: 'April',
					// 		}
					// 	}).then(r => {
					// 		console.log(r)
					// 	});
					// });
					console.log(data.month)
					var URL = "/api/method/pointage_cdk.pointage_cdk.doctype.pointage.pointage.get_data_export?"+"month="+data.month+"&year="+data.year;
        			window.open(URL, '_blank');
				},
			});
			d.show();
		})}}

