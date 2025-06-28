/* @odoo-module */
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";

class jsClassModelInfo extends FormController {
    actionInfoForm() {
        alert("Hello, Janvi");
    }
}

jsClassModelInfo.template = "Online_shopping.modelInfoBtn";

export const modelInfoView = {
    ...formView,
    Controller: jsClassModelInfo,
};

registry.category("views").add("model_info", modelInfoView);














