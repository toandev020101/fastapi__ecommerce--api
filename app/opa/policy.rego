package authz

import data

default allow = false

allow {
    input.method == "POST"
    input.action == "add one"
    input.is_admin == true
    input.path == "product"
}

allow {
    input.method == "PUT"
    input.action == "update one"
    input.is_admin == true
    input.path == "product"
}

allow {
    input.method == "DELETE"
    input.action == "remove one"
    input.is_admin == true
    input.path == "product"
}

allow {
    input.method == "DELETE"
    input.action == "remove list"
    input.is_admin == true
    input.path == "product"
}

allow {
    input.method == "GET"
    input.action == "get all"
    input.is_admin == true
    input.path == "order"
}

allow {
    input.method == "GET"
    input.action == "get list"
    input.is_admin == false
    input.path == "order"
}

allow {
    input.method == "POST"
    input.action == "add one"
    input.is_admin == false
    input.path == "order"
}

allow {
    input.method == "PATCH"
    input.action == "change status"
    input.is_admin == true
    input.path == "order"
}

allow {
    input.method == "PATCH"
    input.action == "change status"
    input.is_admin == false
    input.status == "Đã hủy"
    input.path == "order"
}

allow {
    input.method == "DELETE"
    input.action == "remove one"
    input.is_admin == true
    input.path == "order"
}

allow {
    input.method == "DELETE"
    input.action == "remove list"
    input.is_admin == true
    input.path == "order"
}

allow {
    input.method == "GET"
    input.action == "get all"
    input.is_admin == true
    input.path == "payment"
}

allow {
    input.method == "GET"
    input.action == "get one"
    input.is_admin == true
    input.path == "payment"
}

allow {
    input.method == "POST"
    input.action == "process payment"
    input.is_admin == false
    input.path == "payment"
}
