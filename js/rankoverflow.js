/*!
 * Rank Overflow - client API
 * Copyright 2017 pbdevch
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
    $("#rank-stats").html();
    var promise = new Promise(getAllRanks(userId));
    promise.then(function () {
        //Empty promise success handler
    }).catch(function(e){alert(e)});
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

/**
 * Get user rank for a specific mode
 * @param {int} id: user id
 * @param {string} fetchMode: mode (e.g. month) to fetch data for
 */
function getRank(id, fetchMode) {
    //Part 1: Get user rank and last page number
    fetch('api/getUserRankLastPage.php', {
        method: 'POST',
        headers: {
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        },
        body: 'userid=' + id + '&mode=' + fetchMode
    }).then(function(resp){
        return resp.text();
    }).then(function(data) {
        $("#rank-results").html(data);
        var userRank = $($($(".highlight").children()[2]).children()[0]).children()[0].innerText.substr(1);
        var maxPage = $("[rel='next']").parent().children()[$("[rel='next']").parent().children().length-2].innerText;
        $("#rank-results").html("");

        //Part 2: Get lowest rank
        fetch('api/getLastRank.php', {
            method: 'POST',
            headers: {
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
            },
            body: 'mode=' + fetchMode + '&page=' + maxPage
        }).then(function(resp){
            return resp.text();
        }).then(function(data) {
            $("#rank-results").html(data);
            var lastRank = $($(".league-container").last().children()[2]).children().first().children()[0].innerText.substr(1);
            $("#rank-results").html("");
            $(".loader").addClass("hidden");
            $("#rank-status").html("These are your ranks:");
            var share = userRank / lastRank;
            var percentage = share * 100;
            $("#rank-stats").removeClass("hidden").removeClass("loader");
            $("#rank-stats").html($("#rank-stats").html() + "<p>In league " + fetchMode + ": top " + Math.ceil(percentage) + "%</p>");
        }).catch(function(e){});
    }).catch(function(e){});
}
/**
 * Get user rank for all modes
 * @param {int} id: user id
 */
function getAllRanks(id) {
    return function (resolve, reject) {
        try {
            getRank(id, "week");
            getRank(id, "month");
            getRank(id, "quarter");
            getRank(id, "year");
            getRank(id, "alltime");
            resolve();
        } catch(e) {
            reject(e);
        }
    }
}