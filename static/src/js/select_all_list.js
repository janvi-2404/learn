/* @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { listView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";
import { useService } from '@web/core/utils/hooks';

class SelectAllController extends ListController {
    setup(){
        super.setup();
        this.orm = useService('orm');
    }

    async selectAll() {
        alert("Hello, Janvi");
        const records = this.model.root.selection;
        console.log(records);
        if (records.length > 0) {
            const res = await this.orm.call(this.model.config.resModel, 'download_report', [records.map((record) => record.resId)]);
            if (res) {
                await this.actionService.doAction(res, {});
            }
        } 
    }
}

SelectAllController.template = "Online_shopping.selectAll";

export const modelInfoView = {
    ...listView,
    Controller: SelectAllController,
};

registry.category("views").add("select_all", modelInfoView);