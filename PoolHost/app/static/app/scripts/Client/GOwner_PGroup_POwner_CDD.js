$(function () {

    $("#id_groupowner_id").change(function () {
        var selectedGroupOwner = $(this).val();

        var poolGroupDropDownList = $("#id_poolgroup_id");
        var poolOwnerDropDownList = $("#id_poolowner_id");

        $.ajax({
            cache: false,
            type: "GET",
            url: "../../../../../poolgroups_by_groupowner/",
            data: { "groupowner_id": selectedGroupOwner },
            success: function (data) {
                data = JSON.parse(data);
                poolGroupDropDownList.html("");
                poolOwnerDropDownList.html("");

                if ($("#id_groupowner_id").val() != -1) {
                    $.each(data, function (id, option) {
                        poolGroupDropDownList.append($("<option></option>").val(option.id).html(option.name))
                    });
                    if (data.length != 0) {
                        var selectedPoolGroup = data[0].id;
                        $.ajax({
                            cache: false,
                            type: "GET",
                            url: "../../../../../poolowners_by_poolgroup/",
                            data: { "poolgroup_id": selectedPoolGroup },
                            success: function (data) {
                                data = JSON.parse(data);
                                poolOwnerDropDownList.html("");
                                if ($("#id_poolgroup_id").val() != -1 && data != []) {
                                    $.each(data, function (id, option) {
                                        poolOwnerDropDownList.append($("<option></option>").val(option.id).html(option.name))
                                    });
                                }
                            },
                            error: function (xhr, ajaxOptions, thrownError) {
                                alert('PoolOwnerList failed to load')
                            }
                        });
                    }
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert('PoolOwnerList failed to load')
            }
        });
    });

    $("#id_poolgroup_id").change(function () {
        var selectedPoolGroup = $(this).val();
        var poolOwnerDropDownList = $("#id_poolowner_id");

        $.ajax({
            cache: false,
            type: "GET",
            url: "../../../../../poolowners_by_poolgroup/",
            data: { "poolgroup_id": selectedPoolGroup },
            success: function (data) {
                data = JSON.parse(data);
                poolOwnerDropDownList.html("");
                if (data.length !== 0) {
                    $.each(data, function (id, option) {
                        poolOwnerDropDownList.append($("<option></option>").val(option.id).html(option.name))
                    });
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert('PoolOwnerList failed to load')
            }
        });
    });

});