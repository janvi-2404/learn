/** @odoo-module */

import { useService } from "@web/core/utils/hooks";
// import { TextAreaPopup } from "@point_of_sale/app/utils/input_popups/textarea_popup";
import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

export class ProductBookingButton extends Component {
    static template = "point_of_sale.ProductBookingButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
    }

    async onProductBookingButton(){
        console.log("Hello Janvi Good Morning!!!...")
    }

}

ProductScreen.addControlButton({
    component: ProductBookingButton,
});