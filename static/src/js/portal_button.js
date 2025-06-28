/** @odoo-module **/  

import PortalSidebar from "@portal/js/portal_sidebar";

PortalSidebar.include({
    events: {
        "click .o_print_btn": "_onChangeButton",
        "click .o_portal_invoice_print ": "_onChangeButton",
    },
    start: function () {
        this.autoStreetTwo = document.querySelector(".o_portal_sidebar_content");

        this.autoFromFirst = document.querySelector(".o_portal_sidebar");
        var button = this.autoFromFirst.querySelector(".o_portal_sale_sidebar");
        if (button) {  
        button.style.backgroundColor = "#DEDEDE"; 
        button.style.borderRadius = "30px";
        button.style.padding = "20px";
        }

        return this._super.apply(this, arguments);
    },
    _onChangeButton: function () {
        console.log("frnjfbruf")
        var button = this.autoStreetTwo.querySelector(".o_print_btn");

        if (button) {          
            button.textContent = "Janvi";
            button.style.color = "yellow";
            button.style.backgroundColor = "green";
        }
    },
});