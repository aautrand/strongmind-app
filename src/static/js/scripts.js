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
                alert("Failed to create pizza: " + xhr.responseText);
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
                alert("Failed to create pizza: " + xhr.responseText["message"]);
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
                alert("Failed to delete pizza: " + xhr.responseText["message"]);
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
