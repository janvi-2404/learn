/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";

class jsClassModelIcon extends FormController {
    setup() {
        super.setup();
    }

    actionFormIcon(ev) {
        ev.preventDefault();
        alert("hello");
    }
}

jsClassModelIcon.template = "Online_shopping.modelIconForm";

export const modelIconView = {
    ...formView,
    Controller: jsClassModelIcon,
};

registry.category("views").add("model_order", modelIconView);
