/** @odoo-module */

// import { OrderWidget } from "@point_of_sale/app/generic_components/order_widget/order_widget";

// export class CustomOrderWidget extends OrderWidget {
//     static template = 'point_of_sale.quantityAdded'; 

//     static props = {
//         ...OrderWidget.props, 
//         productCount: { type: Function, optional: true },
//     };

//     setup() {
//         super.setup();
//         this.productCount = this.getProductCount();
//     }

//     get getProductCount() {
//         return this.pos.get_order().get_orderlines().length;
//     }
// }

import { Component } from "@odoo/owl";
import { useListener } from '@web/core/utils/hooks';

class PosScreen extends Component {
    setup() {
        super.setup();
        
        // useListener(this.env.pos, 'change:selectedOrderLine', this._onSelectedOrderChange);
    }

        async _onSelectedOrderChange() {
        return this.pos.get_order().get_orderlines().length;
        // if (this.env.pos && this.env.pos.get_order()) {
        //     const selectedOrder = this.env.pos.get_order();
        //     this.state.totalProductCount = selectedOrder.total_product_count || 0;
        // } else {
        //     this.state.totalProductCount = 0;
        // }
    }
}

PosScreen.template = 'PosScreen';

export default PosScreen;
