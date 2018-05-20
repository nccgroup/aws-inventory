import $ from 'jquery';


export const JS_TREE_CONF = {
    "core" : {
        "themes": {"icons": true, "responsive": true},
        "force_text": true,
    },
    "contextmenu": {
        "items": {
            "toggle_siblings": {
                "label": "Toggle children",
                "separator_after": true,
                "action": function (data) {
                    let inst = $.jstree.reference(data.reference),
                        obj = inst.get_node(data.reference);
                        if (inst.is_closed(obj)) {
                            inst.open_node(obj);
                        }
                        for (var i = 0; i < obj.children.length; i++) {
                            inst.toggle_node(inst.get_node(obj.children[i]));
                        }
                }
            },
            "toggle_children": {
                "label": "Toggle descendants",
                "action": function (data) {
                    let inst = $.jstree.reference(data.reference),
                        obj = inst.get_node(data.reference);
                        if (inst.is_open(obj)) {
                            inst.close_all(obj);
                        }
                        else {
                            inst.open_all(obj);
                        }
                }
            }
        }
    },
    "types": {
        "default": {},
        "root": {"icon": "glyphicon glyphicon-home"},
        "service": {"icon": "glyphicon glyphicon-cloud"},
        "region": {"icon": "glyphicon glyphicon-globe"},
        "operation": {"icon": "glyphicon glyphicon-play"},
        "leaf": {"icon": "glyphicon glyphicon-stop"},
        "response_metadata": {}
    },
    "plugins": ["contextmenu", "search", "types"]
}