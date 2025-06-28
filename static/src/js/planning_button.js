/* @odoo-module */
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { PlanningGanttController } from "@planning/views/planning_gantt/planning_gantt_controller";

patch(PlanningGanttController.prototype, {
    setup(){
        super.setup();
        this.notificationService = useService("notification");
    },

    async planningButton() {
        this.notificationService.add("You closed deal!!!"),{
            title : "Congrats",
            type : "Success",
        }    
    }
});