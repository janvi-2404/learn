/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models" 
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    export_as_JSON(){
        const result = super.export_as_JSON(...arguments);
        result.note = this.getNote();
        return result;
    },

    getNote() {
        return this.note || "";
    },

    setNote(note) {
        this.note = note;
    },

    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        result.note = this.getNote();
        return result;
    },

});