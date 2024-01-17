odoo.define('whatsapp.list_view_button', function(require) {
    "use strict";
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var TreeButton = ListController.extend({
        buttons_template: 'platform_list.buttons',
    });
    var GetPlatformListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TreeButton,
        }),
    });
    viewRegistry.add('get_platform_list_btn_tree', GetPlatformListView);
});