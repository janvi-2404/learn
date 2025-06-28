/* @odoo-module */
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";

class AutoSaveController extends FormController {
    async autoSave() {
        alert("Hello, Janvi");
        const records = this.model.root.selection;
        console.log(records);
        const res = await this.orm.call(this.model.config.resModel, 'generate_report');
        // console.log(res)
        if (res) {
            await this.actionService.doAction(res, {});
        }    
    }
}

AutoSaveController.template = "Online_shopping.autoSave";

export const modelInfoView = {
    ...formView,
    Controller: AutoSaveController,
};

registry.category("views").add("auto_save", modelInfoView);