/* @odoo-module */
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { onMounted, useRef, useState } from "@odoo/owl";

export class CustomDroapDownPopup extends AbstractAwaitablePopup {
    static template = "Online_shopping.CustomDropDownPopup";
    static defaultProps = {
        cancelText: _t("Cancel"),
        confirmText: _t("Save"),
        title: _t("Customer Details"),
        locations: [],
    };
    setup() {
        super.setup();
        this.state = useState({ inputValue: this.props.startingValue });
    }
    getPayload() {
        return this.state.inputValue;
    }

}