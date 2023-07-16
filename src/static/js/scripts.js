$(document).ready(function() {

    $("#saveChanges").click(function(e) {
        e.preventDefault();

        var toppings = [];
        $("input:checkbox[name=toppings]:checked").each(function(){
            toppings.push($(this).val());
        });

        var pizzaData = {
            name: $("#pizzaName").val(),
            toppings: toppings
        }

        $.ajax({
            url: '/api/pizzas',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(pizzaData),
            dataType: 'json',
            success: function (data) {
                $('#newPizzaModal').modal('hide');
                $("#pizzaName").val('');
                $("input:checkbox[name=toppings]:checked").each(function(){
                    $(this).prop('checked', false);
                });
                location.reload();
            },
            error: function (xhr, status, error) {
                var message = JSON.parse(xhr.responseText)["message"];
                alert("Failed to create pizza: " + message);
                $('#newPizzaModal').modal('hide');
                $("#pizzaName").val('');
                $("input:checkbox[name=toppings]:checked").each(function(){
                    $(this).prop('checked', false);
                });
                location.reload();
            }
        });
    });

    $("#updatePizza").click(function(e) {
        e.preventDefault();
        var pizzaId = $("#pizzaId").val();

        var toppings = [];
        $("input:checkbox[name=toppings]:checked").each(function(){
            toppings.push($(this).val());
        });

        var pizzaData = {
            name: $("#pizzaName").val(),
            toppings: toppings
        }

        $.ajax({
            url: '/api/pizzas/'+pizzaId,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(pizzaData),
            dataType: 'json',
            success: function(data) {
                location.reload();
            },
            error: function (xhr, status, error) {
                var message = JSON.parse(xhr.responseText)["message"];
                alert("Failed to update the pizza: " + message);
            }
        });
    });

    $(".deletePizza").click(function(e) {
        e.preventDefault();
        var pizzaId = $(this).data('pizza-id');

        $.ajax({
            url: '/api/pizzas/'+pizzaId,
            type: 'DELETE',
            contentType: 'application/json',
            dataType: 'json',
            success: function(data) {
                location.reload();
            },
            error: function (xhr, status, error) {
                var message = JSON.parse(xhr.responseText)["message"];
                alert("Failed to delete the pizza: " + message);
            }
        });
    });


    $("#saveNewTopping").click(function(e) {
        e.preventDefault();

        var toppings = [];
        $("input:checkbox[name=toppings]:checked").each(function(){
            toppings.push($(this).val());
        });

        var toppingData = {
            name: $("#toppingName").val(),
            toppings: toppings
        }

        $.ajax({
            url: '/api/toppings',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(toppingData),
            dataType: 'json',
            success: function (data) {
                $('#newToppingModal').modal('hide');
                $("#toppingName").val('');
                location.reload();
            },
            error: function (xhr, status, error) {
                var message = JSON.parse(xhr.responseText)["message"];
                alert("Failed to create pizza: " + message);
                $('#newToppingModal').modal('hide');
                $("#toppingName").val('');
                location.reload();
            }
        });
    });

    $(document).on('click', '.editTopping', function(e) {
        e.preventDefault();
        var toppingId = $(this).data('topping-id');
        var toppingName = $(this).data('topping-name');

        $('#toppingUpdateId').val(toppingId);
        $('#toppingUpdateName').val(toppingName);
    });

    $(document).on('click', '.updateTopping', function(e) {
        e.preventDefault();

        var toppingUpdateNameId = $('#toppingUpdateId').val();
        var toppingUpdateNameValue = $('#toppingUpdateName').val();

        var toppingData = {
            name: toppingUpdateNameValue
        }

        $.ajax({
            url: '/api/toppings/'+ toppingUpdateNameId,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(toppingData),
            dataType: 'json',
            success: function(data) {
                location.reload();
            },
            error: function (xhr, status, error) {
                var message = JSON.parse(xhr.responseText)["message"];
                alert("Failed to update the topping: " + message);
            }
        });
    });

    $(".deleteTopping").click(function(e) {
        e.preventDefault();
        var toppingId = $(this).data('topping-id');

        $.ajax({
            url: '/api/toppings/'+toppingId,
            type: 'DELETE',
            contentType: 'application/json',
            dataType: 'json',
            success: function(data) {
                location.reload();
            },
            error: function (xhr, status, error) {
                var message = JSON.parse(xhr.responseText)["message"];
                alert("Failed to delete the topping: " + message);
            }
        });
    });

    $('#newPizzaModal').on('hidden.bs.modal', function () {
        $("#pizzaName").val('');
        $("input:checkbox[name=toppings]:checked").each(function(){
            $(this).prop('checked', false);
        });
    });


});
