/** @odoo-module */

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
// import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { Component } from "@odoo/owl";
// import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";

export class PosButton extends Component {
    static template = "point_of_sale.PosButton";

    setup() {
        this.pos = usePos();
        // this.popup = useService("popup");
    }

    // async onRemoveAll(){
    //     console.log("dsrsrstrstrsstrs");
    //     const allProduct = this.pos.get_order().get_orderlines();
    //     for (let product in allProduct) {
    //         console.log(product)
    //         this.pos.get_order().removeOrderline(product);
    //         this.currentOrder.removeOrderline(product);
    //     }
    // }

    async onRemoveAll() {
        console.log("dsrsrstrstrsstrs");
        const allProducts = this.pos.get_order().get_orderlines();
        for (let i = allProducts.length - 1; i >= 0; i--) {
            const product = allProducts[i];
            // console.log(product);
            this.pos.get_order().removeOrderline(product);
            console.log(product);
        }
    }

    // async onRemoveAll() {
    //     console.log("dsrsrstrstrsstrs");
    //     const allProducts = [...this.pos.get_order().get_orderlines()];
    //     for (let i = 0; i < allProducts.length; i++){
    //         const product = allProducts[i];
    //         this.pos.get_order().removeOrderline(product);
    //     }
    // }
}

ProductScreen.addControlButton({
    component: PosButton,
    position: ["after", "CustomerButton"],
});