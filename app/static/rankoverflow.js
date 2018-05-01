/*!
 * Rank Overflow - client API
 * Copyright 2017 - 2018 Filnor
 * Licensed under MIT (https://github.com/pbdevch/RankOverflow/blob/master/LICENSE)
 */

//Listen for input events (type, paste, etc.)
$("#id").on('input', function () {
    validateForm();
});

/**
 * User has clicked on "Calculate Rank!"
 */
function calculateRank() {
    //Check if users input is valid
    if(!validateForm()) {
        return;
    }

    //Extract id from the URL
    var userId = parseInt($("#id").val().match(/https:\/\/stackoverflow\.com\/users\/\d+/)[0].split('/')[4]);

    //Show loader and loading image
    $(".loader").removeClass("hidden");
    $("#rank-status").html("Your ranks are getting calculated, please wait...");

    //Clear existing results and get ranks
    $(".col-xs-12.card-margin").addClass("hidden");

    fetch(`/api/ranks/${userId}`).then(function(resp){
        return resp.json();
    }).then(function(data) {
        //Read mode from data
        displayRanks("week", data.week.user_rank, data.week.max_page, data.week.last_rank);
        displayRanks("month", data.month.user_rank, data.month.max_page, data.month.last_rank);
        displayRanks("quarter", data.quarter.user_rank, data.quarter.max_page, data.quarter.last_rank);
        displayRanks("year", data.year.user_rank, data.year.max_page, data.year.last_rank);
        displayRanks("alltime", data.alltime.user_rank, data.alltime.max_page, data.alltime.last_rank)

        $("#rank-stats").addClass("hidden");
    }).catch(function(e){console.error(e)});
}

function validateForm() {
    $("#id").val().match(/https:\/\/stackoverflow\.com\/users\/\d+/g);
    if($("#id").val() !== "" && $("#id").val().match(/https:\/\/stackoverflow\.com\/users\/\d+/) !== null ) {
        $("#id").removeClass("invalid");
        $("#idError").removeClass("display");
        return true;
    } else {
        $("#id").addClass("invalid");
        $("#idError").addClass("display");
        return false;
    }
}

function displayRanks(mode, userRank, maxPage, lastRank) {
    var share = userRank / lastRank;
    var percentageExact = share * 100;
    var percentage = percentageExact > 1 ? Math.ceil(percentageExact) : Math.ceil(percentageExact * 100) / 100;

    $(`.rank-${mode}`).first().parent().parent().parent().removeClass("hidden");
    $(`.rank-${mode}`).html(percentage);
    $(`.rank-exact-${mode}`).html(percentageExact);
}