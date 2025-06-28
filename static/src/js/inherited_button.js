/* @odoo-module */
    import { patch } from "@web/core/utils/patch";
    import { ExpenseListController } from "@hr_expense/views/list";

    patch(ExpenseListController.prototype, {

        async actionNewButton() {
            const records = this.model.root.selection;
            console.log(records);
            const res = await this.orm.call(this.model.config.resModel, 'generate_report', [records.map((record) => record.resId)]);
            // console.log(res)
            if (res) {
                await this.actionService.doAction(res, {});
            }
            // const recordId = records.map((a) => a.resId)
            // console.log(typeof records)
            // console.log(records)
            // console.log(recordId)
            // for (var key in records) {
            //     console.log(key + ":" + records[key])
            // }
            // let keys = records[key].data
            // console.log(keys) 
            // console.log(keys.name)
            // console.log(keys.total_amount)
            // console.log(keys.company_id)

            // console.log(records.reduce(()))
            // for (const key in records) {
            //     const orderId = records[key].data.id;
            //     rpc.query({
            //         model: 'hr.expense',
            //         method: 'generate_report',
            //         args: [orderId],
            //     }).then(result => {
            //         console.log('Report generated:', result);
            //     }).fail(error => {
            //         console.error('Failed to generate report:', error);
            //     });
            // } 
        }
    });