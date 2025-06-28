/** @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { CustomDroapDownPopup } from "@Online_shopping/js/custom_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

export class Location extends Component {
    static template = "point_of_sale.LocationButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
        this.orm = useService("orm");
        this.state = useState({ selectedLocation: _t("Location"), locationAdded: false });
    }

    async onLocationButton() {
        console.log("Hello Janvi!!!..");
        let status = true;
        while (status) {
            const selectedOrderline = this.pos.get_order().get_selected_orderline();
            if (!selectedOrderline) {
                return;
            }
            const order = this.pos.get_order().partner;
            if (order) {
                const locations = await this.orm.call('pos.order', 'get_location', ['true']);
                console.log(locations);
                const { confirmed, payload: input } = await this.popup.add(CustomDroapDownPopup, {
                    // startingValue: selectedOrderline.get_customer_note(),
                    title: _t("Add Location"),
                    locations: locations,
                });
                console.log('input', input);
                if (confirmed) {
                    const order1 = this.pos.get_order();
                    console.log(input);
                    if (!input) {
                        await this.popup.add(ErrorPopup, {
                            title: _t("Invalid Location"),
                            body: _t("Please select the proper location."),
                            cancelKey: true,
                        });
                    } else {
                        order1.setLocation(input);
                        this.state.selectedLocation = input || _t("Location");
                        this.state.locationAdded = !!input;
                        break;
                    }
                } else {
                    break;
                }
            } else {
                await this.popup.add(ErrorPopup, {
                    title: _t("Select Customer"),
                    body: _t("Please select Customer."),
                    cancelKey: true,
                });
                break;
            }
        }
    }
    getLocation(){
        return this.state.locationAdded;
    }
}

ProductScreen.addControlButton({
    component: Location,
    position: ["after", "PosButton"],
});
