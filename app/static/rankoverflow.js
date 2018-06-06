/*!
 * Rank Overflow - client API
 * Copyright 2017 - 2018 Filnor
 * Licensed under MIT (https://github.com/pbdevch/RankOverflow/blob/master/LICENSE)
 */
var accounts = [];
var sites = [];

SE.init({
    clientId: 11094,
    key: 'SpGwH7NcD6U2aS6Qmsomug((',
    channelUrl: 'http://rankoverflow.philnet.ch/blank',
    complete: function (data) { console.log(data) }
});

function seAuth() {
    SE.authenticate({
        success: function(data) {
            accounts = data.networkUsers;
            accounts.forEach(function(acc) {
                if(acc.reputation < 200)
                    return;

                $("#sites").append(`<option value="${acc.user_id}">${acc.site_name}</option>`);
                $("#sites").removeAttr("disabled");
            });
            fetch(`/api/sites`).then(function(resp){
                return resp.json();
            }).then(function(data) {
                sites = data;

                //Disable auth button
                $("#seAuthStatus").html("Authenticated");
                $($("#seAuthStatus").parent()).attr("disabled", "disabled");
                $('#calculate').removeClass('disabled');
            }).catch(function(e){console.error(e)});
        },
        error: function(data) { console.error(data) },
        networkUsers: true
    });
}

/**
 * User has clicked on "Calculate Rank!"
 */
function calculateRank() {
    //Show loader and loading image
    $(".loader").removeClass("hidden");
    $("#rank-status").html("Your ranks are getting calculated, please wait...");

    var siteId = 0;
    var siteName = "";
    var selectedSite = $("#sites").find(":selected").text().trim();

    sites.forEach(function(site) {
        if(selectedSite === site.site_full_name) {
            siteId = site.site_id;
            siteName = site.site_name;
        }
    });

    //Clear existing results and get ranks
    $(".col-xs-12.card-margin").addClass("hidden");
    var userId = parseInt($("#sites").val());

    fetch(`/api/ranks/${siteName}/${siteId}/${userId}`).then(function(resp){
        return resp.json();
    }).then(function(data) {
        //Read mode from data
        displayRanks("week", data.week.user_rank, data.week.max_page, data.week.last_rank);
        displayRanks("month", data.month.user_rank, data.month.max_page, data.month.last_rank);
        displayRanks("quarter", data.quarter.user_rank, data.quarter.max_page, data.quarter.last_rank);
        displayRanks("year", data.year.user_rank, data.year.max_page, data.year.last_rank);
        displayRanks("alltime", data.alltime.user_rank, data.alltime.max_page, data.alltime.last_rank);

        $("#rank-stats").addClass("hidden");
    }).catch(function(e){console.error(e)});
}

function displayRanks(mode, userRank, maxPage, lastRank) {
    var share = userRank / lastRank;
    var percentageExact = share * 100;
    var percentage = percentageExact > 1 ? Math.ceil(percentageExact) : Math.ceil(percentageExact * 100) / 100;

    $(`.rank-${mode}`).first().parent().parent().parent().removeClass("hidden");
    $(`.rank-${mode}`).html(percentage);
    $(`.rank-exact-${mode}`).html(percentageExact);
}
