<?php

//region functions
function imgLinks($buffer)
{
    $basic = str_replace('http://localhost/topbar/get-unread-counts?_=1509372063550', 'https://stackexchange.com/topbar/get-unread-counts?_=1509372063550', $buffer);
    $a = trim(preg_replace('/<script.+?<\/script>/', '', $basic));
    $b = trim(preg_replace('/\s\s+/', '', $a));
    return ($b);
}

function read($url) {
    ob_start();
    include($url);
    return ob_get_clean();
}
//endregion

$userId = $_POST['userid'];
$mode = $_POST['mode'];

$leagueType = [
    "week" => date('Y-m-d',strtotime('last sunday')),
    "month" => date("Y-m") . "-01",
    "quarter" => date("Y-m") . "-01",
    "year" => date("Y") . "-01-01",
    "alltime" => "2008-07-31"
];

$url = "https://stackexchange.com/leagues/1/$mode/stackoverflow/$leagueType[$mode]/$userId?sort=reputationchange#$userId";

ini_set("allow_url_include", true);
set_include_path("http://example.com");

ini_set("allow_url_include", false);

echo imgLinks(read($url));

