/** @odoo-module */

import { useService } from "@web/core/utils/hooks";
// import { TextAreaPopup } from "@point_of_sale/app/utils/input_popups/textarea_popup";
import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

export class ProductOrderButton extends Component {
    static template = "point_of_sale.ProductOrderButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
        this.orm = useService("orm");
    }

    async onProductOrderButton() {
        console.log("Hello Good Morning!!!...")
        var self = this
        await this.orm.call(
            "product.order", "all_orders", ['true'], {}
        ).then(function (result) {
            console.log(result)
            self.pos.showScreen('ProductOrderScreen', {
                data: result,
                new_order: false
            });
        })
    }

}

ProductScreen.addControlButton({
    component: ProductOrderButton,
});