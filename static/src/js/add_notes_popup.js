/** @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { TextAreaPopup } from "@point_of_sale/app/utils/input_popups/textarea_popup";
import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

export class AddNote extends Component {
    static template = "point_of_sale.AddNotes";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
    }

    // async onButtonAddedNote(){
    //     console.log("dfgserdfrfdgh");
    //     const order= await this.popup.add(TextAreaPopup, {
    //         title: _t("Add Notes"),
    //     });
    //     console.log(order);
    // }

    async onButtonAddedNote(){
        // const { confirmed, payload: note } = await this.popup.add(TextAreaPopup, {
        //     title: _t("Add Notes"),
        // });
        const selectedOrderline = this.pos.get_order().get_selected_orderline();
        const order = this.pos.get_order();
        if (!selectedOrderline) {
            return;
        }
        const { confirmed, payload: inputNote } = await this.popup.add(TextAreaPopup, {
            title: _t("Add Note"),
        });

        if (confirmed) {
            order.setNote(inputNote);
            // selectedOrderline.set_customer_note(inputNote);
            // selectedOrderline.setNote(inputNote);
        }  
    }
}

ProductScreen.addControlButton({
    component: AddNote,
    position: ["after", "PosButton"],
});

