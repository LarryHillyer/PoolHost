$(function () {

    $("#id_groupowner_id").change(function () {
        var selectedGroupOwner = $(this).val();
        var poolGroupDropDownList = $("#id_poolgroup_id");
        $.ajax({
            cache: false,
            type: "GET",
            url: "../../../../poolgroups_by_groupowner/",
            data: { "groupowner_id": selectedGroupOwner },
            success: function (data) {
                data = JSON.parse(data);
                poolGroupDropDownList.html("");
                if ($("#id_groupowner_id").val() != -1) {
                    $.each(data, function (id, option) {
                        poolGroupDropDownList.append($("<option></option>").val(option.id).html(option.name))
                    });                    
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert('PoolGroupList failed to load!')
            }
        });
    });

});