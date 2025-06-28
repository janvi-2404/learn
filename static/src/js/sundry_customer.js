/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PartnerListScreen } from "@point_of_sale/app/screens/partner_list/partner_list";

patch(PartnerListScreen.prototype, {
    
    onSundeyCustomer(){
        console.log("hello good morning")
        var data = this.pos.partners
        for (let i of data){
            if (i.id == 14){
            console.log(i)
            this.state.selectedPartner = i;
            this.props.resolve({ confirmed: true, payload: this.state.selectedPartner });
            this.pos.closeTempScreen();
            break
            }
        }
    },


    // onSundeyCustomer(){
    //     console.log("Hello Good Morning");
    //     console.log("props:", this.props);
    //     if (!this.props.partners) {
    //         console.error("Partners data is not available in props.");
    //         return;
    //     }
    //     const sundryCustomers = this.props.partners.filter(partner => partner.is_sundry_customer);
        
    //     if (sundryCustomers.length > 0) {
    //         const selectedPartner = sundryCustomers[0];
    //         console.log(selectedPartner);
    //         this.state.selectedPartner = selectedPartner;
    //         this.props.resolve({ confirmed: true, payload: this.state.selectedPartner });
    //         this.props.closeTempScreen();
    //     } else {
    //         console.log("No sundry customers found.");
    //     }
    // },
});