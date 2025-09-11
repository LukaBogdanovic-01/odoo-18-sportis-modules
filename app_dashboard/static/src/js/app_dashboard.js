/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class AppDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.menu = useService("menu");   // servis za menije
        this.apps = [];
        onWillStart(async () => {
            this.apps = await this.orm.searchRead(
                "ir.ui.menu",
                [["parent_id", "=", false], ["name", "!=", "App Dashboard"]],
                ["id", "name", "web_icon", "web_icon_data", "action"]
            );
        });
    }

    openApp(app) {
        this.menu.selectMenu(app.id);
    }

}

AppDashboard.template = "AppDashboardTemplate";
registry.category("actions").add("app_dashboard_client", AppDashboard);

export default AppDashboard;
