/** @odoo-module **/  

import {WebsiteSale} from "@website_sale/js/website_sale";

WebsiteSale.include({
    events: Object.assign({}, WebsiteSale.prototype.events, {
        "change select[name='state_id']": "_onChangeState",
        "change select[name='city_id']": "_onChangeCity",
        "keyup .form-control ": "_onInputKeyup",
        "input input[name='street2']": "_inputAdd",
        "keydown .form-control ": "_onInputkeydown",
        "submit .a-submit": "_onSaveAddress",
    }),
    start: function () {
        this.autoStreetCity = document.querySelector(".div_street2");
        this.autoStreetTwo = document.querySelector(".o_wsale_address_fill");

        return this._super.apply(this, arguments);
    },
    _onChangeState: function () {
        console.log("xyz")
        this.autoStreetCity.querySelectorAll("input").forEach((input) => {
                                input.value = "Janvi";
                            });
    },

    _onInputKeyup: function (event) {
        console.log("Key pressed up: " + event.key);
    },

    _inputAdd: function(){
        var button = this.autoStreetTwo.querySelectorAll(".form-control ");
        // button.style.color = "#FCFCFC";
        console.log("wenfkjrkjf")
    },

    _onInputkeydown: function(event){
        console.log("Key pressed down: " + event.key);
    },

    _onSaveAddress: function(){
        console.log("Address Saved");
    }
});