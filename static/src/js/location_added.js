/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models" 
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    export_as_JSON() {
        const result = super.export_as_JSON(...arguments);
        result.location_added = this.location_added || false;
        // result.location_added = this.getLocation();
        return result;
    },

    setLocation(location_added){
        this.location_added = location_added;
        console.log("location_added",location_added);
    },

    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        result.location_add = this.location_added || "";
        return result;
    },
});